import face_recognition
import cv2
import pickle
import numpy as np
from utils import match_face

ENCODING_FILE = "face/encodings.pkl"

# Load known data
with open(ENCODING_FILE, "rb") as f:
    known_encodings, known_names = pickle.load(f)

claimed_user = input("Enter your username: ").strip().lower()

cap = cv2.VideoCapture(0)
print("[INFO] Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ✅ Fix: Convert BGR → RGB properly
    rgb = np.ascontiguousarray(frame[:, :, ::-1], dtype=np.uint8)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):

        name, confidence = match_face(known_encodings, known_names, encoding)
        name_lower = name.lower().strip()

        # Decision logic
        if name_lower == claimed_user:
            status = "ACCESS GRANTED"
            color = (0, 255, 0)

        elif name != "Unknown":
            status = "IMPERSONATION DETECTED"
            color = (0, 0, 255)

        else:
            status = "UNKNOWN USER"
            color = (0, 165, 255)

        label = f"{name} | {status} | {confidence:.2f}"

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        print(f"[INFO] {label}")

    cv2.imshow("Face Authentication", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()