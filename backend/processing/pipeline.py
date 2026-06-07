import os
from .shot_detector import detect_shots
from .color_extractor import extract_frame, extract_palette
from ..models.schemas import ColorSwatch, MovieProfile, Shot
import cv2


def process_video(video_path: str, n_colors: int = 5, threshold: float = 27.0) -> MovieProfile:
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

    # Detect shots
    raw_shots = detect_shots(video_path, threshold=threshold)

    # For each raw shot, extract color palette from the keyframe
    shots = []
    for raw in raw_shots:
        frame = extract_frame(video_path, raw["keyframe_ms"])
        palette_data = extract_palette(frame, aspect_ratio, n_colors=n_colors)
        shots.append(Shot(
            **raw,
            palette=[ColorSwatch(**s) for s in palette_data],
        ))

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
