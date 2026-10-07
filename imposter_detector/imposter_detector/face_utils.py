"""
face_utils.py
-------------
Face detection using OpenCV Haar Cascades + preprocessing for FER2013 model input.
Returns cropped, normalized 48x48 grayscale face patches.
"""

import cv2
import numpy as np
from typing import List, Tuple

# OpenCV ships with this — no separate download needed
HAAR_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def load_detector() -> cv2.CascadeClassifier:
    detector = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    if detector.empty():
        raise RuntimeError("Failed to load Haar cascade. Check OpenCV installation.")
    return detector


def detect_faces(image_bgr: np.ndarray, detector: cv2.CascadeClassifier) -> List[Tuple[int, int, int, int]]:
    """
    Detect all faces in a BGR image.
    Returns list of (x, y, w, h) bounding boxes.
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return list(faces) if len(faces) > 0 else []


def preprocess_face(image_bgr: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """
    Crop face from image and preprocess for model input.
    Returns array of shape (1, 48, 48, 1), float32, normalized to [0, 1].
    """
    x, y, w, h = bbox
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (48, 48))
    face = face.astype(np.float32) / 255.0
    face = np.expand_dims(face, axis=(0, -1))  # (1, 48, 48, 1)
    return face


def draw_results(image_bgr: np.ndarray, bbox: Tuple, emotion: str,
                 suspicion_score: float, probabilities: dict) -> np.ndarray:
    """
    Draw bounding box + emotion label + suspicion score on image.
    """
    img = image_bgr.copy()
    x, y, w, h = bbox

    # Color: green = safe, yellow = caution, red = suspicious
    if suspicion_score >= 0.65:
        color = (0, 0, 220)   # Red
        label = "SUSPICIOUS"
    elif suspicion_score >= 0.40:
        color = (0, 165, 255) # Orange
        label = "CAUTION"
    else:
        color = (0, 200, 0)   # Green
        label = "NORMAL"

    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

    # Main label
    text = f"{emotion} | {label} ({suspicion_score:.0%})"
    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, color, 2, cv2.LINE_AA)

    # Probability bars on the side
    bar_x = x + w + 10
    for i, (em, prob) in enumerate(probabilities.items()):
        bar_y = y + i * 22
        bar_len = int(prob * 120)
        cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_len, bar_y + 16), (200, 200, 200), -1)
        cv2.putText(img, f"{em[:3]}: {prob:.2f}", (bar_x, bar_y + 13),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (30, 30, 30), 1)

    return img
