## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED BUT UNEXPECTED  #4
## ============================================================
## Target Object  : <FILL IN>  e.g. "Wall art / painting under changing light"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Why thought ok : Rich painting detail → many keypoints
## Why it failed  : Lighting changes drastically → descriptors shift across frames
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

# Attempt 1: standard SIFT         → detect OK in first 5s, then fails as light changes
# Attempt 2: contrastThreshold=0.01 → more keypoints but wrong matches under new lighting
# Attempt 3: ratio=0.80             → more matches accepted but homography degrades

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_4.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_4.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_unexpected_4.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
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
    "CASE_NUMBER": 4,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Unexpected failure: good texture painting fails under dynamic lighting change",
    "FAILURE_ANALYSIS": (
        "SIFT is designed to be partially illumination invariant via gradient normalization, "
        "but large lighting changes (shadows, dimmer switch, sunlight shift) alter local contrast ratios. "
        "Descriptors computed under different lighting are not comparable enough. "
        "Would need illumination-normalization pre-processing or photometric-invariant descriptors (e.g., DAISY)."
    ),
}

if __name__ == "__main__":
    run_detection(config)
