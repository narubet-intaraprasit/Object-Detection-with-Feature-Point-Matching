## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2 — SUCCESS / DIFFICULT  #3
## ============================================================
## NOTE: Previous asset (white sheep in flock) was reclassified →
##       moved to case_failed/failed_but_unexpected/ #2
##       Reason: white wool = low texture, all sheep identical → cannot track individual
## ============================================================
## Target Object  : <FILL IN NEW OBJECT>  e.g. "Magazine partially occluded by hand"
## Template Source: <FILL IN>
## Video Source   : <FILL IN>
## Difficulty     : Partial occlusion — part of object hidden
## How solved     : Low MIN_MATCH_COUNT, sensitive SIFT params
## ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from common import run_detection

BASE = os.path.dirname(__file__)

config = {
    "TEMPLATE_PATH": os.path.join(BASE, "assets", "template_3.png"),
    "VIDEO_PATH":    os.path.join(BASE, "assets", "video_3.mp4"),
    "OUTPUT_PATH":   os.path.join(BASE, "output", "output_difficult_3.mp4"),

    "FEATURE_CHOICE": 1,
    "SIFT_PARAMS": {
        "nfeatures": 0,
        "contrastThreshold": 0.02,
        "edgeThreshold": 20,
        "sigma": 1.2,
    },

    "MIN_MATCH_COUNT": 8,            # lower — fewer visible keypoints due to occlusion
    "RATIO_TEST": 0.78,
    "RANSAC_THRESHOLD": 8.0,

    "DRAW_CHOICE": 1,
    "WAIT_MS": 30,

    "CASE_TYPE": "difficult",
    "CASE_NUMBER": 3,
    "TARGET_OBJECT": "FILL_IN",
    "DESCRIPTION": "Difficult: object partially occluded (hand/object blocking part of target)",
}

if __name__ == "__main__":
    run_detection(config)
