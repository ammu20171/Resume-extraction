# Resume Extractor API

A production-ready resume parsing system that extracts structured data from PDF, DOCX, and image files.

## Features

- 📄 Support for PDF, DOCX, and image files
- 🔍 Named Entity Recognition with spaCy
- 📧 Extract email, phone, links
- 💼 Parse work experience, education, skills
- 🚀 FastAPI REST API
- 🧪 OCR support for scanned documents

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the API
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

## Usage

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

## Project Structure

```
resume-extractor/
├── app/              # FastAPI application
├── parsers/          # Document parsers
├── extractors/       # Data extraction logic
├── schemas/          # Pydantic models
└── tests/            # Test files
```

## License

MIT License


 brew install tesseract
