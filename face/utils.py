import numpy as np
import face_recognition

def match_face(known_encodings, known_names, current_encoding, threshold=0.5):
    distances = face_recognition.face_distance(known_encodings, current_encoding)

    best_index = np.argmin(distances)
    best_distance = distances[best_index]

    confidence = 1 - best_distance

    if best_distance < threshold:
        return known_names[best_index], confidence
    else:
        return "Unknown", confidence