from fastapi import APIRouter, Body, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from io import BytesIO
try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None

router = APIRouter()


class ResumeAnalyzeIn(BaseModel):
    resume_text: str
    terms: List[str] | None = None


@router.post("/resume/analyze")
def resume_analyze(data: ResumeAnalyzeIn):
    if not data.resume_text:
        raise HTTPException(400, detail="resume_text requis")
    text = data.resume_text.lower()
    terms = data.terms or []
    missing = [t for t in terms if t.lower() not in text]
    coverage = 0 if not terms else int(100 * (len(terms) - len(missing)) / len(terms))
    suggestions = [f"Ajouter une phrase sur: {t}" for t in missing[:10]]
    return {"missing_terms": missing, "coverage": coverage, "suggestions": suggestions}


@router.post("/resume/upload")
async def resume_upload(file: UploadFile = File(...)):
    if not PdfReader:
        raise HTTPException(400, detail="PDF non supporté côté serveur")
    content = await file.read()
    text = ""
    try:
        reader = PdfReader(BytesIO(content))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        raise HTTPException(400, detail="Extraction PDF échouée")
    return {"text": text.strip()}


