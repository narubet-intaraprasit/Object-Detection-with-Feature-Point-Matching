## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED AS EXPECTED  #5
## ============================================================
## Target Object  : <FILL IN>  e.g. "Uniform wall / floor tile"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why expected   : Repetitive pattern — FLANN confuses identical local patches
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_5.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_5.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_expected_5.mp4"),

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
    "CASE_NUMBER": 5,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Repetitive pattern (tiles/wall) — FLANN produces many false matches",
    "FAILURE_ANALYSIS": (
        "Repetitive/periodic patterns (tiles, brick, fabric weave) produce near-identical local descriptors. "
        "FLANN cannot distinguish between repeating patches, causing many incorrect matches. "
        "RANSAC cannot recover a valid homography from these ambiguous correspondences. "
        "Would need global appearance features (e.g., color histogram, whole-image embedding)."
    ),
}

if __name__ == "__main__":
    run_detection(config)
