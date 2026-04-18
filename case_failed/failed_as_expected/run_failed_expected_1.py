## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED AS EXPECTED  #1
## ============================================================
## Target Object  : <FILL IN>  e.g. "Plain brown paper / post-it note"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why expected   : Near-zero texture → SIFT finds almost no keypoints
##                  Cannot reach MIN_MATCH_COUNT even with loose params
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_1.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_1.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_expected_1.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,   # tried lowering — still not enough features
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 8,            # tried lowest practical threshold
    "RATIO_TEST": 0.80,              # tried loosest ratio
    "RANSAC_THRESHOLD": 8.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_as_expected",
    "CASE_NUMBER": 1,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Plain/uniform surface — expected to fail due to near-zero texture",
    "FAILURE_ANALYSIS": (
        "Plain paper/solid surface has no corners, blobs, or gradients. "
        "SIFT requires local intensity variation to detect keypoints. "
        "To succeed, would need edge-based descriptor or color histogram approach."
    ),
}

if __name__ == "__main__":
    run_detection(config)
