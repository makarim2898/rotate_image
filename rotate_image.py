import cv2
import os

def rotate_images_in_folder(folder_path, output_folder):
    # Buat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterasi melalui semua file di dalam folder
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Pastikan hanya memproses file gambar
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Baca gambar
            image = cv2.imread(filepath)

            # Jika gambar berhasil dibaca
            if image is not None:
                # Rotasi 180 derajat
                rotated_image = cv2.rotate(image, cv2.ROTATE_180)

                # Simpan gambar yang sudah dirotasi ke folder output
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, rotated_image)

                print(f"Berhasil merotasi: {filename}")
            else:
                print(f"Gagal membaca: {filename}")

# Path folder input dan output
input_folder = str(input("masukan path folder sumber:"))
output_folder = f"{input_folder}_output"

rotate_images_in_folder(input_folder, output_folder)
