import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Warning: spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

def extract_entities(text: str) -> dict:
    """Extract named entities using spaCy"""
    if not nlp:
        return {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    
    doc = nlp(text[:100000])  # Limit text size for performance
    ents = {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    
    for e in doc.ents:
        if e.label_ in ents:
            ents[e.label_].append(e.text)
    
    return ents
