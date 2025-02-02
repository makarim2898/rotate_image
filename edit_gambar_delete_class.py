import cv2
from ultralytics import YOLO
import os

# Load the YOLOv8 model
model = YOLO(r"C:\Python_projects\ai_oring\ai_oring_app\be-oring-ai\models\model_to_ijiwaru.pt")

# Folder input dan output
input_folder = r"D:\python_environtment\dataset\foto_dataset\1.Filtered_dataset\5. W_RANTAI_NG_MAJU_ORING_OK"
output_folder = r".\blurred_ng_image"
os.makedirs(output_folder, exist_ok=True)

countj = 0
print(input_folder)
print(os.listdir(input_folder))
# Proses setiap gambar dalam folder input
for filename in os.listdir(input_folder):
    print("dah masuk for")
    input_path = os.path.join(input_folder, filename)
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue  # Skip non-image files

    # Baca gambar
    frame = cv2.imread(input_path)

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
                blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)
                frame[y1:y2, x1:x2] = blurred_roi

    # Simpan gambar hasil
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, frame)
    countj += 1

print(f"Proses selesai. Gambar hasil disimpan di folder: {output_folder} jumlah {countj}")
