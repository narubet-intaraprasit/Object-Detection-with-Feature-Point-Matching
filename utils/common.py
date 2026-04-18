## CI 7204 Image Processing and Analytics 2/2568
## Challenge 2: Object Detection with Feature Point Matching
## Shared utility — imported by all case scripts

import os
import numpy as np
import cv2

# Colors for each detected instance (BGR)
INSTANCE_COLORS = [
    (0, 255, 0),    # green   — instance 1
    (0, 0, 255),    # red     — instance 2
    (255, 0, 0),    # blue    — instance 3
    (0, 255, 255),  # yellow  — instance 4
    (255, 0, 255),  # magenta — instance 5
]


# ---------------------------------------------------------------------------
# Multi-instance detector: Iterative Homography
# Returns list of dst_pts quads (one per found instance)
# ---------------------------------------------------------------------------
def detect_all_instances(template_kps, template_descs, template_gray,
                         cam_kps, cam_descs, flann, config):
    """
    Iteratively find all instances of the template in the camera frame.
    After each found instance, inlier keypoints are removed so the next
    call to findHomography targets a different location.
    """
    min_match  = config.get("MIN_MATCH_COUNT", 8)
    ratio      = config.get("RATIO_TEST", 0.75)
    ransac_t   = config.get("RANSAC_THRESHOLD", 8.0)
    max_objs   = config.get("MAX_DETECTIONS", 5)

    remaining_kps   = list(cam_kps)
    remaining_descs = cam_descs.copy()

    h_t, w_t = template_gray.shape[:2]
    src_corners = np.float32(
        [[0, 0], [0, h_t - 1], [w_t - 1, h_t - 1], [w_t - 1, 0]]
    ).reshape(-1, 1, 2)

    found_boxes = []  # list of dst_pts quads

    for iteration in range(max_objs):
        if len(remaining_kps) < min_match or remaining_descs is None:
            break

        # Match template against remaining keypoints
        matches = flann.knnMatch(template_descs, remaining_descs, k=2)

        good = []
        for mn in matches:
            if len(mn) == 2:
                m, n = mn[0], mn[1]
                if m.distance < ratio * n.distance:
                    good.append(m)

        if len(good) < min_match:
            break

        t_pts = np.float32(
            [template_kps[m.queryIdx].pt for m in good]
        ).reshape(-1, 1, 2)
        c_pts = np.float32(
            [remaining_kps[m.trainIdx].pt for m in good]
        ).reshape(-1, 1, 2)

        H, mask = cv2.findHomography(t_pts, c_pts, cv2.RANSAC, ransac_t)
        if H is None or mask is None:
            break

        inlier_mask = mask.ravel().astype(bool)
        if inlier_mask.sum() < min_match:
            break

        # Store bounding box for this instance
        dst_corners = cv2.perspectiveTransform(src_corners, H)
        found_boxes.append(dst_corners)

        # Remove inlier keypoints so next iteration finds a different instance
        inlier_train_idx = {
            good[i].trainIdx
            for i in range(len(good))
            if inlier_mask[i]
        }
        keep = [i for i in range(len(remaining_kps)) if i not in inlier_train_idx]

        if not keep:
            break

        remaining_kps   = [remaining_kps[i] for i in keep]
        remaining_descs = remaining_descs[keep]

        print(f"  Instance {iteration + 1} found — "
              f"inliers={inlier_mask.sum()}, remaining_kps={len(remaining_kps)}")

    return found_boxes


# ---------------------------------------------------------------------------
# Helper: overlay fg over bg using a binary mask
# ---------------------------------------------------------------------------
def overlayImage(fg_img, bg_img, fg_maskBinary):
    bg_maskBinary = cv2.bitwise_not(fg_maskBinary)
    merge_fg = cv2.bitwise_and(fg_img, fg_img, mask=fg_maskBinary)
    merge_bg = cv2.bitwise_and(bg_img, bg_img, mask=bg_maskBinary)
    return cv2.bitwise_or(merge_fg, merge_bg)


# ---------------------------------------------------------------------------
# Helper: create feature detector
# ---------------------------------------------------------------------------
def create_detector(choice, sift_params=None):
    if choice == 1:
        params = sift_params or {}
        return cv2.SIFT_create(**params), "SIFT"
    if choice == 2:
        if not hasattr(cv2, "xfeatures2d"):
            print("[ERROR] SURF is not available in this OpenCV build.")
            return None, None
        return cv2.xfeatures2d.SURF_create(), "SURF"
    return cv2.ORB_create(), "ORB"


