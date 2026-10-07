import face_recognition
import os
import pickle
import numpy as np

DATA_PATH = "face/data"
ENCODING_FILE = "face/encodings.pkl"

def encode_faces():
    encodings = []
    names = []

    print("[INFO] Encoding faces...")

    for user in os.listdir(DATA_PATH):
        user_path = os.path.join(DATA_PATH, user)

        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)

            image = face_recognition.load_image_file(img_path)
            image = np.ascontiguousarray(image, dtype=np.uint8)
            face_enc = face_recognition.face_encodings(image)

            if len(face_enc) > 0:
                encodings.append(face_enc[0])
                names.append(user)
            else:
                print(f"[WARNING] No face found in {img_path}")

    with open(ENCODING_FILE, "wb") as f:
        pickle.dump((encodings, names), f)

    print("[INFO] Encodings saved successfully!")


if __name__ == "__main__":
    encode_faces()