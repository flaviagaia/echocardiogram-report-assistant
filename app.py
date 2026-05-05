from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.clinical_logic import DiastolicValue, EffusionValue, LVSizeValue, RVFunctionValue, ValveSeverityValue
from src.pipeline import EchocardiogramReportAssistantPipeline


app = FastAPI(title="Echocardiogram Report Assistant")
pipeline = EchocardiogramReportAssistantPipeline()


class DraftRequest(BaseModel):
    indication: str
    lvef_percent: int = Field(..., ge=5, le=90)
    lv_size: LVSizeValue
    rv_function: RVFunctionValue
    diastolic_function: DiastolicValue
    mitral_regurgitation: ValveSeverityValue
    aortic_stenosis: ValveSeverityValue
    pericardial_effusion: EffusionValue
    extra_notes: str = ""
    top_k: int = Field(default=5, ge=1, le=10)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "echocardiogram-report-assistant"}


@app.post("/draft-report")
def draft_report(payload: DraftRequest) -> dict:
    return pipeline.run(**payload.model_dump())
