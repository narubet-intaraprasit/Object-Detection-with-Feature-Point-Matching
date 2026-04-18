## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED BUT UNEXPECTED  #2
## ============================================================
## Target Object  : Single white sheep in a moving flock
## Template Source: Close-up photo of one white sheep (slightly blurry, full body)
## Video Source   : Outdoor flock of 20+ white sheep grazing and walking
## Why thought ok : Sheep has fluffy white wool — expected texture-rich surface for SIFT
## Why it failed  : White wool = low texture + all sheep look identical → cannot track one individual
## Attempts made  : Tried 3 param sets below (all failed)
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

# Attempt 1: standard SIFT    → MIN=10, ratio=0.75, RANSAC=5.0
#   Result: Template keypoints ~30 only. match lines scatter across wrong sheep.
# Attempt 2: sensitive SIFT   → MIN=8,  ratio=0.78, RANSAC=8.0, contrastThreshold=0.02
#   Result: Slightly more keypoints but bounding box jumps between sheep every frame.
# Attempt 3: most aggressive  → MIN=5,  ratio=0.82, RANSAC=12.0, contrastThreshold=0.01
#   Result: Detects "a sheep" but wrong individual every frame — not stable tracking.

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_2.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_2.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_unexpected_2.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.01,   # very sensitive — wool is low contrast
        "edgeThreshold": 30,          # higher — try to catch body outline edges
        "sigma": 1.0,
    },

    "MIN_MATCH_COUNT": 5,            # bare minimum — template has very few keypoints
    "RATIO_TEST": 0.82,              # loosest — still fails
    "RANSAC_THRESHOLD": 12.0,        # very tolerant — non-rigid body movement

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_unexpected",
    "CASE_NUMBER": 2,
    "TARGET_OBJECT": "Single white sheep tracked in a moving flock of 20+ identical sheep",
    "DESCRIPTION": "Unexpected failure: white wool is low-texture + all sheep look identical → SIFT cannot track one individual",
    "FAILURE_ANALYSIS": (
        "White sheep wool appears texture-rich visually but is near-uniform in gradient space. "
        "SIFT relies on local gradient changes — wool has very few stable scale-space extrema. "
        "Three compounding failures: "
        "(1) Low texture: white wool gives <50 template keypoints — far too few for reliable matching. "
        "(2) No unique identity: all sheep in the flock are visually identical — SIFT descriptors "
        "from one sheep match every other sheep equally well, making it impossible to track a specific individual. "
        "(3) Non-rigid deformation: as the sheep walks, its body shape, leg position, and wool "
        "arrangement change continuously — Homography cannot model this non-rigid motion. "
        "Result: bounding box jumps randomly between different sheep each frame. "
        "Would need re-identification features (e.g., ear tag detection, color marking) or "
        "temporal tracking (Kalman filter / optical flow) rather than pure feature matching."
    ),
}

if __name__ == "__main__":
    run_detection(config)
