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
