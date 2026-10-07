"""
batch_predict.py
----------------
Run imposter detection on a folder of images and produce a summary CSV + annotated outputs.

Usage:
    python batch_predict.py --input ./test_images/ --output ./results/
"""

import argparse
import os
import json
import csv
import cv2

from emotion_model import load_model
from face_utils import load_detector, detect_faces, preprocess_face, draw_results
from deception_scorer import compute_suspicion_score

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}


def batch_predict(input_dir: str, output_dir: str, weights_path: str):
    os.makedirs(output_dir, exist_ok=True)

    print("Loading model and detector...")
    model = load_model(weights_path)
    detector = load_detector()

    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(image_files)} images.\n")

    summary_rows = []

    for filename in sorted(image_files):
        filepath = os.path.join(input_dir, filename)
        image = cv2.imread(filepath)
        if image is None:
            print(f"  [SKIP] Could not load {filename}")
            continue

        faces = detect_faces(image, detector)
        if not faces:
            print(f"  [NO FACE] {filename}")
            summary_rows.append({
                "file": filename, "faces_detected": 0,
                "dominant_emotion": "N/A", "suspicion_score": "N/A", "verdict": "No face detected"
            })
            continue

        for i, bbox in enumerate(faces):
            face_input = preprocess_face(image, bbox)
            raw_probs = model.predict(face_input, verbose=0)[0]
            suspicion_score, dominant_emotion, breakdown = compute_suspicion_score(raw_probs)

            print(f"  {filename} | Face #{i+1} | {dominant_emotion} | Score: {suspicion_score:.1%} | {breakdown['verdict']}")

            image = draw_results(image, bbox, dominant_emotion, suspicion_score, breakdown['probabilities'])

            summary_rows.append({
                "file": filename,
                "face_index": i + 1,
                "faces_detected": len(faces),
                "dominant_emotion": dominant_emotion,
                "dominant_confidence": breakdown['dominant_confidence'],
                "suspicion_score": breakdown['final_suspicion_score'],
                "raw_stress_score": breakdown['raw_stress_score'],
                "masking_penalty": breakdown['masking_penalty'],
                "entropy_factor": breakdown['entropy_factor'],
                "stress_leakage": breakdown['stress_leakage'],
                "verdict": breakdown['verdict'],
                **{f"prob_{em}": v for em, v in breakdown['probabilities'].items()}
            })

        # Save annotated image
        out_path = os.path.join(output_dir, filename)
        cv2.imwrite(out_path, image)

    # Save CSV summary
    csv_path = os.path.join(output_dir, "summary.csv")
    if summary_rows:
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
            writer.writeheader()
            writer.writerows(summary_rows)

    print(f"\nDone. Annotated images saved to: {output_dir}")
    print(f"Summary CSV: {csv_path}")

    # Print flagged images
    suspicious = [r for r in summary_rows if isinstance(r.get('suspicion_score'), float) and r['suspicion_score'] >= 0.65]
    if suspicious:
        print(f"\n🚨 {len(suspicious)} SUSPICIOUS face(s) flagged:")
        for r in suspicious:
            print(f"   {r['file']} (Face #{r.get('face_index', '?')}) — Score: {r['suspicion_score']:.1%}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Imposter Detection")
    parser.add_argument("--input",   required=True,  help="Folder of input images")
    parser.add_argument("--output",  required=True,  help="Folder to save annotated results + CSV")
    parser.add_argument("--weights", default="models/fer2013_weights.h5")
    args = parser.parse_args()

    batch_predict(args.input, args.output, args.weights)
