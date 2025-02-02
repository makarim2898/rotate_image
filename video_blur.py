import cv2
from ultralytics import YOLO
import os

# Load the YOLOv8 model
model = YOLO(r"C:\Python_projects\ai_oring\ai_oring_app\be-oring-ai\models\model_to_ijiwaru.pt")

# Input dan output file video
input_video = r".\video oring\video_test\test6.mp4"
output_video = r".\output_video\blurred_video_test6.mp4"
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# Buka video input
cap = cv2.VideoCapture(input_video)
if not cap.isOpened():
    print(f"Error: Tidak dapat membuka video {input_video}")
    exit()

# Ambil properti video
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec video output
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Selesai jika tidak ada frame lagi

    # Run YOLOv8 inference
    results = model(frame, conf=0.6, max_det=4)

    # Proses deteksi
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])

            # Blur area jika class termasuk 0-5
            if cls_id in range(6):  # Class 0-5
                roi = frame[y1:y2, x1:x2]
                blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
                frame[y1:y2, x1:x2] = blurred_roi

    # Simpan frame hasil ke video output
    out.write(frame)
    frame_count += 1
    print(f"Proses frame ke-{frame_count}")

# Bersihkan sumber daya
cap.release()
out.release()
print(f"Proses selesai. Video hasil disimpan di: {output_video}")
