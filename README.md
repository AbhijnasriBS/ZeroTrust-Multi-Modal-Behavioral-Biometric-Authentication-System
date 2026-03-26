# ZeroTrust Multi-Modal Behavioral Biometric Authentication System

This project focuses on behavioral biometric authentication for banking environments, with keystroke dynamics as one implemented modality.

## Overview

Keystroke authentication is a behavioral biometric technique that verifies a user based on unique typing patterns. Instead of relying only on passwords or OTPs, the system analyzes timing-based typing behavior such as hold time, down-down time, and up-down time to identify whether the user is genuine or an impostor.

This project aligns with a zero-trust security approach, where identity is continuously validated rather than trusted after a single login.

## Keystroke Authentication Module

The keystroke module is based on the idea that each individual has a unique typing rhythm, similar to a behavioral fingerprint.

### Features Used

- **Hold Time (H):** duration a key is pressed
- **Down-Down Time (DD):** time between pressing consecutive keys
- **Up-Down Time (UD):** time between releasing one key and pressing the next key

These timing features are used to build a user’s behavioral profile.

## Dataset

The implementation uses the **CMU Keystroke Dynamics Dataset**, which contains typing samples collected from multiple users typing the fixed phrase:

`.tie5Roanl`

### Dataset details

- Around **20,400 cleaned samples**
- **52 users**
- **31 timing-based features** used after preprocessing

## Implementation

A keystroke-based authentication pipeline was implemented using Python and scikit-learn.

### Steps performed

1. Loaded the keystroke dataset
2. Removed missing values
3. Dropped non-feature columns such as `sessionIndex` and `rep`
4. Scaled the feature values using `StandardScaler`
5. Trained an **SVM (Support Vector Machine)** model
6. Evaluated authentication performance

## Results

The keystroke model achieved:

- **Accuracy:** approximately **0.89**
- Evaluated using authentication-related metrics:
  - **FAR** — False Acceptance Rate
  - **FRR** — False Rejection Rate
  - **EER** — Equal Error Rate

## Banking Relevance

In banking systems, keystroke authentication can provide an additional layer of protection by:

- detecting impostor access attempts
- strengthening login verification
- supporting continuous identity verification in a zero-trust framework

## Tech Stack

- Python
- Pandas
- scikit-learn
- GitHub for collaboration and version control

## Future Scope

- Add more behavioral biometric modalities
- Introduce privacy-preserving behavioral fingerprinting
- Extend to continuous authentication during banking sessions
