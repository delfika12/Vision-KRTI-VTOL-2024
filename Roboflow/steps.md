# DATASET ROBOFLOW

Roboflow adalah web yang digunakan untuk membuat dan labelling dataset untuk object detection, bisa dengan framing video ataupun foto satu-satu.
Labelling digunakan untuk memberi spesifikasi pada foto, bagian apa pada foto yang ingin difokuskan dan dipelajari oleh mesin.

## STEPS

### Pra roboflow, mengambil video/data yang ingin diolah:

1. Setelah menentukan barang yang ingin dideteksi, rekam video dengan fokus angle dari objek yang ingin di detect (misalkan mau deteksi bagian atas dari objek, maka fokuskan video ke bagian atas objek).
2. Meskipun terfokus pada satu titik, coba untuk mendapatkan video dari sudut yang berbeda-beda (misal dari atas tapi agak miring).
3. Ambil beberapa video dengan latar yang berbeda
![Screenshot 2024-06-11 100427](https://github.com/rdanenn/Roboflow/assets/172345163/91259cc5-2f76-4620-9959-9f4924a39df3)
![Screenshot 2024-06-11 110946](https://github.com/rdanenn/Roboflow/assets/172345163/849b95c2-c8cd-4fff-b9d7-538d3b7149e5)


### In roboflow:

#### Framing
1. Buat akun roboflow dan ikuti semua proses pembuatan workspace
2. Dalam "Upload Data" masukkan video-video yang diambil, Roboflow akan "frame video" (mengambil foto setiap berapa frame)
3. Setelah video di-frame, bisa "assign" jumlah foto yang akan di labelling kepada rekan (berbagi tugas)
![Screenshot 2024-06-11 111445](https://github.com/rdanenn/Roboflow/assets/172345163/0d81dea4-f621-4c53-9901-e464c94b3c1b)


#### Labelling
1. Dalam "Annotate" mulai anotasi / labelling dataset yang telah diinput
2. Gunakan bounding box tool untuk menspesifikasi pada gambar objek deteksi, bisa menggunakan polygon tool tetapi lebih lama dan detil
3. Tentukan nama label yang ingin ditetapkan, nama label disamakan untuk semua objek yang sama
4. Lakukan pada seluruh foto dalam dataset
5. Semua dataset yang telah di-labelling bisa dilihat dalam "Dataset" di sebelah kiri
![Screenshot 2024-06-11 110630](https://github.com/rdanenn/Roboflow/assets/172345163/9adde646-d378-4abf-b91d-367145c0e14f)


#### Exporting
1. Dalam "Generate" klik "Create new version", scroll ke bawah dan klik "create" pada "create"
2. Dataset yang telah dilabelling akan digunakan untuk membuat "version" baru, jika ingin menambahkan dataset bisa membuat "version" baru lagi
3. Klik "Export dataset" di sebelah kanan atas dan centang "download zip to computer" untuk mendapatkan export dataset
![Screenshot 2024-06-11 111552](https://github.com/rdanenn/Roboflow/assets/172345163/cc86e1f1-afec-4bb7-928e-aa89839c6a62)
