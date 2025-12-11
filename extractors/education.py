import re
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
    """Extract education entries"""
    if not section_text:
        return []
    
    items = []
    blocks = section_text.split("\n\n")
    
    for block in blocks:
        lines = [l for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        
        block_lower = block.lower()
        has_degree = any(deg in block_lower for deg in DEGREE_WORDS)
        
        if has_degree:
            years = re.findall(r"(19|20)\d{2}", block)
            degree = next((d for d in DEGREE_WORDS if d in block_lower), None)
            
            items.append({
                "institution": lines[0] if lines else None,
                "degree": degree,
                "start_year": years[0] if len(years) >= 1 else None,
                "end_year": years[1] if len(years) >= 2 else years[0] if len(years) == 1 else None
            })
    
    return items
