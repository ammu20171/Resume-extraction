HEADERS = [
    "summary", "objective", "profile", "about",
    "education", "academic", "qualification",
    "experience", "work experience", "employment", "work history",
    "skills", "technical skills", "core competencies", "expertise",
    "projects", "certifications", "certificates", "licenses"
]

def split_sections(text: str) -> dict:
    """Split resume into sections based on headers"""
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
    
    return {k: "\n".join(v).strip() for k, v in sections.items() if v}
