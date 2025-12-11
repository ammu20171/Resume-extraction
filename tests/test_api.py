import io
import pytest
from fastapi.testclient import TestClient
import app.main as main_mod
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

def test_upload_success(monkeypatch):
    # Patch extraction pipeline to avoid heavy deps
    monkeypatch.setattr(main_mod, "extract_text", lambda path: "dummy extracted text")
    monkeypatch.setattr(main_mod, "to_json", lambda text: {"name": "Alice", "email": "alice@example.com"})
    files = {"file": ("resume.pdf", b"%PDF-1.4\n%fake pdf content", "application/pdf")}
    resp = client.post("/extract", files=files)
    assert resp.status_code == 200
    j = resp.json()
    assert j["status"] == "success"
    assert j["filename"] == "resume.pdf"
    assert j["data"]["name"] == "Alice"
    assert j["data"]["email"] == "alice@example.com"

def test_upload_no_filename():
    files = {"file": ("", b"", "application/pdf")}
    resp = client.post("/extract", files=files)
    assert resp.status_code == 400

def test_upload_unsupported_extension():
    files = {"file": ("resume.txt", b"plain text", "text/plain")}
    resp = client.post("/extract", files=files)
    assert resp.status_code == 400
    assert "Unsupported file type" in resp.json().get("detail", "")

def test_upload_processing_error(monkeypatch):
    def _boom(path):
        raise Exception("boom")
    monkeypatch.setattr(main_mod, "extract_text", _boom)
    files = {"file": ("resume.pdf", b"%PDF-1.4\n", "application/pdf")}
    resp = client.post("/extract", files=files)
    assert resp.status_code == 500
    assert "Processing error" in resp.json().get("detail", "")
