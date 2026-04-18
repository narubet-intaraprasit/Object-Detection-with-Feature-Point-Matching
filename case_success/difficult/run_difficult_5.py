## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / DIFFICULT  #5
## ============================================================
## Target Object  : <FILL IN>  e.g. "Small sticker/logo on laptop lid"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Difficulty     : Object is small relative to frame, scale challenge
## How solved     : Increase nfeatures, lower contrastThreshold
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_5.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_5.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_difficult_5.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 1000,           # force SIFT to find more keypoints
        "contrastThreshold": 0.02,
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 8,
    "RATIO_TEST": 0.78,
    "RANSAC_THRESHOLD": 8.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "difficult",
    "CASE_NUMBER": 5,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Difficult: small target object relative to frame size — scale issue",
}

if __name__ == "__main__":
    run_detection(config)
