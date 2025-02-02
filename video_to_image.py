import cv2
from ultralytics import YOLO
import os

# Load the YOLOv8 model
model = YOLO(r"C:\Python_projects\ai_oring\ai_oring_app\be-oring-ai\models\model_to_ijiwaru.pt")

# Input video dan folder output
input_video = r".\video oring\video_test\test5.mp4"
output_folder = r".\output_frames\test5"
os.makedirs(output_folder, exist_ok=True)

# Tentukan rentang waktu (detik) untuk menyimpan frame sebagai gambar
start_time = 13  # mulai dari detik ke-5
end_time = 16   # hingga detik ke-10

# Buka video input
cap = cv2.VideoCapture(input_video)
if not cap.isOpened():
    print(f"Error: Tidak dapat membuka video {input_video}")
    exit()

# Ambil properti video
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frame per second
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frame
duration = frame_count / fps  # Durasi total video dalam detik
print(f"Durasi video: {duration:.2f} detik")

# Hitung indeks frame untuk waktu yang ditentukan
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Selesai jika tidak ada frame lagi

    if start_frame <= frame_idx <= end_frame:
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

        # Simpan frame sebagai gambar
        output_path = os.path.join(output_folder, f"frame_{frame_idx}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Frame {frame_idx} disimpan sebagai gambar: {output_path}")

    # Keluar jika frame sudah melewati rentang waktu
    if frame_idx > end_frame:
        break

    frame_idx += 1

# Bersihkan sumber daya
cap.release()
print(f"Proses selesai. Gambar hasil disimpan di folder: {output_folder}")
