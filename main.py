from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from pdf2docx import Converter
import shutil

app = FastAPI(title="PDF to DOCX Converter")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary directory for file storage
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

# File cleanup configuration
MAX_FILE_AGE_MINUTES = 10
MAX_FILE_SIZE_MB = 25


async def cleanup_old_files():
    """Background task to clean up files older than MAX_FILE_AGE_MINUTES"""
    while True:
        try:
            current_time = datetime.now()
            for file_path in TEMP_DIR.glob("*"):
                if file_path.is_file():
                    file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age > timedelta(minutes=MAX_FILE_AGE_MINUTES):
                        file_path.unlink()
                        print(f"Cleaned up old file: {file_path.name}")
        except Exception as e:
            print(f"Error during cleanup: {e}")

        await asyncio.sleep(60)  # Run cleanup every minute


@app.on_event("startup")
async def startup_event():
    """Start background cleanup task on app startup"""
    asyncio.create_task(cleanup_old_files())


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/convert")
async def convert_pdf_to_docx(file: UploadFile = File(...)):
    """
    Convert uploaded PDF to DOCX format

    Args:
        file: Uploaded PDF file

    Returns:
        FileResponse with the converted DOCX file
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Validate content type
    if file.content_type not in ['application/pdf', 'application/x-pdf']:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file")

    # Generate unique filenames
    unique_id = str(uuid.uuid4())
    pdf_path = TEMP_DIR / f"{unique_id}.pdf"
    docx_path = TEMP_DIR / f"{unique_id}.docx"

    try:
        # Save uploaded PDF
        with open(pdf_path, "wb") as buffer:
            content = await file.read()

            # Check file size (25MB limit)
            if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB limit"
                )

            buffer.write(content)

        # Convert PDF to DOCX
        try:
            cv = Converter(str(pdf_path))
            cv.convert(str(docx_path))
            cv.close()
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to convert PDF. The file may be corrupted, password-protected, or invalid. Error: {str(e)}"
            )

        # Verify DOCX was created
        if not docx_path.exists():
            raise HTTPException(status_code=500, detail="Conversion failed. Output file not created")

        # Get original filename without extension
        original_name = Path(file.filename).stem
        output_filename = f"{original_name}.docx"

        # Return the converted file
        return FileResponse(
            path=str(docx_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            background=cleanup_files_after_download(pdf_path, docx_path)
        )

    except HTTPException:
        # Clean up files on error
        if pdf_path.exists():
            pdf_path.unlink()
        if docx_path.exists():
            docx_path.unlink()
        raise
    except Exception as e:
        # Clean up files on unexpected error
        if pdf_path.exists():
            pdf_path.unlink()
        if docx_path.exists():
            docx_path.unlink()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


async def cleanup_files_after_download(pdf_path: Path, docx_path: Path):
    """Background task to delete files after download completes"""
    await asyncio.sleep(2)  # Give time for download to complete
    try:
        if pdf_path.exists():
            pdf_path.unlink()
        if docx_path.exists():
            docx_path.unlink()
    except Exception as e:
        print(f"Error cleaning up files: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PDF to DOCX Converter"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
