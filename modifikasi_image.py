import cv2
import numpy as np

def update_video(*args):
    global alpha, beta
    alpha = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10
    beta = cv2.getTrackbarPos('Brightness', 'Adjustments')

# Inisialisasi webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Gagal membuka webcam.")
    exit()

# Buat jendela
cv2.namedWindow('Adjustments')

# Tambahkan trackbars
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, update_video)
cv2.createTrackbar('Brightness', 'Adjustments', 50, 100, update_video)

# Default nilai
alpha, beta = 1.0, 50

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    # Sesuaikan frame
    adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    
    # Tampilkan hasil
    cv2.imshow('Adjustments', adjusted)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
