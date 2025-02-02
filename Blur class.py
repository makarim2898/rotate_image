# Digunakan untuk membuat class tertentu menjadi blur
#tujuan nya agar antoasi menjadi fokus dan balancing dataset jadi mudah

import cv2
import os
import glob
import numpy as np
from ultralytics import YOLO

def blur_objects(image_path, output_path, model, classes_to_blur):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    
    results = model(image)[0]  # Inferensi dengan YOLOv8
    
    for box in results.boxes.data:
        x1, y1, x2, y2, conf, class_id = box.cpu().numpy()
        class_id = int(class_id)
        
        if class_id in classes_to_blur:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            roi = image[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (45, 45), 0)
            image[y1:y2, x1:x2] = blurred_roi
    
    cv2.imwrite(output_path, image)

def process_folder(image_folder, output_folder, model, classes_to_blur):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print("Reading folder images...")
    image_files = glob.glob(os.path.join(image_folder, "*.jpg"))
    print("Done, Now Blurring images entire folder...")
    for image_file in image_files:
        output_file = os.path.join(output_folder, os.path.basename(image_file))
        blur_objects(image_file, output_file, model, classes_to_blur)
    
    print("Done")
    print(f"Output folder: {output_folder}")

        
# Load model YOLOv8
model = YOLO(r"C:\Python_projects\ai_oring\ai_oring_app\be-oring-ai\models\model_to_ijiwaru.pt")


image_folder = r".\Path source folder"  # Ganti dengan path ke folder gambar
output_folder = rf"{image_folder} Blur"  # Ganti dengan folder output
classes_to_blur = {6,7}  # Set kelas yang ingin diblur

process_folder(image_folder, output_folder, model, classes_to_blur)
