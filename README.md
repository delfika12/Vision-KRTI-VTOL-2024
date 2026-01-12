# Vision KRTI VTOL 2024

Repository ini berisi sistem Computer Vision untuk tim VTOL di KRTI 2024. Kita pakai YOLOv5 yang telah dimodifikasi supaya bisa deteksi objek target (payload, basket, dll) dan memberikan informasi posisinya ke sistem navigasi (ROS 1).

## 1. Tujuan
Intinya, repo ini dibuat supaya drone bisa:
*   Mendeteksi objek target secara real-time.
*   Mengetahui posisi objek secara visual (apakah di Kanan Atas, Tengah, Kiri Bawah, dsb).
*   Mengirim data tersebut ke Flight Controller lewat ROS agar drone bisa melakukan manuver otomatis (tracking atau precision landing).

## 2. Isi Repository
Berikut file-file penting yang sering dipakai:
*   **`yolov5/`**: Folder utama. Di sini tersimpan framework YOLOv5 dan script deteksi custom kita.
    *   `detect_best_webcam.py`: Script untuk menjalankan deteksi menggunakan 1 kamera.
    *   `detect_best_dualwebcam.py`: Script untuk menjalankan 2 kamera sekaligus (misal: kamera depan + kamera bawah).
    *   `best-KRTI.pt`: File model (weights) terbaik yang siap pakai.
*   **`train-yolov5.ipynb`**: Notebook untuk melatih model. Kalau mau training ulang pakai dataset baru, pakai ini aja prosesnya lebih mudah dipantau.

## 3. Setup Environment
Biar programnya jalan lancar, siapkan dulu hal berikut:

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/delfika12/Vision-KRTI-VTOL-2024.git
    cd Vision-KRTI-VTOL-2024
    ```

2.  **Install Dependencies:**
    Sangat disarankan pakai virtual environment (seperti conda atau venv).
    ```bash
    pip install -r yolov5/requirements.txt
    ```

3.  **Sistem ROS 1:**
    Pastikan `rospy` dan `std_msgs` sudah terinstall (biasanya sudah ada kalau install `ros-noetic-desktop-full`). Jangan lupa jalankan `roscore` di terminal terpisah sebelum run program deteksinya.

## 4. Cara Training Model
Kalau butuh update model atau nambah dataset:
1.  Buka file **`train-yolov5.ipynb`**. Notebook ini berisi panduan step-by-step dari setup sampai export model `.pt`.
2.  **Dataset:** Kita rekomendasikan pakai **Roboflow** untuk labeling gambar.
    *   Saat export dataset, pilih format **"YOLOv5 PyTorch"**.
    *   Referensi repo resmi untuk detail teknis: [ultralytics/yolov5](https://github.com/ultralytics/yolov5).

## 5. Cara Menjalankan Program
Masuk dulu ke direktori `yolov5`:
```bash
cd yolov5
```

### A. Pakai 1 Kamera (`detect_best_webcam.py`)
```bash
python detect_best_webcam.py --source 0 --weights best-KRTI.pt
```
*   `--source`: ID kamera (default `0`), bisa juga diganti path video.
*   `--weights`: Path ke file model (default `best-KRTI.pt`).

### B. Pakai 2 Kamera (`detect_best_dualwebcam.py`)
Gunakan ini jika drone memakai kamera depan (navigasi) dan kamera bawah (dropping) secara bersamaan.
```bash
python detect_best_dualwebcam.py --source1 0 --source2 1
```
*   `--source1` & `--source2`: Index kamera yang terdeteksi di OS.
*   `--frameskip`: Default `3`. Ini fungsinya untuk melompati beberapa frame agar beban CPU tidak terlalu berat saat memproses 2 kamera sekaligus.

## 6. Integrasi ke ROS
Data hasil deteksi akan otomatis dikirim ke topic ROS. Format datanya dibuat string sederhana (CSV-like) agar mudah di-parsing di sisi Flight Controller.

| Program | Nama Topic | Format Data | Contoh Data |
| :--- | :--- | :--- | :--- |
| **Satu Kamera** | `/singlecam` | `"NamaKelas,Posisi"` | `basket,Top Left` |
| **Dua Kamera** | `/dualcam` | `"IndexCam,NamaKelas,Posisi"` | `0,person,Center` |

*   **Posisi**: Menggunakan grid 3x3 (Top Left, Top Center, Top Right, ... , Bottom Right).
*   **IndexCam**: `0` mengacu pada kamera `source1`, dan `1` mengacu pada kamera `source2`.

---
*Tim Vision KRTI VTOL 2024*
