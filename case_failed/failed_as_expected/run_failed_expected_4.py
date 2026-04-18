## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED AS EXPECTED  #4
## ============================================================
## Target Object  : <FILL IN>  e.g. "Transparent glass / plastic bottle"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why expected   : Transparent objects show background through them — no stable features
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_4.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_4.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_expected_4.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 8,
    "RATIO_TEST": 0.80,
    "RANSAC_THRESHOLD": 8.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_as_expected",
    "CASE_NUMBER": 4,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Transparent object — expected to fail, background bleeds through surface",
    "FAILURE_ANALYSIS": (
        "Transparent materials show background through them. "
        "Keypoints detected are from background, not the object itself, so they shift with perspective. "
        "Would need silhouette/contour-based approach or stereo depth cues."
    ),
}

if __name__ == "__main__":
    run_detection(config)
