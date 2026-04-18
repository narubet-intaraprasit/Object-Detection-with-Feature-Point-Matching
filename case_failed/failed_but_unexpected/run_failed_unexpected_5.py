## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED BUT UNEXPECTED  #5
## ============================================================
## Target Object  : <FILL IN>  e.g. "Book cover in cluttered bookshelf"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why thought ok : Book cover has rich art/text
## Why it failed  : Background clutter has similar features → many false matches
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

# Attempt 1: standard SIFT   → bounding box jitters wildly onto wrong books
# Attempt 2: ratio=0.65      → fewer matches, still wrong location
# Attempt 3: MIN_MATCH=15    → barely detects anything

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_5.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_5.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_unexpected_5.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 6,
    "RATIO_TEST": 0.80,
    "RANSAC_THRESHOLD": 10.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_unexpected",
    "CASE_NUMBER": 5,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Unexpected failure: visually rich target overwhelmed by similar background clutter",
    "FAILURE_ANALYSIS": (
        "A bookshelf background contains many book spines with text and colors similar to the target. "
        "FLANN matches template features to background books rather than the target. "
        "RANSAC finds a consistent homography — but for the wrong object. "
        "Would need spatial context (ROI proposal) or distinctive global color signature to isolate target."
    ),
}

if __name__ == "__main__":
    run_detection(config)
