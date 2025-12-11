import re
from typing import List

DATE_RANGE = re.compile(
    r"([A-Za-z]{3,9}\s?\d{4}|\d{4})\s?[-–—]\s?([A-Za-z]{3,9}\s?\d{4}|\d{4}|present|current)",
    re.IGNORECASE
)

def extract_experience(section_text: str) -> List[dict]:
    """Extract work experience entries"""
    if not section_text:
        return []
    
    items = []
    blocks = section_text.split("\n\n")
    
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
        description = "\n".join(desc_lines) if desc_lines else None
        
        items.append({
            "company": company,
            "role": role,
            "start_date": dates[0],
            "end_date": dates[1],
            "description": description
        })
    
    return items
