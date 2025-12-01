from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO

# ABSOLUTE PROJECT PATHS
ROOT = Path(r"C:\src\traffic-digital-twin")
VIDEO_PATH = ROOT / "data" / "traffic_video.mp4"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)
CSV_PATH = OUTPUTS_DIR / "yolo_detections.csv"

MODEL_NAME = "yolov8n.pt"
VEHICLE_CLASSES = {"car", "bus", "truck", "motorbike"}

def load_model():
    return YOLO(MODEL_NAME)

def main():
    print("VIDEO_PATH:", VIDEO_PATH)
    print("VIDEO_EXISTS?:", VIDEO_PATH.exists())

    if not VIDEO_PATH.exists():
        raise FileNotFoundError(f"VIDEO NOT FOUND at {VIDEO_PATH}")

    model = load_model()
    cap = cv2.VideoCapture(str(VIDEO_PATH))

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0
    frame_idx = 0
    records = []

    print(f"[INFO] Processing video at {fps:.2f} FPS...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)[0]

        vehicle_count = 0
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = results.names[cls_id]
            if cls_name in VEHICLE_CLASSES:
                vehicle_count += 1

        t = frame_idx / fps
        records.append({
            "frame": frame_idx,
            "time_sec": t,
            "vehicle_count": vehicle_count
        })

        frame_idx += 1
        if frame_idx % 50 == 0:
            print(f"[INFO] Processed {frame_idx} frames...")

    cap.release()

    df = pd.DataFrame(records)
    df.to_csv(CSV_PATH, index=False)
    print(f"[DONE] Saved YOLO detections to {CSV_PATH}")

if __name__ == "__main__":
    main()
