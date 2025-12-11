from fastapi import FastAPI, UploadFile, File, HTTPException
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
    """
    Extract structured data from resume file
    
    Supports: PDF, DOCX, JPG, PNG
    """
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
