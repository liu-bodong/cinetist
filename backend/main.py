from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import jobs
from .models.schemas import Job

app = FastAPI(title="Cinetist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    path: str
    n_colors: int = 5
    threshold: float = 27.0


@app.post("/analyze", response_model=Job)
async def analyze(req: AnalyzeRequest):
    if not req.path:
        raise HTTPException(status_code=400, detail="Path is required")
    return jobs.start_analysis(req.path, n_colors=req.n_colors, threshold=req.threshold)


@app.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/health")
async def health():
    return {"status": "ok"}
