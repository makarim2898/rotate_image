import cv2
import numpy as np

def adjust_brightness_contrast_exposure(image, alpha=1.0, beta=0, gamma=1.0, clarity=1.0):
    """
    Menyesuaikan brightness, contrast, exposure (gamma), dan clarity dari sebuah gambar.
    
    Parameters:
        - image: numpy array, gambar input (BGR)
        - alpha: float, faktor kontras (default 1.0)
        - beta: int, offset brightness (default 0)
        - gamma: float, faktor exposure (default 1.0)
        - clarity: float, faktor kejelasan (default 1.0)
    
    Returns:
        - adjusted: numpy array, gambar yang telah disesuaikan
    """
    # Adjust brightness and contrast
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    # Adjust exposure (gamma correction)
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    adjusted = cv2.LUT(adjusted, table)
    
    # Adjust clarity (sharpening)
    if clarity > 1.0:
        kernel = np.array([[0, -1, 0],
                           [-1, 5 + clarity, -1],
                           [0, -1, 0]])
        adjusted = cv2.filter2D(adjusted, -1, kernel)
    
    return adjusted

def update_image(*args):
    # Dapatkan nilai dari trackbars
    alpha = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10
    beta = cv2.getTrackbarPos('Brightness', 'Adjustments') - 100
    gamma = cv2.getTrackbarPos('Exposure', 'Adjustments') / 10
    clarity = cv2.getTrackbarPos('Clarity', 'Adjustments') / 10
    
    # Terapkan perubahan pada gambar
    adjusted = adjust_brightness_contrast_exposure(original_image, alpha=alpha, beta=beta, gamma=gamma, clarity=clarity)
    
    # Tampilkan gambar hasil
    cv2.imshow('Adjustments', adjusted)

# Baca gambar
image_path = 'foto_dataset/lawan_data_11/lawan_data_11_20241208_110227.png'
original_image = cv2.imread(image_path)
if original_image is None:
    print(f"Gagal membaca gambar dari {image_path}. Pastikan file tersedia.")
    exit()

# Buat jendela
cv2.namedWindow('Adjustments')

# Tambahkan trackbars
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, update_image)  # Default kontras = 1.0
cv2.createTrackbar('Brightness', 'Adjustments', 100, 200, update_image)  # Default kecerahan = 0
cv2.createTrackbar('Exposure', 'Adjustments', 10, 30, update_image)  # Default exposure = 1.0
cv2.createTrackbar('Clarity', 'Adjustments', 10, 30, update_image)  # Default clarity = 1.0

# Tampilkan gambar awal
update_image()

# Tunggu hingga user menekan tombol 'q'
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
