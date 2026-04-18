## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / DIFFICULT  #4
## ============================================================
## Target Object  : <FILL IN>  e.g. "Product in low-light / dim room"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Difficulty     : Low illumination reduces contrast and keypoint quality
## How solved     : Very low contrastThreshold in SIFT, loose ratio test
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_4.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_4.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_difficult_4.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.01,   # very sensitive — captures low-contrast keypoints
        "edgeThreshold": 25,
        "sigma": 1.0,
    },

    "MIN_MATCH_COUNT": 8,
    "RATIO_TEST": 0.80,              # loosest ratio — accept weaker matches
    "RANSAC_THRESHOLD": 8.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "difficult",
    "CASE_NUMBER": 4,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Difficult: low-light scene reduces SIFT keypoint quality significantly",
}

if __name__ == "__main__":
    run_detection(config)
