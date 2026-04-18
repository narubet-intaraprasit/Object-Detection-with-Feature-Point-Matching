## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / DIFFICULT  #1
## ============================================================
## NOTE: Previous asset (red cosmetic jar) was reclassified →
##       moved to case_failed/failed_but_unexpected/ #1
##       Reason: curved surface violates Homography planarity assumption
## ============================================================
## Target Object  : <FILL IN NEW OBJECT>  e.g. "Logo on clothing (fabric moves)"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Difficulty     : Non-rigid deformation — fabric bends/wrinkles
## How solved     : Lower contrastThreshold, higher RANSAC tolerance
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_1.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_1.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_difficult_1.mp4"),

    # ---- Tuned for difficult: more sensitive SIFT ---------------------------
    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,   # default=0.04 → lower = more keypoints
        "edgeThreshold": 20,         # default=10   → higher = keep edge points
        "sigma": 1.2,                # default=1.6  → finer scale detection
    },

    # ---- Relaxed thresholds for difficult cases -----------------------------
    "MIN_MATCH_COUNT": 8,            # lower than easy
    "RATIO_TEST": 0.78,              # slightly looser
    "RANSAC_THRESHOLD": 8.0,         # tolerates more perspective distortion

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "difficult",
    "CASE_NUMBER": 1,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Difficult: non-rigid/deformable object (e.g. logo on moving fabric)",
}

if __name__ == "__main__":
    run_detection(config)
