import torch
import cv2
import numpy as np


# =========================================================
# LOAD MODEL ONCE
# =========================================================

MODEL_PATH = "../weights/yolov5n/best.pt"

model = torch.hub.load(
    ".",
    "custom",
    path=MODEL_PATH,
    source="local"
)

model.conf = 0.1
model.iou = 0.45


# =========================================================
# DETECTION
# =========================================================

def detect_weeds(image):
    """
    Run YOLOv5 directly on a PIL image.

    Returns:
        output_image
        detections
    """

    # -----------------------------------------------------
    # PIL -> NumPy
    # -----------------------------------------------------

    image_np = np.array(image)

    # PIL image is RGB
    # YOLOv5 accepts RGB through the hub model,
    # so DO NOT convert to BGR here.
    
    # -----------------------------------------------------
    # Run YOLO
    # -----------------------------------------------------

    results = model(
        image_np,
        size=640
    )

    # -----------------------------------------------------
    # Get detections
    # -----------------------------------------------------

    detections = []

    for detection in results.xyxy[0]:

        x1 = float(detection[0])
        y1 = float(detection[1])
        x2 = float(detection[2])
        y2 = float(detection[3])

        confidence = float(detection[4])
        class_id = int(detection[5])

        detections.append({
            "class_id": class_id,
            "confidence": confidence,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        })

    # -----------------------------------------------------
    # Create output image
    # -----------------------------------------------------

    output_image = image_np.copy()

    # -----------------------------------------------------
    # Draw bounding boxes ourselves
    # -----------------------------------------------------

    for detection in detections:

        x1 = int(detection["x1"])
        y1 = int(detection["y1"])
        x2 = int(detection["x2"])
        y2 = int(detection["y2"])

        confidence = detection["confidence"]

        # Bounding box
        cv2.rectangle(
            output_image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3
        )

        # Label
        label = f"Weed {confidence * 100:.1f}%"

        cv2.putText(
            output_image,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    return output_image, detections