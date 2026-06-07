from enum import Enum
from pydantic import BaseModel


class ColorSwatch(BaseModel):
    hex: str
    coverage: float


class Shot(BaseModel):
    index: int
    start_ms: float
    end_ms: float
    duration_ms: float
    start_frame: int
    end_frame: int
    keyframe_ms: float
    palette: list[ColorSwatch]


class MovieProfile(BaseModel):
    filename: str
    width: int
    height: int
    aspect_ratio: float
    duration_ms: float
    fps: float
    shot_count: int
    shots: list[Shot]


class JobStatus(str, Enum):
    PENDING = "pending"
    DETECTING_SHOTS = "detecting_shots"
    EXTRACTING_COLORS = "extracting_colors"
    DONE = "done"
    ERROR = "error"


class Job(BaseModel):
    id: str
    status: JobStatus
    progress: float = 0.0
    filename: str | None = None
    result: MovieProfile | None = None
    error: str | None = None
