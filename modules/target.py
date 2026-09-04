def get_targets(detections, image_width, image_height):
    """
    Convert YOLO bounding boxes into
    camera-relative target positions.
    """

    camera_center_x = image_width / 2
    camera_center_y = image_height / 2

    targets = []

    for i, detection in enumerate(detections):

        x1 = detection["x1"]
        y1 = detection["y1"]
        x2 = detection["x2"]
        y2 = detection["y2"]

        # ---------------------------------------------
        # Weed center
        # ---------------------------------------------

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # ---------------------------------------------
        # Offset from camera center
        # ---------------------------------------------

        offset_x = cx - camera_center_x
        offset_y = cy - camera_center_y

        # ---------------------------------------------
        # Horizontal direction
        # ---------------------------------------------

        if abs(offset_x) < image_width * 0.05:
            horizontal = "CENTER"

        elif offset_x > 0:
            horizontal = "RIGHT"

        else:
            horizontal = "LEFT"

        # ---------------------------------------------
        # Vertical direction
        # ---------------------------------------------

        if abs(offset_y) < image_height * 0.05:
            vertical = "CENTER"

        elif offset_y > 0:
            vertical = "DOWN"

        else:
            vertical = "UP"

        targets.append({
            "weed": i + 1,
            "confidence": detection["confidence"],
            "x1": round(x1, 1),
            "y1": round(y1, 1),
            "x2": round(x2, 1),
            "y2": round(y2, 1),
            "cx": round(cx, 1),
            "cy": round(cy, 1),
            "offset_x": round(offset_x, 1),
            "offset_y": round(offset_y, 1),
            "horizontal": horizontal,
            "vertical": vertical
        })

    return targets