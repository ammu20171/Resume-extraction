# ...existing code...
import pytesseract
from PIL import Image, ImageOps, ImageFilter
import shutil

def parse_image(path: str) -> str:
    """Extract text from image using OCR. Checks for tesseract binary first."""
    if not shutil.which("tesseract"):
        raise RuntimeError("tesseract is not installed or it's not in your PATH. Install it (macOS: `brew install tesseract`) and restart the service.")
    try:
        img = Image.open(path)
        # Preprocess for better OCR
        img = ImageOps.grayscale(img)
        img = img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise Exception(f"Error parsing image: {str(e)}")