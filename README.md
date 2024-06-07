# Vision-KRTI-VTOL-2024
Merupakan repository progresan sourcecode dan tutorial singkat ngejalaninnya 

## Objektif dari Vision sesuai kebutuhan seleksi wilayah

- Bisa mendeteksi payload, keranjang, dan jendela lalu mengembalikan parameter yang akan mengatur pergerakan terbang dari drone ( wajib ).  
  Langkah mencapai :
  1. Pengumpulan dataset dari setiap objek/class yang akan dideteksi
  2. Labeling dataset sesuai class
  3. Pembuatan model object detection ( .pt ) menggunakan arsitektur yolov5n atau mobileNet
  4. Pembuatan file detect.py yang akan menjalankan model object detection  
      detect.py harus bisa melakukan 
      - Menjalankan model object detection ( memunculkan boundary box, class, dan confidence )
      - Memperkirakan jarak dengan perhitungan pixel ( memunculkan perkiraan jarak objek dibawah boundary box )
      - mengembalikan parameter yang akan mengatur pergerakan dari drone
  5. Melakukan uji performa dari model dan detect.py pada Jetson Nano  
      hal yang harus disiapkan sebelum bisa uji ke Jetson nano:  
      - Setup environment awal
      - Penginstalan librarary
      - Test kemampuan kamera
  7. Jika perform yang dihasilkan tidak sesuai harapan, kembali ke poin no 3
  8. Jika perform yang dihasilkan tidak sesuai harapan, alhamdulillah dah kelar seharusnya
     
- Bisa menampilkan/livestream tampilan dari camera pada drone ke komputer Ground Stations ( poin plus )
  Langkah mencapai :
  1. Penginstalan dan setup awal penggunaan ssh dan vnc server menggunakan remote.it dan realVNC
  2. Test performa
