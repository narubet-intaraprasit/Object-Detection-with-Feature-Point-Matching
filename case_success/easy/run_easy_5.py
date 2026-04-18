## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / EASY  #5
## ============================================================
## Target Object  : <FILL IN>  e.g. "Album cover / comic cover"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why easy       : Colorful artwork, high contrast, many keypoints
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_5.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_5.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_easy_5.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": None,

    "MIN_MATCH_COUNT": 10,
    "RATIO_TEST": 0.75,
    "RANSAC_THRESHOLD": 5.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "easy",
    "CASE_NUMBER": 5,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Easy case: colorful artwork with many distinctive keypoints",
}

if __name__ == "__main__":
    run_detection(config)
