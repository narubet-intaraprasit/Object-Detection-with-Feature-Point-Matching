## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / DIFFICULT  #2
## ============================================================
## Target Object  : <FILL IN>  e.g. "Road sign (extreme camera angle)"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Difficulty     : Large perspective change, moving camera
## How solved     : Higher RANSAC threshold, sensitive SIFT
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_2.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_2.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_difficult_2.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 8,
    "RATIO_TEST": 0.78,
    "RANSAC_THRESHOLD": 10.0,        # very tolerant for large perspective shift

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "difficult",
    "CASE_NUMBER": 2,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Difficult: large perspective distortion / extreme viewing angle",
}

if __name__ == "__main__":
    run_detection(config)
