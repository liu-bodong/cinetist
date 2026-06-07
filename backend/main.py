from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .processing.pipeline import process_video
from .models.schemas import MovieProfile

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


@app.post("/analyze", response_model=MovieProfile)
async def analyze(req: AnalyzeRequest):
    try:
        return process_video(req.path, n_colors=req.n_colors, threshold=req.threshold)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {req.path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
