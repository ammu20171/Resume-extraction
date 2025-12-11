import pdfplumber

def parse_pdf(path: str) -> str:
    """Extract text from PDF file"""
    text = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text.append(t)
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")
