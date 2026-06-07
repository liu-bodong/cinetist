from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector


def detect_shots(video_path: str, threshold: float = 27.0) -> list[dict]:
    """
    Returns a list of shots, each with millisecond timecodes and frame indices.
    threshold: ContentDetector sensitivity — lower = more cuts detected.
    """
    video = open_video(video_path)
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video, show_progress=True)
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
