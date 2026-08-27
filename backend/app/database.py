from __future__ import annotations

import os
from datetime import datetime
from typing import Generator

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quality.db")


def ensure_sqlite_parent_dir(url: str) -> None:
    if not url.startswith("sqlite"):
        return

    db_path = url.replace("sqlite:///", "", 1)
    if db_path.startswith("/"):
        parent_dir = os.path.dirname(db_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)


ensure_sqlite_parent_dir(DATABASE_URL)


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    quality_score = Column(Float, nullable=False)
    quality_label = Column(String, nullable=False)
    issues = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
