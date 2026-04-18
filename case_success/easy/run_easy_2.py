## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / EASY  #2
## ============================================================
## Target Object  : <FILL IN>  e.g. "Cereal box / product packaging"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why easy       : Bold logo, multiple colors, high contrast
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_2.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_2.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_easy_2.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": None,

    "MIN_MATCH_COUNT": 10,
    "RATIO_TEST": 0.75,
    "RANSAC_THRESHOLD": 5.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "easy",
    "CASE_NUMBER": 2,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Easy case: product packaging with rich graphics and text",
}

if __name__ == "__main__":
    run_detection(config)
