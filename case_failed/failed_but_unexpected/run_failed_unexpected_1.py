## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — FAILED BUT UNEXPECTED  #1
## ============================================================
## Target Object  : Small red cosmetic jar (lip balm/cream container) held in hand
## Template Source: Frontal photo of the jar (flat, lid closed, good lighting)
## Video Source   : Person holding jar in hand, lid open, moving slightly
## Why thought ok : Object has distinct red color and textured label — expected SIFT to lock on
## Why it failed  : Curved surface + open lid + small size → Homography assumption violated
## Attempts made  : Tried 3 param sets below (all failed)
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

# ---- ATTEMPT 3 (most aggressive — still failed) ----------------------------
# Attempt 1: standard SIFT   → MIN=10, ratio=0.75, RANSAC=5.0   → match lines scatter across face/background
# Attempt 2: sensitive SIFT  → MIN=8,  ratio=0.78, RANSAC=8.0   → bounding box jitters wildly, not on jar
# Attempt 3: loosest possible→ MIN=6,  ratio=0.82, RANSAC=12.0  → occasionally detects but wrong location

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_1.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_1.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_failed_unexpected_1.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 500,
        "contrastThreshold": 0.01,   # very sensitive — needed to capture jar edge/label
        "edgeThreshold": 30,          # higher — keep curved edge keypoints
        "sigma": 1.0,
    },

    "MIN_MATCH_COUNT": 6,            # reduced to minimum viable
    "RATIO_TEST": 0.82,              # loosest ratio to accept more matches
    "RANSAC_THRESHOLD": 12.0,        # very tolerant — curved surface causes large reprojection error

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "failed_unexpected",
    "CASE_NUMBER": 1,
    "TARGET_OBJECT": "Small red cosmetic jar (lip balm) held in hand, lid open",
    "DESCRIPTION": "Unexpected failure: curved container with open lid violates Homography planarity assumption",
    "FAILURE_ANALYSIS": (
        "The red cosmetic jar appears to have rich texture (label, color contrast) — expected SIFT to detect it. "
        "However, three fundamental issues cause failure: "
        "(1) Curved surface: Homography (H matrix) assumes the object is a flat plane. "
        "A cylindrical/round jar surface introduces non-linear distortion that a 3x3 H cannot model. "
        "(2) Open lid changes object shape: template shows closed jar but video shows open lid — "
        "the visible surface differs significantly from the template, reducing valid matches. "
        "(3) Small object size: jar occupies <80x80 pixels in frame — SIFT struggles to find "
        "stable scale-space extrema at this resolution. "
        "Feature match lines scatter to the person's face and background instead of the jar. "
        "Resolution: would need 3D pose estimation (e.g., PnP + depth camera) or "
        "color-based segmentation to pre-locate the jar before descriptor matching."
    ),
}

if __name__ == "__main__":
    run_detection(config)
