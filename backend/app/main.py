from __future__ import annotations

from typing import Any, Dict

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import database, models, schemas
from .database import get_db

app = FastAPI(title="AI Image Quality Assessment API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database.init_db()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff"}


@app.get("/health", response_model=schemas.HealthResponse)
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=schemas.AnalysisResponse)
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)) -> Any:
    ext = (file.filename or "").split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file upload")

    import cv2
    import numpy as np

    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Unreadable or corrupt image")

    result = models.analyzer.analyze(image)

    record = database.AnalysisResult(
        filename=file.filename,
        quality_score=float(result["quality_score"]),
        quality_label=result["quality_label"],
        issues=result["issues"],
        features=result["features"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return JSONResponse(
        content={
            "quality_score": result["quality_score"],
            "quality_label": result["quality_label"],
            "issues": result["issues"],
            "features": result["features"],
            "model_status": result["model_status"],
        }
    )


@app.get("/history", response_model=list[schemas.HistoryItem])
def list_history(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.query(database.AnalysisResult).order_by(database.AnalysisResult.id.desc()).all()
    return [
        {
            "id": row.id,
            "filename": row.filename,
            "quality_score": row.quality_score,
            "quality_label": row.quality_label,
            "issues": row.issues,
            "timestamp": row.timestamp.isoformat(),
        }
        for row in rows
    ]


@app.get("/history/{item_id}", response_model=schemas.HistoryItem)
def fetch_history_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    row = db.query(database.AnalysisResult).filter(database.AnalysisResult.id == item_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="History item not found")

    return {
        "id": row.id,
        "filename": row.filename,
        "quality_score": row.quality_score,
        "quality_label": row.quality_label,
        "issues": row.issues,
        "timestamp": row.timestamp.isoformat(),
    }
