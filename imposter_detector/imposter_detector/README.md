# 🕵️ Imposter Detector — Facial Emotion Analysis

Detects behavioral and emotional cues suggesting deceptive behavior or impersonation,
using FER2013-trained CNN + a multi-factor suspicion scoring system.

---

## How It Works

### Step 1 — Face Detection
Uses OpenCV Haar Cascade to locate all faces in the image.

### Step 2 — Emotion Classification
A CNN (trained on FER2013) classifies each face into 7 emotions:
`Angry | Disgust | Fear | Happy | Sad | Surprise | Neutral`

### Step 3 — Suspicion Scoring (`deception_scorer.py`)
Three factors combine into a single **suspicion score (0–1)**:

| Factor | What it captures |
|--------|-----------------|
| **Weighted stress score** | Fear/Disgust/Anger are weighted heavily; Happy reduces score |
| **Masking penalty** | High-confidence Neutral/Happy + underlying stress = deception signal |
| **Entropy factor** | Conflicted emotional state (mixed probabilities) with stress leakage |

### Verdicts
| Score | Label | Meaning |
|-------|-------|---------|
| ≥ 0.65 | 🔴 SUSPICIOUS | Strong stress/deceptive cues |
| 0.40–0.64 | 🟠 CAUTION | Some emotional inconsistency |
| < 0.40 | 🟢 NORMAL | No significant cues |

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download pretrained weights
```bash
python download_model.py
```
This downloads `models/fer2013_weights.h5` (~25MB) from the `gitshanks/fer2013` repo.

---

## Usage

### Single image
```bash
python predict.py --image path/to/face.jpg
```

Save annotated output:
```bash
python predict.py --image face.jpg --save output.jpg
```

Save JSON results:
```bash
python predict.py --image face.jpg --save output.jpg --json results.json
```

### Batch (folder of images)
```bash
python batch_predict.py --input ./test_images/ --output ./results/
```
Produces:
- Annotated images with bounding boxes + scores
- `results/summary.csv` with all scores per face

---

## Psychological Basis

Impersonators exhibit classic behavioral cues:

- **Fear leakage** — Panic from being discovered seeps through even when trying to appear calm
- **Disgust/contempt** — Involuntary micro-expressions of contempt when pretending to be someone else
- **Masking behavior** — Deliberate suppression of stress under a "happy" or "neutral" face creates
  a characteristic high-confidence-mask + residual-stress-leakage pattern
- **Emotional entropy** — Genuine emotions tend to be clear (low entropy). Deceptive states
  are conflicted (moderate-high entropy with stress bleeding through)

---

## Extending This

### To improve accuracy:
1. **Fine-tune on labeled deception data** — AffectNet, RAF-DB, or DFEW have more nuanced labels
2. **Add facial landmark analysis** — Use MediaPipe Face Mesh to track asymmetry, muscle tension
3. **Use a Vision Transformer** — Replace CNN with ViT/EfficientNet for ~5% accuracy gain on FER2013
4. **Add context window** — For video: track emotion change over time, not just per-frame

### Alternative/better datasets for this task:
| Dataset | Why better |
|---------|-----------|
| **DEAP** | Physiological + facial for deception |
| **AffectNet** | 450k images, finer-grained labels |
| **RAF-DB** | Real-world, compound expressions |
| **DDCF** | Specifically for deception detection |

---

## Output Example (JSON)
```json
{
  "dominant_emotion": "Neutral",
  "dominant_confidence": 0.71,
  "raw_stress_score": 0.312,
  "masking_penalty": 0.18,
  "entropy_factor": 0.09,
  "final_suspicion_score": 0.582,
  "verdict": "CAUTION — Some emotional inconsistency",
  "probabilities": {
    "Angry": 0.08, "Disgust": 0.05, "Fear": 0.12,
    "Happy": 0.04, "Sad": 0.09, "Surprise": 0.01, "Neutral": 0.71
  }
}
```
