import argparse
import sys
import cv2
import numpy as np
from fer import FER
from deception_scorer import compute_suspicion_score

def predict_image(image_path, save_path=None, verbose=True):
    image = cv2.imread(image_path)
    if image is None:
        print(f"ERROR: Could not load image at {image_path}")
        sys.exit(1)

    # Upscale small images so face detector can find the face
    h, w = image.shape[:2]
    if w < 100 or h < 100:
        scale = 200 / min(w, h)
        image = cv2.resize(image, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
        print(f"Upscaled image from {w}x{h} to {image.shape[1]}x{image.shape[0]}")

    detector = FER(mtcnn=False)
    results = detector.detect_emotions(image)

    # Filter out small false-positive faces (keep only reasonably sized detections)
    img_area = image.shape[0] * image.shape[1]
    results = [r for r in results if (r["box"][2] * r["box"][3]) > img_area * 0.05]

    if not results:
        print("No faces detected. Trying on full image as face...")
        # Treat the whole image as a face (FER2013 images are already cropped faces)
        results = [{"box": [0, 0, image.shape[1], image.shape[0]],
                    "emotions": detector.detect_emotions(image)[0]["emotions"]
                    if detector.detect_emotions(image) else
                    {"angry":0,"disgust":0,"fear":0,"happy":0,"sad":0,"surprise":0,"neutral":1}}]

    print(f"Detected {len(results)} face(s).\n")

    for i, face_data in enumerate(results):
        box = face_data["box"]
        emotions = face_data["emotions"]

        probs = np.array([
            emotions.get("angry", 0.0),
            emotions.get("disgust", 0.0),
            emotions.get("fear", 0.0),
            emotions.get("happy", 0.0),
            emotions.get("sad", 0.0),
            emotions.get("surprise", 0.0),
            emotions.get("neutral", 0.0)
        ], dtype=np.float32)

        if probs.sum() > 0:
            probs = probs / probs.sum()

        suspicion_score, dominant_emotion, breakdown = compute_suspicion_score(probs)

        if verbose:
            print(f"=== Face #{i+1} ===")
            print(f"  Dominant Emotion : {breakdown['dominant_emotion']} ({breakdown['dominant_confidence']:.1%})")
            print(f"  Suspicion Score  : {suspicion_score:.1%}")
            print(f"  Verdict          : {breakdown['verdict']}")
            print(f"\n  Emotion Breakdown:")
            for em, prob in breakdown['probabilities'].items():
                bar = '█' * int(prob * 30)
                print(f"    {em:<10} {prob:.3f}  {bar}")
            print(f"\n  Scoring Details:")
            print(f"    Raw stress score : {breakdown['raw_stress_score']}")
            print(f"    Masking penalty  : {breakdown['masking_penalty']}")
            print(f"    Entropy factor   : {breakdown['entropy_factor']}")
            print()

        x, y, w, h = box
        if suspicion_score >= 0.65:
            color, label = (0, 0, 220), "SUSPICIOUS"
        elif suspicion_score >= 0.40:
            color, label = (0, 165, 255), "CAUTION"
        else:
            color, label = (0, 200, 0), "NORMAL"

        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
        cv2.putText(image, f"{dominant_emotion} | {label} ({suspicion_score:.0%})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2, cv2.LINE_AA)

    if save_path:
        cv2.imwrite(save_path, image)
        print(f"Annotated image saved to: {save_path}")
    else:
        cv2.imshow("Imposter Detector", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--save", default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    predict_image(args.image, args.save, verbose=not args.quiet)