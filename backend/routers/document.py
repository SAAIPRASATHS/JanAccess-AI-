"""
Document Router — Upload, extract, and simplify government documents.
"""
import os
import uuid
import shutil
import logging
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import DocumentAnalysis
from backend.services import ai_service
from backend.schemas import AnalysisResponse

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = "backend/static/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document (TXT or PDF) and get a simplified explanation.
    """
    # Validate file type
    allowed_extensions = [".txt", ".pdf"]
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save file
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        content = ""
        if file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        elif file_ext == ".pdf":
            content = _extract_pdf_text(file_path)

        if not content.strip():
            content = "The document appears to be empty or could not be read."

        # Simplify using AI
        simplification = await ai_service.simplify_text(content)
        next_steps = await ai_service.generate_next_steps(content)

        # Store in database
        summary = content[:300] + "..." if len(content) > 300 else content
        analysis = DocumentAnalysis(
            filename=file.filename,
            content_summary=summary,
            simplification=simplification
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return AnalysisResponse(
            filename=file.filename or "unknown",
            summary=summary,
            simplification=simplification,
            next_steps=next_steps
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document analysis error: {e}")
        raise HTTPException(status_code=500, detail="Document analysis failed.")
    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass


def _extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages[:20]:  # Limit to 20 pages
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except ImportError:
        logger.warning("PyPDF2 not installed — returning placeholder for PDF.")
        return "PDF text extraction requires PyPDF2. Install it with: pip install PyPDF2"
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return "Could not extract text from this PDF. The file may be scanned or encrypted."
