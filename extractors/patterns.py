import re
from typing import Optional, List

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[-\s]?)?(?:\d{10}|\d{3}[-\s]?\d{3}[-\s]?\d{4})")
URL_RE = re.compile(r"https?://[^\s]+|(?:www\.)?linkedin\.com/[^\s]+|github\.com/[^\s]+")

def extract_email(text: str) -> Optional[str]:
    """Extract first email address"""
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None

def extract_phone(text: str) -> Optional[str]:
    """Extract first phone number"""
    m = PHONE_RE.search(text)
    return m.group(0) if m else None

def extract_links(text: str) -> List[str]:
    """Extract all URLs"""
    return list(set(URL_RE.findall(text)))
