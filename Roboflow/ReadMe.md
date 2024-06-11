# DATASET ROBOFLOW

Roboflow adalah web yang digunakan untuk membuat dan labelling dataset untuk object detection, bisa dengan framing video ataupun foto satu-satu.
Labelling digunakan untuk memberi spesifikasi pada foto, bagian apa pada foto yang ingin difokuskan dan dipelajari oleh mesin.

## STEPS

### Pra roboflow, mengambil video/data yang ingin diolah:

1. Setelah menentukan barang yang ingin dideteksi, rekam video dengan fokus angle dari objek yang ingin di detect (misalkan mau deteksi bagian atas dari objek, maka fokuskan video ke bagian atas objek).
2. Meskipun terfokus pada satu titik, coba untuk mendapatkan video dari sudut yang berbeda-beda (misal dari atas tapi agak miring).
3. Ambil beberapa video dengan latar yang berbeda

### In roboflow:

#### Framing
1. Buat akun roboflow dan ikuti semua proses pembuatan workspace
2. Dalam "Upload Data" masukkan video-video yang diambil, Roboflow akan "frame video" (mengambil foto setiap berapa frame)
3. Setelah video di-frame, bisa "assign" jumlah foto yang akan di labelling kepada rekan (berbagi tugas)

#### Labelling
1. Dalam "Annotate" mulai anotasi / labelling dataset yang telah diinput
2. Gunakan bounding box tool untuk menspesifikasi pada gambar objek deteksi, bisa menggunakan polygon tool tetapi lebih lama dan detil
3. Tentukan nama label yang ingin ditetapkan, nama label disamakan untuk semua objek yang sama
4. Lakukan pada seluruh foto dalam dataset
5. Semua dataset yang telah di-labelling bisa dilihat dalam "Dataset" di sebelah kiri

#### Exporting
1. Dalam "Generate" klik "Create new version", scroll ke bawah dan klik "create" pada "create"
2. Dataset yang telah dilabelling akan digunakan untuk membuat "version" baru, jika ingin menambahkan dataset bisa membuat "version" baru lagi
3. Klik "Export dataset" di sebelah kanan atas dan centang "download zip to computer" untuk mendapatkan export dataset

