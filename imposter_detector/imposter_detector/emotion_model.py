"""
emotion_model.py
----------------
Defines the CNN architecture trained on FER2013.
7 emotion classes: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, BatchNormalization,
    Dropout, Flatten, Dense, Activation
)


EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
NUM_CLASSES = len(EMOTION_LABELS)
IMG_SIZE = 48  # FER2013 standard


def build_model(input_shape=(48, 48, 1), num_classes=7) -> Sequential:
    """
    Builds the CNN architecture used for FER2013 classification.
    Based on the well-known 4-block architecture with ~73% val accuracy.
    """
    model = Sequential([
        # Block 1
        Conv2D(64, (3, 3), padding='same', input_shape=input_shape),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Dropout(0.25),

        # Block 2
        Conv2D(128, (5, 5), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Dropout(0.25),

        # Block 3
        Conv2D(512, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Dropout(0.25),

        # Block 4
        Conv2D(512, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Dropout(0.25),

        # Classifier head
        Flatten(),
        Dense(256),
        BatchNormalization(),
        Activation('relu'),
        Dropout(0.25),

        Dense(512),
        BatchNormalization(),
        Activation('relu'),
        Dropout(0.25),

        Dense(num_classes, activation='softmax')
    ])
    return model


def load_model(weights_path: str) -> Sequential:
    """Load model with pretrained weights."""
    model = build_model()
    model.load_weights(weights_path)
    return model
