import cv2
import numpy as np
import os
from tkinter import filedialog
from tkinter import Tk

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
    global alpha, beta, gamma, clarity
    alpha = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10
    beta = cv2.getTrackbarPos('Brightness', 'Adjustments') - 100
    gamma = cv2.getTrackbarPos('Exposure', 'Adjustments') / 10
    clarity = cv2.getTrackbarPos('Clarity', 'Adjustments') / 10
    
    # Terapkan perubahan pada gambar
    adjusted = adjust_brightness_contrast_exposure(original_image, alpha=alpha, beta=beta, gamma=gamma, clarity=clarity)
    
    # Gabungkan gambar asli dan gambar yang disesuaikan menjadi satu
    combined = np.hstack((original_image, adjusted))  # Menyusun gambar secara horizontal
    
    # Tampilkan gambar gabungan dalam satu jendela
    cv2.imshow('Adjustments', combined)

def save_edited_images(input_folder, output_folder, alpha, beta, gamma, clarity):
    """
    Menyimpan gambar yang sudah disesuaikan dari folder input ke folder output dengan nama baru.
    
    Parameters:
        - input_folder: Path folder tempat gambar input berada
        - output_folder: Path folder tempat gambar hasil edit disimpan
        - alpha, beta, gamma, clarity: Parameter untuk pengeditan gambar
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Membuat folder output jika belum ada

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Baca gambar
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            # Edit gambar
            adjusted_image = adjust_brightness_contrast_exposure(image, alpha=alpha, beta=beta, gamma=gamma, clarity=clarity)
            
            # Buat nama file baru dengan tambahan parameter edit
            file_name, file_extension = os.path.splitext(filename)
            new_filename = f"{file_name}_contrast{alpha}_brightness{beta}_exposure{gamma}_clarity{clarity}{file_extension}"
            new_image_path = os.path.join(output_folder, new_filename)
            
            # Simpan gambar yang sudah disesuaikan
            cv2.imwrite(new_image_path, adjusted_image)
            print(f"Saved edited image: {new_image_path}")

# Baca gambar pertama (untuk menampilkan gambar asli)
image_path = 'foto_dataset/lawan_data_11/lawan_data_11_20241208_110227.png'
original_image = cv2.imread(image_path)
if original_image is None:
    print(f"Gagal membaca gambar dari {image_path}. Pastikan file tersedia.")
    exit()

# Buat jendela untuk penyesuaian gambar
cv2.namedWindow('Adjustments')

# Tambahkan trackbars
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, update_image)  # Default kontras = 1.0
cv2.createTrackbar('Brightness', 'Adjustments', 100, 200, update_image)  # Default kecerahan = 0
cv2.createTrackbar('Exposure', 'Adjustments', 10, 30, update_image)  # Default exposure = 1.0
cv2.createTrackbar('Clarity', 'Adjustments', 10, 30, update_image)  # Default clarity = 1.0

# Tampilkan gambar awal dan terapkan update pertama
update_image()

# Tunggu hingga user menekan tombol 's' untuk menyimpan gambar atau tombol 'q' untuk keluar
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Pilih folder input dan output
        root = Tk()
        root.withdraw()  # Hide the root window
        
        input_folder = filedialog.askdirectory(title="Pilih Folder Gambar Input")
        if input_folder:
            output_folder = filedialog.askdirectory(title="Pilih Folder untuk Menyimpan Hasil")
            if output_folder:
                save_edited_images(input_folder, output_folder, alpha, beta, gamma, clarity)
            else:
                print("Folder output tidak dipilih.")
        else:
            print("Folder input tidak dipilih.")
        
        break

cv2.destroyAllWindows()
