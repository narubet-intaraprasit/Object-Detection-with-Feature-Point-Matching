## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED AS EXPECTED  #3
## ============================================================
## Target Object  : <FILL IN>  e.g. "Mirror / shiny metal surface"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why expected   : Specular reflection changes appearance per camera angle
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_3.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_3.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_expected_3.mp4"),

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
    "CASE_NUMBER": 3,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Reflective surface — expected to fail, specular highlight changes with viewpoint",
    "FAILURE_ANALYSIS": (
        "Reflective/specular surfaces change appearance drastically with camera angle. "
        "Template keypoints will not match video descriptors due to highlight shift. "
        "Would need photometric-invariant descriptors to handle this."
    ),
}

if __name__ == "__main__":
    run_detection(config)
