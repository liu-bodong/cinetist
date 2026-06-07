import cv2
import numpy as np
from sklearn.cluster import KMeans


def extract_palette(frame_bgr: np.ndarray, aspect_ratio: float, n_colors: int = 5) -> list[dict]:
    """
    Returns dominant colors from a frame as hex strings with pixel coverage ratios.
    Clustering is done in LAB space for perceptual accuracy.
    """
    small = cv2.resize(frame_bgr, (int(90 * aspect_ratio), 90), interpolation=cv2.INTER_AREA)
    lab = cv2.cvtColor(small, cv2.COLOR_BGR2LAB)
    pixels = lab.reshape(-1, 3).astype(np.float32)

    kmeans = KMeans(n_clusters=n_colors, n_init=3, random_state=42)
    labels = kmeans.fit_predict(pixels)

    palette = []
    total = len(labels)
    for i, center in enumerate(kmeans.cluster_centers_):
        coverage = float(np.sum(labels == i) / total)
        lab_pixel = np.uint8([[center]])
        bgr = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2BGR)[0][0]
        hex_color = f"#{int(bgr[2]):02x}{int(bgr[1]):02x}{int(bgr[0]):02x}"
        palette.append({"hex": hex_color, "coverage": round(coverage, 4)})

    palette.sort(key=lambda x: x["coverage"], reverse=True)
    return palette


def extract_frame(video_path: str, timestamp_ms: float) -> np.ndarray:
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_ms)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not read frame at {timestamp_ms:.0f}ms from {video_path}")
    return frame
