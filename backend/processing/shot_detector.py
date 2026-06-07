from typing import Callable, Optional
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector


def detect_shots(
    video_path: str,
    threshold: float = 27.0,
    total_frames: Optional[int] = None,
    on_progress: Optional[Callable[[float], None]] = None,
) -> list[dict]:
    """
    Returns a list of shots, each with millisecond timecodes and frame indices.
    threshold: ContentDetector sensitivity — lower = more cuts detected.
    on_progress: called with a 0..1 fraction as cuts are detected (approximate —
    fires once per detected cut, using that cut's frame position as a proxy for
    how far through the video we are).
    """
    video = open_video(video_path)
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))

    callback = None
    if on_progress and total_frames:
        def callback(_frame_img, frame_timecode):
            on_progress(min(frame_timecode.get_frames() / total_frames, 1.0))

    manager.detect_scenes(video, show_progress=False, callback=callback)
    scenes = manager.get_scene_list()

    shots = []
    for i, (start, end) in enumerate(scenes):
        start_ms = start.get_seconds() * 1000
        end_ms = end.get_seconds() * 1000
        shots.append({
            "index": i,
            "start_ms": start_ms,
            "end_ms": end_ms,
            "duration_ms": end_ms - start_ms,
            "start_frame": start.get_frames(),
            "end_frame": end.get_frames(),
            "keyframe_ms": (start_ms + end_ms) / 2,
        })

    return shots
