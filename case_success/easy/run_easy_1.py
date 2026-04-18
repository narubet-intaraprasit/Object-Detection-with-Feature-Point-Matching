## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / EASY  #1
## ============================================================
## Target Object  : <FILL IN>  e.g. "Book cover - Harry Potter"
## Template Source: <FILL IN>  e.g. "Self-photographed"
## Video Source   : <FILL IN>  e.g. "Self-recorded"
## Why easy       : Object has rich color/texture, simple background
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    # ---- Paths (put your files in assets/) ----------------------------------
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_1.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_1.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_easy_1.mp4"),

    # ---- Feature Detector ---------------------------------------------------
    "FEATURE_CHOICE": 1,       # 1=SIFT (recommended for easy), 3=ORB
    "SIFT_PARAMS": None,       # None = SIFT defaults (good for easy cases)

    # ---- Matching Parameters ------------------------------------------------
    "MIN_MATCH_COUNT": 10,     # easy: standard threshold
    "RATIO_TEST": 0.75,        # easy: Lowe's standard ratio
    "RANSAC_THRESHOLD": 5.0,   # easy: standard RANSAC error

    # ---- Display ------------------------------------------------------------
    "DRAW_CHOICE": 1,          # 1=bounding box
    "WAIT_MS": 30,

    # ---- Case Info (for report) ---------------------------------------------
    "CASE_TYPE": "easy",
    "CASE_NUMBER": 1,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Easy case: rich texture/color, plain background, frontal view",
}

if __name__ == "__main__":
    run_detection(config)
