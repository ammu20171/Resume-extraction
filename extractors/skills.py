import re
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
    """Extract skills from skills section"""
    if not section_text:
        return []
    
    tokens = re.split(r"[,\n;•·\|]", section_text.lower())
    found_skills = set()
    
    for token in tokens:
        cleaned = token.strip()
        if cleaned in KNOWN_SKILLS:
            found_skills.add(cleaned)
    
    return sorted(list(found_skills))