# ---------------------------------------------------------------------------
# Main detection pipeline
# ---------------------------------------------------------------------------
def run_detection(config):
    template_path     = config["TEMPLATE_PATH"]
    video_path        = config["VIDEO_PATH"]
    output_path       = config["OUTPUT_PATH"]
    feature_choice    = config.get("FEATURE_CHOICE", 1)
    sift_params       = config.get("SIFT_PARAMS", None)
    min_match_count   = config.get("MIN_MATCH_COUNT", 10)
    ratio_test        = config.get("RATIO_TEST", 0.75)
    ransac_threshold  = config.get("RANSAC_THRESHOLD", 5.0)
    wait_ms           = config.get("WAIT_MS", 30)
    draw_choice       = config.get("DRAW_CHOICE", 1)
    case_type         = config.get("CASE_TYPE", "unknown")
    case_number       = config.get("CASE_NUMBER", 0)
    target_object     = config.get("TARGET_OBJECT", "N/A")
    description       = config.get("DESCRIPTION", "N/A")
    failure_analysis  = config.get("FAILURE_ANALYSIS", None)

    # --- Print case summary --------------------------------------------------
    print(f"\n{'='*65}")
    print(f"  CASE : {case_type.upper()} #{case_number}")
    print(f"  TARGET   : {target_object}")
    print(f"  DESC     : {description}")
    print(f"  PARAMS   : MIN_MATCH={min_match_count} | RATIO={ratio_test} | RANSAC={ransac_threshold}")
    if sift_params:
        print(f"  SIFT     : {sift_params}")
    if failure_analysis:
        print(f"  EXPECTED FAILURE: {failure_analysis}")
    print(f"{'='*65}\n")

    # --- Load template -------------------------------------------------------
    template_bgr = cv2.imread(template_path)
    if template_bgr is None:
        print(f"[ERROR] Cannot open template: {template_path}")
        print("        -> Put your template image in the assets/ folder.")
        return
    template_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)

    # --- Load video ----------------------------------------------------------
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        print("        -> Put your video file in the assets/ folder.")
        return

    # --- Create detector & compute template descriptors ----------------------
    detector, detector_name = create_detector(feature_choice, sift_params)
    if detector is None:
        capture.release()
        return

    template_kps, template_descs = detector.detectAndCompute(template_gray, None)
    if template_descs is None or len(template_kps) == 0:
        print("[ERROR] No keypoints found in template image.")
        print("        -> Use a template with richer texture/pattern.")
        capture.release()
        return

    print(f"Template keypoints: {len(template_kps)}")

    # --- FLANN matcher -------------------------------------------------------
    FLANN_INDEX_KDTREE = 0
    FLANN_INDEX_LSH    = 6
    if feature_choice in [1, 2]:
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    else:
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # --- Video writer --------------------------------------------------------
    frame_w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps     = capture.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 20.0

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_w, frame_h))
    if not writer.isOpened():
        print(f"[ERROR] Cannot write output video: {output_path}")
        capture.release()
        return

    print(f"Detector : {detector_name} + FLANN + RANSAC")
    print(f"Output   : {output_path}")
    print("Press ESC to stop early.\n")

    multi_detect = config.get("MULTI_DETECT", False)
    max_detections = config.get("MAX_DETECTIONS", 5)

    frame_count  = 0
    detect_count = 0

    # --- Main processing loop ------------------------------------------------
    while True:
        ret, cam_bgr = capture.read()
        if not ret or cam_bgr is None:
            print("End of video.")
            break

        frame_count += 1
        cam_gray = cv2.cvtColor(cam_bgr, cv2.COLOR_BGR2GRAY)
        cam_kps, cam_descs = detector.detectAndCompute(cam_gray, None)

        homoResult  = cam_bgr.copy()
        goodMatches = []
        matchesMask = None
        detected    = False

        if cam_descs is not None and len(cam_kps) > 0:

            # ================================================================
            # MULTI-DETECT MODE: Iterative Homography
            # ================================================================
            if multi_detect:
                found_boxes = detect_all_instances(
                    template_kps, template_descs, template_gray,
                    cam_kps, cam_descs, flann, config
                )
                for i, dst_pts in enumerate(found_boxes):
                    color = INSTANCE_COLORS[i % len(INSTANCE_COLORS)]
                    homoResult = cv2.polylines(
                        homoResult, [np.int32(dst_pts)],
                        True, color, 2, cv2.LINE_AA
                    )
                    # Label each instance
                    cx = int(dst_pts[:, 0, 0].mean())
                    cy = int(dst_pts[:, 0, 1].mean())
                    cv2.putText(homoResult, f"#{i+1}",
                                (cx - 10, cy), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, color, 2)
                if found_boxes:
                    detected = True
                    detect_count += 1
                status_text  = f"DETECTED {len(found_boxes)} object(s)" if found_boxes \
                               else f"NOT DETECTED (0/{min_match_count})"
                status_color = (0, 255, 0) if found_boxes else (0, 0, 255)

            # ================================================================
            # SINGLE-DETECT MODE: standard pipeline
            # ================================================================
            else:
                matches = flann.knnMatch(template_descs, cam_descs, k=2)
                for mn in matches:
                    if len(mn) == 2:
                        m, n = mn[0], mn[1]
                        if m.distance < ratio_test * n.distance:
                            goodMatches.append(m)

                if len(goodMatches) >= min_match_count:
                    template_pts = np.float32(
                        [template_kps[m.queryIdx].pt for m in goodMatches]
                    ).reshape(-1, 1, 2)
                    cam_pts = np.float32(
                        [cam_kps[m.trainIdx].pt for m in goodMatches]
                    ).reshape(-1, 1, 2)
                    H, mask = cv2.findHomography(
                        template_pts, cam_pts, cv2.RANSAC, ransac_threshold
                    )
                    if H is not None and mask is not None:
                        matchesMask = mask.ravel().tolist()
                        h, w = template_gray.shape[:2]
                        src_pts = np.float32(
                            [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
                        ).reshape(-1, 1, 2)
                        dst_pts = cv2.perspectiveTransform(src_pts, H)
                        if draw_choice in [1, 3]:
                            homoResult = cv2.polylines(
                                homoResult, [np.int32(dst_pts)],
                                True, (0, 255, 0), 2, cv2.LINE_AA
                            )
                        detected = True
                        detect_count += 1

                status_text  = f"DETECTED ({len(goodMatches)} matches)" if detected \
                               else f"NOT DETECTED ({len(goodMatches)}/{min_match_count})"
                status_color = (0, 255, 0) if detected else (0, 0, 255)

        else:
            status_text  = f"NOT DETECTED (no keypoints)"
            status_color = (0, 0, 255)

        # --- Overlay status text on frame ------------------------------------
        cv2.putText(homoResult, status_text,
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        mode_label = "MULTI" if multi_detect else "SINGLE"
        cv2.putText(homoResult,
                    f"{case_type.upper()} #{case_number} | {detector_name}+FLANN+RANSAC [{mode_label}]",
                    (10, frame_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)

        # --- Draw feature matches (single mode only) -------------------------
        win_title = f"{case_type.upper()} #{case_number}"
        cv2.imshow(f"{win_title} - Detection", homoResult)

        if not multi_detect:
            draw_params = dict(
                matchColor=(0, 255, 0),
                singlePointColor=(255, 0, 0),
                matchesMask=matchesMask,
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
            )
            matchResult = cv2.drawMatches(
                template_bgr, template_kps,
                cam_bgr, cam_kps if cam_kps else [],
                goodMatches, None, **draw_params
            )
            cv2.imshow(f"{win_title} - Matches", matchResult)

        writer.write(homoResult)

        if cv2.waitKey(wait_ms) == 27:
            print("ESC pressed — stopping early.")
            break

    # --- Summary -------------------------------------------------------------
    rate = (detect_count / frame_count * 100) if frame_count > 0 else 0.0
    print(f"\n--- Result Summary ---")
    print(f"Total frames   : {frame_count}")
    print(f"Detected frames: {detect_count}  ({rate:.1f}%)")
    print(f"Output saved   : {output_path}")
    if failure_analysis and rate < 30:
        print(f"[ANALYSIS] Detection rate {rate:.1f}% — consistent with expected failure.")
        print(f"           Reason: {failure_analysis}")

    cv2.destroyAllWindows()
    writer.release()
    capture.release()
