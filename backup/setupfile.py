#!/usr/bin/env python3
"""
Resume Extractor - Automated Project Setup Script
Run this script to automatically create the complete project structure
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        "app",
        "parsers",
        "extractors",
        "schemas",
        "tests",
        "tests/sample_resumes"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}/")

def create_file(path, content):
    """Create a file with given content"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created file: {path}")

def setup_project():
    """Main setup function"""
    print("\n" + "="*60)
    print("Resume Extractor - Project Setup")
    print("="*60 + "\n")
    
    # Create directories
    print("📁 Creating directory structure...")
    create_directory_structure()
    print()
    
    # Create __init__.py files
    print("📝 Creating __init__.py files...")
    init_files = {
        "app/__init__.py": "",
        "parsers/__init__.py": """from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .image_parser import parse_image

__all__ = ['parse_pdf', 'parse_docx', 'parse_image']
""",
        "extractors/__init__.py": """from .patterns import extract_email, extract_phone, extract_links
from .nlp import extract_entities
from .sections import split_sections
from .skills import extract_skills
from .education import extract_education
from .experience import extract_experience

__all__ = [
    'extract_email',
    'extract_phone',
    'extract_links',
    'extract_entities',
    'split_sections',
    'extract_skills',
    'extract_education',
    'extract_experience'
]
""",
        "schemas/__init__.py": """from .resume import Resume, ExperienceItem, EducationItem

__all__ = ['Resume', 'ExperienceItem', 'EducationItem']
""",
        "tests/__init__.py": ""
    }
    
    for file_path, content in init_files.items():
        create_file(file_path, content)
    print()
    
    # Create schema files
    print("📋 Creating schema files...")
    create_file("schemas/resume.py", """from pydantic import BaseModel
from typing import List, Optional

class ExperienceItem(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class EducationItem(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None

class Resume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    links: List[str] = []
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    certifications: List[str] = []
""")
    print()
    
    # Create parser files
    print("📄 Creating parser files...")
    create_file("parsers/pdf_parser.py", """import pdfplumber

def parse_pdf(path: str) -> str:
    \"\"\"Extract text from PDF file\"\"\"
    text = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text.append(t)
        return "\\n".join(text)
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")
""")
    
    create_file("parsers/docx_parser.py", """from docx import Document

def parse_docx(path: str) -> str:
    \"\"\"Extract text from DOCX file including tables\"\"\"
    try:
        doc = Document(path)
        parts = []
        
        # Extract paragraphs
        for p in doc.paragraphs:
            if p.text.strip():
                parts.append(p.text)
        
        # Extract tables
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells)
                if row_text.strip():
                    parts.append(row_text)
        
        return "\\n".join(parts)
    except Exception as e:
        raise Exception(f"Error parsing DOCX: {str(e)}")
""")
    
    create_file("parsers/image_parser.py", """import pytesseract
from PIL import Image, ImageOps, ImageFilter

def parse_image(path: str) -> str:
    \"\"\"Extract text from image using OCR\"\"\"
    try:
        img = Image.open(path)
        # Preprocess for better OCR
        img = ImageOps.grayscale(img)
        img = img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise Exception(f"Error parsing image: {str(e)}")
""")
    print()
    
    # Create extractor files
    print("🔍 Creating extractor files...")
    create_file("extractors/patterns.py", """import re
from typing import Optional, List

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\\+?\\d{1,3}[-\\s]?)?(?:\\d{10}|\\d{3}[-\\s]?\\d{3}[-\\s]?\\d{4})")
URL_RE = re.compile(r"https?://[^\\s]+|(?:www\\.)?linkedin\\.com/[^\\s]+|github\\.com/[^\\s]+")

def extract_email(text: str) -> Optional[str]:
    \"\"\"Extract first email address\"\"\"
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None

def extract_phone(text: str) -> Optional[str]:
    \"\"\"Extract first phone number\"\"\"
    m = PHONE_RE.search(text)
    return m.group(0) if m else None

def extract_links(text: str) -> List[str]:
    \"\"\"Extract all URLs\"\"\"
    return list(set(URL_RE.findall(text)))
""")
    
    create_file("extractors/nlp.py", """import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Warning: spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

def extract_entities(text: str) -> dict:
    \"\"\"Extract named entities using spaCy\"\"\"
    if not nlp:
        return {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    
    doc = nlp(text[:100000])  # Limit text size for performance
    ents = {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    
    for e in doc.ents:
        if e.label_ in ents:
            ents[e.label_].append(e.text)
    
    return ents
""")
    
    create_file("extractors/sections.py", """HEADERS = [
    "summary", "objective", "profile", "about",
    "education", "academic", "qualification",
    "experience", "work experience", "employment", "work history",
    "skills", "technical skills", "core competencies", "expertise",
    "projects", "certifications", "certificates", "licenses"
]

def split_sections(text: str) -> dict:
    \"\"\"Split resume into sections based on headers\"\"\"
    lines = text.splitlines()
    sections = {}
    current = "other"
    
    for line in lines:
        line_lower = line.strip().lower()
        
        # Check if line is a header
        matched = False
        for header in HEADERS:
            if line_lower.startswith(header) or line_lower == header:
                current = header
                sections[current] = []
                matched = True
                break
        
        if not matched and line.strip():
            sections.setdefault(current, []).append(line)
    
    return {k: "\\n".join(v).strip() for k, v in sections.items() if v}
""")
    
    create_file("extractors/skills.py", """import re
from typing import List

KNOWN_SKILLS = {
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust",
    "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "asp.net",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "ci/cd",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "html", "css", "sass", "bootstrap", "tailwind",
    "rest api", "graphql", "microservices", "agile", "scrum"
}

def extract_skills(section_text: str) -> List[str]:
    \"\"\"Extract skills from skills section\"\"\"
    if not section_text:
        return []
    
    tokens = re.split(r"[,\\n;•·\\|]", section_text.lower())
    found_skills = set()
    
    for token in tokens:
        cleaned = token.strip()
        if cleaned in KNOWN_SKILLS:
            found_skills.add(cleaned)
    
    return sorted(list(found_skills))
""")
    
    create_file("extractors/education.py", """import re
from typing import List

DEGREE_WORDS = [
    "b.tech", "b.e", "b.e.", "btech", "bachelor",
    "bsc", "b.sc", "ba", "b.a",
    "m.tech", "m.e", "m.e.", "mtech", "master",
    "msc", "m.sc", "ms", "m.s", "mba", "m.b.a",
    "phd", "ph.d", "doctorate",
    "diploma", "associate"
]

def extract_education(section_text: str) -> List[dict]:
    \"\"\"Extract education entries\"\"\"
    if not section_text:
        return []
    
    items = []
    blocks = section_text.split("\\n\\n")
    
    for block in blocks:
        lines = [l for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        
        block_lower = block.lower()
        has_degree = any(deg in block_lower for deg in DEGREE_WORDS)
        
        if has_degree:
            years = re.findall(r"(19|20)\\d{2}", block)
            degree = next((d for d in DEGREE_WORDS if d in block_lower), None)
            
            items.append({
                "institution": lines[0] if lines else None,
                "degree": degree,
                "start_year": years[0] if len(years) >= 1 else None,
                "end_year": years[1] if len(years) >= 2 else years[0] if len(years) == 1 else None
            })
    
    return items
""")
    
    create_file("extractors/experience.py", """import re
from typing import List

DATE_RANGE = re.compile(
    r"([A-Za-z]{3,9}\\s?\\d{4}|\\d{4})\\s?[-–—]\\s?([A-Za-z]{3,9}\\s?\\d{4}|\\d{4}|present|current)",
    re.IGNORECASE
)

def extract_experience(section_text: str) -> List[dict]:
    \"\"\"Extract work experience entries\"\"\"
    if not section_text:
        return []
    
    items = []
    blocks = section_text.split("\\n\\n")
    
    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        
        # Find date range
        m = DATE_RANGE.search(block)
        dates = (m.group(1), m.group(2)) if m else (None, None)
        
        # Parse first line for role and company
        first = lines[0]
        role, company = None, None
        
        if " at " in first:
            parts = first.split(" at ", 1)
            role = parts[0].strip()
            company = parts[1].strip()
        elif " - " in first and len(lines) > 1:
            role = first
            company = lines[1] if len(lines) > 1 else None
        else:
            role = first
        
        # Description is remaining lines
        desc_lines = lines[1:] if company else lines[2:] if len(lines) > 2 else []
        description = "\\n".join(desc_lines) if desc_lines else None
        
        items.append({
            "company": company,
            "role": role,
            "start_date": dates[0],
            "end_date": dates[1],
            "description": description
        })
    
    return items
""")
    print()
    
    # Create app files
    print("🚀 Creating application files...")
    create_file("app/pipeline.py", """import os
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from parsers.image_parser import parse_image
from extractors.patterns import extract_email, extract_phone, extract_links
from extractors.nlp import extract_entities
from extractors.sections import split_sections
from extractors.skills import extract_skills
from extractors.education import extract_education
from extractors.experience import extract_experience

def extract_text(path: str) -> str:
    \"\"\"Extract text from file based on extension\"\"\"
    ext = os.path.splitext(path)[1].lower()
    
    if ext == ".pdf":
        return parse_pdf(path)
    elif ext in [".docx", ".doc"]:
        return parse_docx(path)
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
        return parse_image(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def to_json(text: str) -> dict:
    \"\"\"Convert extracted text to structured JSON\"\"\"
    # Split into sections
    sections = split_sections(text)
    
    # Extract entities
    ents = extract_entities(text)
    
    # Extract skills
    skills_text = sections.get("skills", sections.get("technical skills", ""))
    skills = extract_skills(skills_text)
    
    # Extract education
    edu_text = sections.get("education", sections.get("academic", ""))
    education = extract_education(edu_text)
    
    # Extract experience
    exp_text = sections.get("experience", sections.get("work experience", ""))
    experience = extract_experience(exp_text)
    
    # Get summary
    summary = sections.get("summary", sections.get("objective", sections.get("profile", None)))
    
    # Extract basic info
    name = ents["PERSON"][0] if ents["PERSON"] else None
    location = ents["GPE"][0] if ents["GPE"] else None
    
    # Extract certifications
    cert_text = sections.get("certifications", sections.get("certificates", ""))
    certifications = [c.strip() for c in cert_text.splitlines() if c.strip()] if cert_text else []
    
    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": location,
        "links": extract_links(text),
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "education": education,
        "certifications": certifications
    }
""")
    
    create_file("app/main.py", """from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os
from app.pipeline import extract_text, to_json

app = FastAPI(
    title="Resume Extractor API",
    description="Extract structured data from resume files (PDF, DOCX, Images)",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Resume Extractor API",
        "endpoints": {
            "POST /extract": "Upload a resume file to extract data",
            "GET /health": "Check API health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/extract")
async def extract_resume(file: UploadFile = File(...)):
    \"\"\"
    Extract structured data from resume file
    
    Supports: PDF, DOCX, JPG, PNG
    \"\"\"
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(400, "No file provided")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Extract text
            text = extract_text(tmp_path)
            
            # Convert to structured JSON
            data = to_json(text)
            
            return {
                "status": "success",
                "filename": file.filename,
                "data": data
            }
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")
    print()
    
    # Create requirements.txt
    print("📦 Creating requirements.txt...")
    create_file("requirements.txt", """# Core API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Document Parsing
pdfplumber==0.10.3
python-docx==1.1.0
pytesseract==0.3.10
Pillow==10.1.0

# NLP and Text Processing
spacy==3.7.2
en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Data Validation
pydantic==2.5.0

# Utilities
python-dotenv==1.0.0

# Testing (optional)
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
""")
    print()
    
    # Create .gitignore
    print("🔒 Creating .gitignore...")
    create_file(".gitignore", """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temp files
*.tmp
temp/
tmp/

# OS
.DS_Store
Thumbs.db

# Project specific
sample_resumes/
uploads/
*.pdf
*.docx
!tests/sample_resumes/*.pdf
!tests/sample_resumes/*.docx

# Environment
.env
""")
    print()
    
    # Create .env
    print("⚙️  Creating .env...")
    create_file(".env", """API_HOST=0.0.0.0
API_PORT=8000
MAX_UPLOAD_SIZE=10485760
TESSERACT_PATH=/usr/local/bin/tesseract
""")
    print()
    
    # Create README
    print("📖 Creating README.md...")
    create_file("README.md", """# Resume Extractor API

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
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

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
curl -X POST "http://localhost:8000/extract" \\
  -H "Content-Type: multipart/form-data" \\
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
""")
    print()
    
    # Create test file
    print("🧪 Creating test file...")
    create_file("tests/test_api.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Add more tests for file upload when you have sample resumes
""")
    print()
    
    # Final instructions
    print("="*60)
    print("✅ Project setup complete!")
    print("="*60)
    print("\n📋 Next steps:\n")
    print("1. Create a virtual environment:")
    print("   python -m venv .venv")
    print("   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate\n")
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt\n")
    print("3. Download spaCy model:")
    print("   python -m spacy download en_core_web_sm\n")
    print("4. Run the application:")
    print("   uvicorn app.main:app --reload\n")
    print("5. Visit http://localhost:8000/docs for API documentation\n")
    print("="*60)
    print("🎉 Happy coding!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        setup_project()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during setup: {str(e)}")
        sys.exit(1)