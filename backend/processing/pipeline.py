import os
from typing import Callable, Optional
from .shot_detector import detect_shots
from .color_extractor import extract_frame, extract_palette
from ..models.schemas import ColorSwatch, MovieProfile, Shot
import cv2


def process_video(
    video_path: str,
    n_colors: int = 5,
    threshold: float = 27.0,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> MovieProfile:
    """
    on_progress: called with (phase, fraction) where phase is one of
    "detecting_shots" / "extracting_colors" and fraction is 0..1 within that phase.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    # Get video metadata
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    aspect_ratio = width / height
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_ms = (total_frames / fps) * 1000
    cap.release()

    def report(phase: str, fraction: float):
        if on_progress:
            on_progress(phase, fraction)

    # Phase 1: detect shots
    report("detecting_shots", 0.0)
    raw_shots = detect_shots(
        video_path,
        threshold=threshold,
        total_frames=int(total_frames),
        on_progress=lambda f: report("detecting_shots", f),
    )
    report("detecting_shots", 1.0)

    # Phase 2: extract a color palette from each shot's keyframe
    shots = []
    for raw in raw_shots:
        frame = extract_frame(video_path, raw["keyframe_ms"])
        palette_data = extract_palette(frame, aspect_ratio, n_colors=n_colors)
        shots.append(Shot(
            **raw,
            palette=[ColorSwatch(**s) for s in palette_data],
        ))
        report("extracting_colors", (raw["index"] + 1) / len(raw_shots))

    return MovieProfile(
        filename=os.path.basename(video_path),
        width=int(width),
        height=int(height),
        aspect_ratio=round(aspect_ratio, 4),
        duration_ms=duration_ms,
        fps=fps,
        shot_count=len(shots),
        shots=shots,
    )
