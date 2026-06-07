import os
import threading
import uuid

from .models.schemas import Job, JobStatus
from .processing.pipeline import process_video

# Shot detection requires a full decode pass; color extraction is comparatively
# quick per-shot. These weights blend the two phases into one overall progress value.
_DETECTION_WEIGHT = 0.6
_EXTRACTION_WEIGHT = 0.4

_jobs: dict[str, Job] = {}
_lock = threading.Lock()


def get_job(job_id: str) -> Job | None:
    with _lock:
        return _jobs.get(job_id)


def _set(job_id: str, **fields) -> None:
    with _lock:
        job = _jobs[job_id]
        _jobs[job_id] = job.model_copy(update=fields)


def _run(job_id: str, path: str, n_colors: int, threshold: float) -> None:
    def on_progress(phase: str, fraction: float) -> None:
        if phase == "detecting_shots":
            overall = fraction * _DETECTION_WEIGHT
        else:
            overall = _DETECTION_WEIGHT + fraction * _EXTRACTION_WEIGHT
        _set(job_id, status=JobStatus(phase), progress=overall)

    try:
        profile = process_video(path, n_colors=n_colors, threshold=threshold, on_progress=on_progress)
        _set(job_id, status=JobStatus.DONE, progress=1.0, result=profile)
    except Exception as e:
        _set(job_id, status=JobStatus.ERROR, error=str(e))


def start_analysis(path: str, n_colors: int = 5, threshold: float = 27.0) -> Job:
    job_id = str(uuid.uuid4())
    job = Job(id=job_id, status=JobStatus.PENDING, filename=os.path.basename(path))
    with _lock:
        _jobs[job_id] = job

    thread = threading.Thread(target=_run, args=(job_id, path, n_colors, threshold), daemon=True)
    thread.start()
    return job
