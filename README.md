# PDF to DOCX Converter

A lightweight, production-ready web application that converts PDF files to editable Microsoft Word (.docx) documents instantly. No authentication required, privacy-focused, and easy to deploy.

## Features

- **Zero Authentication**: No sign-up, login, or account creation required
- **Privacy First**: Files are automatically deleted after download or within 10 minutes
- **Modern UI**: Clean, responsive interface with drag-and-drop support
- **Fast Conversion**: Convert PDFs to DOCX in seconds
- **Secure**: File size limits, type validation, and automatic cleanup
- **Easy Deployment**: Deploy to free hosting platforms in minutes

## Tech Stack

- **Backend**: FastAPI (Python)
- **Conversion Engine**: pdf2docx
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **File Handling**: Async I/O with aiofiles

## Installation & Local Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or download this repository**
   ```bash
   cd pdf-to-docx-converter
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

## Usage

1. Open the application in your browser
2. Drag and drop a PDF file or click "Browse Files" to select one
3. Wait for the conversion to complete (usually a few seconds)
4. Download the converted DOCX file automatically
5. Convert another file or close the page

## File Limits

- **Maximum file size**: 25MB
- **Supported format**: PDF only
- **File retention**: Files are deleted immediately after download or within 10 minutes

## Deployment

### Option 1: Render (Recommended)

1. Create a free account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository or upload files
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Click "Create Web Service"

### Option 2: Railway

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Python and dependencies
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

### Option 3: Hugging Face Spaces

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space
3. Choose "Gradio" or "Streamlit" SDK (or use custom Docker)
4. Upload files
5. Add `app.py` pointing to your FastAPI app
6. Deploy

### Option 4: Docker (Self-hosted)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t pdf-to-docx .
docker run -p 8000:8000 pdf-to-docx
```

## Project Structure

```
pdf-to-docx-converter/
├── main.py                 # FastAPI backend with conversion logic
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Frontend UI
├── temp_files/            # Temporary storage (auto-created, auto-cleaned)
└── README.md              # Documentation
```

## API Endpoints

### `GET /`
Serves the main HTML interface

### `POST /convert`
Converts uploaded PDF to DOCX
- **Request**: multipart/form-data with `file` field
- **Response**: DOCX file download
- **Errors**: 
  - 400: Invalid file type or size
  - 422: Conversion failed (corrupted/protected PDF)
  - 500: Server error

### `GET /health`
Health check endpoint
- **Response**: `{"status": "healthy", "service": "PDF to DOCX Converter"}`

## Security Considerations

- File type validation on client and server
- File size limits (25MB)
- No permanent storage of user files
- Automatic file cleanup every minute
- CORS configured for production use
- No user data collection or tracking

## Troubleshooting

### Conversion fails for specific PDFs
- **Password-protected PDFs**: Not supported. Remove password first.
- **Corrupted files**: Ensure the PDF opens correctly in a PDF reader
- **Large files**: Files over 25MB are rejected. Try compressing the PDF first.

### Port already in use
Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use different port
```

### Dependencies installation fails
Ensure you have Python 3.8+ and pip updated:
```bash
python --version
pip install --upgrade pip
```

## License

This project is provided as-is for educational and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Built with ❤️ using FastAPI and pdf2docx
