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

list_folder=["foto_dataset\data_11", 
             "foto_dataset\data_18", 
             "foto_dataset\LAWAN DATA 18",
             "foto_dataset\lawan_data_11",
             "foto_dataset\marking putih\\rantai lompat maju\data_5",
             "foto_dataset\marking putih\\rantai lompat maju\data_6",
             "foto_dataset\marking putih\\rantai lompat maju\data_7",
             "foto_dataset\marking putih\\rantai lompat maju\data_8",
             "foto_dataset\marking putih\\rantai ok\data_9",
             "foto_dataset\marking putih\\rantai ok\data_10",
             "foto_dataset\marking putih\\rantai ok\data_11",
             "foto_dataset\marking putih\\rantai ok\data_12",
             "foto_dataset\marking putih\\rantai_lompat mundur\data_1",
             "foto_dataset\marking putih\\rantai_lompat mundur\data_2",
             "foto_dataset\marking putih\\rantai_lompat mundur\data_3",
             "foto_dataset\marking putih\\rantai_lompat mundur\data_4",
             "foto_dataset\oke putih",
             "foto_dataset\\rantai kuning ok"]

# Path folder input dan output
# input_folder = str(input("masukan path folder sumber:"))

for i in range(len(list_folder)):
    output_folder = f"{list_folder[i]}_rotated"
    rotate_images_in_folder(list_folder[i], output_folder)
