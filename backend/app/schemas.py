from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class IssueResult(BaseModel):
    type: str
    severity: str
    confidence: float


class FeatureSummary(BaseModel):
    laplacian_var: float
    sobel_mean: float
    sobel_std: float
    brightness_mean: float
    brightness_std: float
    dark_ratio: float
    bright_ratio: float
    contrast_rms: float
    noise_est: float
    saturation_mean: float
    entropy: float
    edge_density: float
    blur_fft: float
    block_std: float
    color_hist_skew: float


class AnalysisResponse(BaseModel):
    quality_score: int
    quality_label: str
    issues: List[IssueResult]
    features: Dict[str, Any]
    model_status: str = Field(default="fallback")


class HistoryItem(BaseModel):
    id: int
    filename: str
    quality_score: float
    quality_label: str
    issues: Optional[List[dict]] = None
    timestamp: str
