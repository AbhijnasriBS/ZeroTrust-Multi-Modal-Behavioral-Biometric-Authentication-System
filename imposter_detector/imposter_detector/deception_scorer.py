"""
deception_scorer.py
--------------------
Core logic that converts raw emotion probabilities into a "suspicion score"
indicating possible impersonation / deceptive behavior.

Psychological basis:
- Impersonators often show fear, disgust, or anger suppressed under a neutral/happy mask
- Leakage: high confidence in stress emotions even when trying to appear calm
- Micro-expressions: sharp confidence spikes in fear/anger/disgust
- Masking: very high confidence in "happy" or "neutral" combined with residual fear/anger

Score is between 0.0 (clearly genuine) and 1.0 (highly suspicious).
"""

from typing import Dict, Tuple
import numpy as np

# Emotion indices matching FER2013 label order
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Weights for suspicion contribution
# Stress emotions → increase suspicion
# Happy/Surprise → decrease (genuine positive)
SUSPICION_WEIGHTS = {
    'Angry':    0.75,   # Strong stress signal
    'Disgust':  0.80,   # Strong deception signal (contempt)
    'Fear':     0.90,   # Strongest — panic, being caught
    'Happy':    -0.30,  # Reduces suspicion (genuine positive)
    'Sad':      0.40,   # Mild stress
    'Surprise': 0.10,   # Neutral — context dependent
    'Neutral':  0.05,   # Slight — masking behavior
}

# When dominant emotion is one of these with high confidence, apply masking penalty
MASKING_EMOTIONS = {'Happy', 'Neutral'}
MASKING_THRESHOLD = 0.60  # If >60% confident in a mask emotion

# If stress emotion probability exceeds this despite mask, it's leakage
LEAKAGE_THRESHOLD = 0.10
STRESS_EMOTIONS = {'Angry', 'Disgust', 'Fear', 'Sad'}


def compute_suspicion_score(probabilities: np.ndarray) -> Tuple[float, str, Dict]:
    """
    Args:
        probabilities: np.array of shape (7,) — softmax output from emotion model

    Returns:
        suspicion_score (float, 0–1)
        dominant_emotion (str)
        breakdown (dict) — detailed scoring breakdown for transparency
    """
    probs = dict(zip(EMOTIONS, probabilities.tolist()))

    # --- Step 1: Weighted stress score ---
    raw_score = 0.0
    for emotion, weight in SUSPICION_WEIGHTS.items():
        raw_score += probs[emotion] * weight
    raw_score = np.clip(raw_score, 0.0, 1.0)

    # --- Step 2: Masking penalty ---
    dominant = max(probs, key=probs.get)
    masking_penalty = 0.0

    if dominant in MASKING_EMOTIONS and probs[dominant] > MASKING_THRESHOLD:
        # Check for leakage: stress emotions bleeding through
        stress_leakage = sum(probs[e] for e in STRESS_EMOTIONS)
        if stress_leakage > LEAKAGE_THRESHOLD:
            masking_penalty = stress_leakage * 0.5  # Scale penalty by leakage amount

    # --- Step 3: Entropy analysis ---
    # Very low entropy (one emotion completely dominant) = more genuine
    # Moderate entropy with stress = suspicious (conflicted emotional state)
    entropy = -sum(p * np.log(p + 1e-8) for p in probs.values())
    max_entropy = np.log(len(EMOTIONS))
    normalized_entropy = entropy / max_entropy  # 0–1

    # Suspicious zone: moderate entropy (0.3–0.7) with stress
    stress_prob = sum(probs[e] for e in STRESS_EMOTIONS)
    entropy_factor = 0.0
    if 0.3 < normalized_entropy < 0.75 and stress_prob > 0.2:
        entropy_factor = normalized_entropy * stress_prob * 0.4

    # --- Final score ---
    final_score = np.clip(raw_score + masking_penalty + entropy_factor, 0.0, 1.0)

    breakdown = {
        "dominant_emotion": dominant,
        "dominant_confidence": round(probs[dominant], 3),
        "raw_stress_score": round(raw_score, 3),
        "masking_penalty": round(masking_penalty, 3),
        "entropy_factor": round(entropy_factor, 3),
        "normalized_entropy": round(normalized_entropy, 3),
        "stress_leakage": round(sum(probs[e] for e in STRESS_EMOTIONS), 3),
        "final_suspicion_score": round(float(final_score), 3),
        "verdict": classify_verdict(final_score),
        "probabilities": {k: round(v, 3) for k, v in probs.items()}
    }

    return float(final_score), dominant, breakdown


def classify_verdict(score: float) -> str:
    if score >= 0.65:
        return "SUSPICIOUS — High stress/deceptive cues detected"
    elif score >= 0.40:
        return "CAUTION — Some emotional inconsistency"
    else:
        return "NORMAL — No significant deceptive cues"
