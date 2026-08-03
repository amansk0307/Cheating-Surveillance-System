import cv2
import torch
from ultralytics import YOLO

# Load YOLOv8 pretrained on COCO
model = YOLO('models/yolov8n.pt')
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def process_mobile_detection(frame):
    results = model(frame, verbose=False)
    mobile_detected = False

    for result in results:
        for box in result.boxes:
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if conf < 0.5 or cls != 67:  # 67 is 'cell phone' in COCO
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"Mobile ({conf:.2f})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            mobile_detected = True

    return frame, mobile_detected