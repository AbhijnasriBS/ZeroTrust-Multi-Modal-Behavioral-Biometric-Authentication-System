"""
download_model.py
-----------------
Downloads pretrained FER2013 model weights.
Source: https://github.com/gitshanks/fer2013
Run once before using the detector.
"""

import os
import requests
from tqdm import tqdm

WEIGHTS_URL = "https://github.com/gitshanks/fer2013/raw/master/facialemotionmodel.h5"
WEIGHTS_PATH = "models/fer2013_weights.h5"


def download_file(url: str, dest: str):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    print(f"Downloading weights from {url}")
    with open(dest, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))
    print(f"Saved to {dest}")


if __name__ == "__main__":
    if os.path.exists(WEIGHTS_PATH):
        print(f"Weights already exist at {WEIGHTS_PATH}")
    else:
        download_file(WEIGHTS_URL, WEIGHTS_PATH)
        print("Done. You can now run predict.py")
