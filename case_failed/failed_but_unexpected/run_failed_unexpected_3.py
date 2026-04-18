## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED BUT UNEXPECTED  #3
## ============================================================
## Target Object  : <FILL IN>  e.g. "Small brand logo on product in video"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why thought ok : Logo has clear graphics and color
## Why it failed  : Logo too small in frame → very low pixel resolution → SIFT scale mismatch
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

# Attempt 1: standard SIFT         → 0 keypoints in video frame
# Attempt 2: contrastThreshold=0.01 → few keypoints but wrong scale match
# Attempt 3: nfeatures=1000         → more keypoints but none near logo

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_3.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_3.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_unexpected_3.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 1000,
        "contrastThreshold": 0.01,
        "edgeThreshold": 25,
        "sigma": 1.0,
    },

    "MIN_MATCH_COUNT": 6,
    "RATIO_TEST": 0.80,
    "RANSAC_THRESHOLD": 10.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_unexpected",
    "CASE_NUMBER": 3,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Unexpected failure: logo too small in video — severe resolution/scale mismatch",
    "FAILURE_ANALYSIS": (
        "When the target object occupies < 50x50 pixels in the video frame, "
        "SIFT cannot extract stable scale-space extrema. "
        "Template is high-res but video representation is too low-res for descriptor matching. "
        "Would need multi-scale image pyramid search or zoom-invariant global features."
    ),
}

if __name__ == "__main__":
    run_detection(config)
