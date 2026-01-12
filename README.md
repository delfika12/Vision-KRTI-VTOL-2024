# Vision KRTI VTOL 2024

Repositori ini berisi implementasi sistem Computer Vision untuk divisi VTOL KRTI 2024. Sistem ini menggunakan arsitektur YOLOv5 untuk deteksi objek target dan mengintegrasikan output deteksi ke dalam jaringan komunikasi ROS 1 (Robot Operating System).

## 1. Tujuan
Mengembangkan subsistem visi yang berfungsi untuk:
*   Mendeteksi objek target secara *real-time*.
*   Menentukan posisi relatif objek visual dalam grid 3x3.
*   Mentransmisikan data deteksi ke *Flight Controller* untuk kebutuhan manuver otonom (*tracking* atau *precision landing*).

## 2. Struktur Repositori
*   **`yolov5/`**: Direktori utama framework dan script inferensi.
    *   `detect_best_webcam.py`: Script inferensi untuk kamera tunggal.
    *   `detect_best_dualwebcam.py`: Script inferensi untuk kamera ganda (paralel).
    *   `best-KRTI.pt`: File bobot (*weights*) model hasil pelatihan terbaik.
*   **`train-yolov5.ipynb`**: Jupyter Notebook untuk mempermudah proses pelatihan ulang model.

## 3. Persiapan Lingkungan

1.  **Kloning Repositori:**
    ```bash
    git clone https://github.com/delfika12/Vision-KRTI-VTOL-2024.git
    cd Vision-KRTI-VTOL-2024
    ```

2.  **Instalasi Dependensi:**
    Disarankan menggunakan *virtual environment*.
    ```bash
    pip install -r yolov5/requirements.txt
    ```

3.  **Konfigurasi ROS 1:**
    Pastikan `rospy` dan antarmuka pesan `std_msgs` telah terinstal. Jalankan `roscore` sebelum memulai inferensi.

## 4. Pelatihan Model
Gunakan notebook **`train-yolov5.ipynb`** untuk melatih model dengan dataset baru.
*   **Manajemen Dataset:** Disarankan menggunakan Roboflow untuk *labeling* dan manajemen data.
*   **Format Ekspor:** Pilih format "YOLOv5 PyTorch".
*   **Dokumentasi Teknis:** Rujuk ke [ultralytics/yolov5](https://github.com/ultralytics/yolov5) untuk parameter pelatihan mendalam.

## 5. Menjalankan Kode
Pindah ke direktori kerja:
```bash
cd yolov5
```

### A. Kamera Tunggal (`detect_best_webcam.py`)
```bash
python detect_best_webcam.py --source 0 --weights best-KRTI.pt
```
*   `--source`: ID perangkat kamera (default `0`) atau *path* file video.
*   `--weights`: *Path* model (default `best-KRTI.pt`).

### B. Kamera Ganda (`detect_best_dualwebcam.py`)
Menjalankan inferensi pada dua *stream* kamera secara simultan (misal: kamera depan dan bawah).
```bash
python detect_best_dualwebcam.py --source1 0 --source2 1
```
*   `--source1` / `--source2`: Index perangkat kamera.
*   `--frameskip`: Jumlah *frame* yang dilewati antar proses deteksi untuk optimasi performa CPU (default `3`).

## 6. Integrasi ROS
Data deteksi dipublikasikan ke topik ROS menggunakan tipe pesan `std_msgs/String`.

| Mode | Topik | Format Pesan | Contoh Output |
| :--- | :--- | :--- | :--- |
| **Kamera Tunggal** | `/singlecam` | `"Kelas,Posisi"` | `basket,Top Left` |
| **Kamera Ganda** | `/dualcam` | `"IndexCam,Kelas,Posisi"` | `0,person,Center` |

*   **Posisi**: Menggunakan pembagian grid 3x3 (contoh: *Top Left, Center, Bottom Right*).
*   **IndexCam**: `0` merepresentasikan `--source1`, `1` merepresentasikan `--source2`.

---
*Tim Inti Vision KRTI VTOL 2024*
