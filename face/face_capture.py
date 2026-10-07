import cv2
import os

def capture_images(user_name, num_images=15):
    save_path = f"face/data/{user_name}"
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("[INFO] Press 's' to capture images, 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Face Capture", frame)

        key = cv2.waitKey(1)

        if key == ord('s'):
            file_path = os.path.join(save_path, f"{count}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"[INFO] Saved {file_path}")
            count += 1

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    user = input("Enter username: ")
    capture_images(user)