# 🌋 Volcano Monitoring System
### Sistem Monitoring Gunung Api Berbasis Machine Learning untuk Klasifikasi dan Deteksi Anomali

<p align="center">
  <strong>Proyek Kerja Praktik — Pusat Vulkanologi dan Mitigasi Bencana Geologi (PVMBG)</strong>
</p>


## 📌 Tentang Proyek

**Volcano Monitoring System** merupakan sistem monitoring gunung api berbasis *Machine Learning* yang dikembangkan dalam kegiatan kerja praktik di **Pusat Vulkanologi dan Mitigasi Bencana Geologi (PVMBG)** dibawah supervisi Dr. Devy Kamil Syahbana. Sistem ini dirancang untuk membantu analisis citra CCTV gunung api melalui pendekatan pengolahan citra dan pembelajaran mesin.

Pemantauan gunung api menghasilkan banyak citra CCTV yang perlu diamati untuk mengetahui kondisi visual gunung. Pengolahan citra secara otomatis dapat membantu mengelompokkan kondisi yang terlihat pada gambar dan menandai citra yang memiliki karakteristik berbeda dari kelompok data pada umumnya.

Proyek ini menerapkan dua pendekatan sesuai karakteristik data yang digunakan:

1. **Supervised Learning pada Gunung Lewotolok**, menggunakan arsitektur ResNet50 untuk mengklasifikasikan citra CCTV ke dalam empat kategori kondisi visual.
2. **Unsupervised Learning pada Gunung Tangkuban Perahu**, menggunakan MobileNetV2 sebagai ekstraktor fitur dan K-Means untuk mengelompokkan citra serta mengidentifikasi kandidat anomali berdasarkan jarak terhadap centroid cluster.

Hasil analisis ditampilkan melalui aplikasi web sehingga pengguna dapat melihat ringkasan hasil pemrosesan, klasifikasi citra, kandidat anomali, riwayat, dan informasi sistem dalam satu antarmuka.

> **Catatan:** Sistem ini merupakan alat bantu analisis citra CCTV. Hasil klasifikasi dan kandidat anomali tidak menggantikan interpretasi petugas, verifikasi lapangan, maupun penetapan status aktivitas gunung api oleh pihak berwenang.

## 🎯 Tujuan Proyek

- Mengembangkan sistem monitoring berbasis web untuk menampilkan hasil analisis citra CCTV gunung api.
- Menerapkan *supervised learning* untuk mengklasifikasikan kondisi visual citra CCTV Gunung Lewotolok.
- Menerapkan *unsupervised learning* untuk mengelompokkan citra CCTV Gunung Tangkuban Perahu.
- Mengidentifikasi kandidat anomali berdasarkan karakteristik fitur citra dan jaraknya terhadap pusat cluster.
- Mengintegrasikan model *Machine Learning* dengan aplikasi web agar hasil pemrosesan lebih mudah diakses dan dipahami.
- Melakukan pengujian terhadap performa model serta mendokumentasikan hasil dan keterbatasannya.

## ✨ Fitur Utama

### 1. Dashboard

Dashboard menjadi halaman utama untuk menampilkan ringkasan sistem monitoring dan menyediakan akses ke fitur-fitur yang tersedia.

### 2. Klasifikasi CCTV Gunung Lewotolok

Fitur ini menggunakan model ResNet50 yang dilatih dengan pendekatan *supervised learning*. Model mempelajari pola visual berdasarkan citra yang telah diberi label, kemudian memprediksi kategori kondisi visual untuk citra yang dianalisis.

Empat kategori yang digunakan adalah:

| Label | Keterangan |
|---|---|
| `Tenang` | Citra yang dikategorikan ke dalam kondisi visual tenang berdasarkan data pelatihan. |
| `Asap Putih` | Citra yang menunjukkan karakteristik visual asap putih. |
| `Erupsi/Awan Kelabu` | Citra dengan karakteristik visual yang dikelompokkan ke dalam kategori erupsi/awan kelabu. |
| `Tertutup Awan` | Citra ketika area gunung tertutup awan sehingga kondisi visualnya terbatas. |

Kategori tersebut merupakan label klasifikasi visual dalam dataset, bukan penetapan status resmi aktivitas gunung api.

### 3. Pengelompokan dan Deteksi Kandidat Anomali Gunung Tangkuban Perahu

Fitur ini menggunakan pendekatan *unsupervised learning*, sehingga proses pengelompokan dilakukan tanpa label kelas yang telah ditentukan sebelumnya.

MobileNetV2 digunakan untuk mengekstraksi fitur visual citra, kemudian K-Means mengelompokkan fitur tersebut berdasarkan kemiripannya. Jarak citra terhadap centroid cluster digunakan sebagai *anomaly score* untuk membantu mengidentifikasi citra yang berbeda dari pola kelompok data.

Hasilnya dibedakan menjadi:
- **Normal:** citra yang tidak melewati ambang batas skor anomali.
- **Kandidat Anomali:** citra yang skor anomalinya melewati ambang batas yang ditentukan.

Kandidat anomali tidak secara otomatis berarti terjadi erupsi. Citra tersebut memerlukan pemeriksaan dan interpretasi lebih lanjut.

### 4. Riwayat

Halaman riwayat digunakan untuk membantu pengguna melihat catatan hasil pemrosesan yang tersedia di dalam aplikasi.

### 5. Informasi Sistem

Halaman informasi menyajikan informasi pendukung mengenai sistem monitoring yang dikembangkan.

## 🖥️ Dokumentasi Tampilan Aplikasi

Bagian ini menampilkan dokumentasi antarmuka aplikasi. Gambar akan muncul setelah file gambar diunggah ke repository sesuai struktur folder yang digunakan.

### Dashboard

<img width="827" height="395" alt="image" src="https://github.com/user-attachments/assets/4f8477a5-5fd1-449c-a98d-5fab9f54cdd5" />


### Halaman Klasifikasi Lewotolok

<img width="827" height="397" alt="image" src="https://github.com/user-attachments/assets/ac57c4db-7711-453d-9ff7-c5885129cda3" />


### Halaman Tangkuban Perahu

<img width="827" height="396" alt="image" src="https://github.com/user-attachments/assets/d7178b04-6ce1-4dcb-b7c3-7e09045d49fe" />


### Halaman Riwayat

<img width="827" height="395" alt="image" src="https://github.com/user-attachments/assets/b635b661-4f74-4b00-ba5d-549d7a073b1a" />


### Halaman Informasi

<img width="827" height="394" alt="image" src="https://github.com/user-attachments/assets/34eb0dd1-4597-4e77-a02a-ab35f6b7eb66" />


## 🧠 Metode dan Teknologi Machine Learning

### A. Supervised Learning — ResNet50

ResNet50 merupakan arsitektur *Convolutional Neural Network* (CNN) yang digunakan untuk mempelajari fitur visual dari citra. Model yang digunakan dalam proyek ini memanfaatkan bobot awal dari ImageNet dan dilanjutkan dengan proses *fine-tuning* agar model dapat menyesuaikan representasi fiturnya dengan karakteristik citra CCTV Gunung Lewotolok.

Tahapan umum klasifikasi meliputi:

1. Menyiapkan dataset citra dan label kelas.
2. Melakukan pembagian data menjadi data pelatihan, validasi, dan pengujian.
3. Melakukan penyeimbangan kelas pada data pelatihan menggunakan *oversampling*.
4. Menyesuaikan model ResNet50 melalui proses pelatihan dan *fine-tuning*.
5. Mengevaluasi model menggunakan data pengujian.
6. Mengintegrasikan model terpilih ke dalam sistem monitoring.

### B. Unsupervised Learning — MobileNetV2 dan K-Means

MobileNetV2 digunakan untuk mengekstraksi fitur dari citra CCTV Gunung Tangkuban Perahu menjadi representasi numerik berdimensi 1.280. Representasi tersebut kemudian digunakan sebagai masukan bagi algoritma K-Means.

K-Means mengelompokkan data berdasarkan kedekatan fitur terhadap centroid. Jumlah cluster dievaluasi menggunakan beberapa alternatif nilai K, kemudian kualitas pemisahan cluster dibandingkan menggunakan *Silhouette Score*.

Untuk mendeteksi kandidat anomali, sistem menghitung jarak fitur citra terhadap centroid terdekat. Ambang batas ditentukan menggunakan persentil ke-95 dari skor anomali. Citra yang melampaui ambang batas tersebut ditandai sebagai kandidat anomali untuk ditinjau lebih lanjut.

### Perbedaan Kedua Pendekatan

| Aspek | Lewotolok | Tangkuban Perahu |
|---|---|---|
| Pendekatan | Supervised Learning | Unsupervised Learning |
| Metode utama | ResNet50 | MobileNetV2 + K-Means |
| Label kelas | Empat kelas yang telah ditentukan | Tidak memerlukan label kelas awal |
| Tujuan | Klasifikasi kondisi visual | Pengelompokan citra dan identifikasi kandidat anomali |
| Evaluasi utama | Accuracy, loss, dan F1-score | Silhouette Score dan analisis skor anomali |

## 📊 Hasil Pengujian

### A. Hasil Klasifikasi Gunung Lewotolok

Berdasarkan hasil pengujian pada laporan kerja praktik, model ResNet50 memperoleh hasil berikut:

| Metrik | Hasil |
|---|---:|
| Jumlah citra dataset | 10.850 |
| Jumlah citra pengujian | 1.434 |
| Test Accuracy | **85,98%** |
| Test Loss | 0,4329 |
| Macro F1-score | 0,8424 |
| Weighted F1-score | 0,8602 |
| Durasi pelatihan | 72,90 menit |
| Epoch pelatihan | 16 |

Dataset dibagi dengan proporsi 70% data pelatihan, 15% data validasi, dan 15% data pengujian menggunakan pembagian berdasarkan kelompok tanggal/sesi. Proses *oversampling* diterapkan hanya pada data pelatihan untuk membantu mengatasi ketidakseimbangan jumlah sampel antar kelas.

Hasil pengujian menunjukkan bahwa model dapat mengklasifikasikan citra berdasarkan empat kategori visual yang ditentukan. Nilai akurasi perlu dibaca bersama metrik lainnya, khususnya F1-score, untuk mendapatkan gambaran performa yang lebih menyeluruh.

<img width="646" height="303" alt="image" src="https://github.com/user-attachments/assets/694ba6a0-c83e-408b-81f1-b2329c4c0934" />


### B. Hasil Pengelompokan dan Deteksi Kandidat Anomali Tangkuban Perahu

Hasil eksperimen *unsupervised learning* yang tercatat dalam laporan adalah sebagai berikut:

| Metrik | Hasil |
|---|---:|
| Jumlah citra valid | 9.906 |
| Ekstraktor fitur | MobileNetV2 |
| Dimensi fitur | 1.280 |
| Jumlah cluster terpilih | 3 |
| Silhouette Score | 0,210797 |
| Ambang batas anomali (persentil ke-95) | 15,792045 |
| Citra normal | 9.410 |
| Kandidat anomali | 496 |

Nilai *Silhouette Score* digunakan untuk membantu mengevaluasi kualitas pengelompokan. Sementara itu, ambang batas persentil ke-95 digunakan untuk menandai citra dengan skor jarak yang relatif tinggi terhadap centroid terdekat.

Hasil tersebut merupakan hasil analisis terhadap dataset yang digunakan. Kategori kandidat anomali tidak dapat langsung diartikan sebagai erupsi atau kondisi berbahaya tanpa pemeriksaan lebih lanjut.

![Distribusi cluster Tangkuban Perahu]
<img width="549" height="470" alt="image" src="https://github.com/user-attachments/assets/62b1c06e-31ac-4c6d-898a-7b3c243ce7a1" />
<img width="549" height="470" alt="image" src="https://github.com/user-attachments/assets/d99974fd-9d7b-4241-b0d5-c65125b3d491" />
<img width="549" height="470" alt="image" src="https://github.com/user-attachments/assets/15d3f8bd-4643-43a3-a0ba-5d423b896919" />

![Visualisasi deteksi kandidat anomali Tangkuban Perahu]
<img width="615" height="730" alt="image" src="https://github.com/user-attachments/assets/221cb7e7-246a-489c-88f9-bb60ef074655" />


## 🏗️ Arsitektur Sistem

Secara umum, sistem terdiri dari beberapa komponen yang saling terhubung:

1. **Dataset CCTV:** menyediakan citra yang digunakan dalam proses analisis.
2. **Pemrosesan citra:** menyiapkan citra sebagai masukan model.
3. **Model Machine Learning:** menjalankan klasifikasi atau pengelompokan berdasarkan pendekatan yang digunakan.
4. **Backend Flask:** menangani logika aplikasi dan integrasi pemrosesan.
5. **Database PostgreSQL:** mendukung penyimpanan data aplikasi sesuai implementasinya.
6. **Frontend web:** menampilkan dashboard, hasil analisis, riwayat, dan informasi sistem.

Alur umum pemrosesan:

```text
              DATA CITRA CCTV
                     |
                     v
             PEMROSESAN CITRA
                     |
          +----------+----------+
          |                     |
          v                     v
    GUNUNG LEWOTOK            GUNUNG
    SUPERVISED             TANGKUBAN PERAHU
          |                     |
          v                     v
       ResNet50              MobileNetV2
          |                     |
          v                     v
    Klasifikasi 4 kelas      Ekstraksi fitur
                                |
                                v
                              K-Means
                                |
                                v
                       Skor kandidat anomali
          |                     |
          +----------+----------+
                     |
                     v
              BACKEND FLASK
                     |
           +---------+---------+
           |                   |
           v                   v
       PostgreSQL          FRONTEND WEB
                               |
                               v
                       HASIL ANALISIS
```

Diagram di atas menggambarkan alur konseptual sistem, bukan representasi detail seluruh implementasi kode.

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama untuk pemrosesan dan integrasi sistem. |
| Flask | Framework backend untuk aplikasi web. |
| TensorFlow / Keras | Pengembangan, pelatihan, dan pemuatan model deep learning. |
| ResNet50 | Klasifikasi citra CCTV Gunung Lewotolok. |
| MobileNetV2 | Ekstraksi fitur visual citra Gunung Tangkuban Perahu. |
| Scikit-learn | Implementasi K-Means dan evaluasi pengelompokan. |
| OpenCV dan Pillow | Mendukung pemrosesan citra. |
| NumPy dan Pandas | Pengolahan data numerik dan tabular. |
| Matplotlib / Seaborn | Visualisasi dan analisis hasil eksperimen. |
| Joblib | Mendukung penyimpanan atau pemuatan objek model yang kompatibel. |
| PostgreSQL | Database aplikasi. |
| HTML, CSS, JavaScript | Pengembangan antarmuka web. |
| Google Colab dan Google Drive | Lingkungan eksperimen dan penyimpanan data selama pengembangan. |

## 📁 Struktur Repository

Struktur berikut merupakan contoh susunan repository yang dapat disesuaikan dengan file proyek yang benar-benar tersedia.

```text
volcano_monitoring/
│
├── README.md
├── app.py
├── requirements.txt
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   │   └── ...
│   ├── js/
│   │   └── ...
│   └── images/
│       └── ...
│
├── models/
│   ├── lewotolok/
│   │   └── ...
│   └── tangkuban/
│       └── ...
│
├── docs/
│   └── images/
│       ├── dashboard.jpg
│       ├── halaman_lewotolok.jpg
│       ├── halaman_tangkuban.jpg
│       ├── halaman_riwayat.jpg
│       ├── halaman_info.jpg
│       ├── resnet50_performance.jpg
│       ├── tangkuban_cluster_distribution.jpg
│       └── tangkuban_anomaly_detection.jpg
│
└── ...
```

**Penting:** nama file dan folder di atas merupakan contoh dokumentasi. Sesuaikan dengan struktur proyek yang sebenarnya. Jangan membuat `app.py` atau `requirements.txt` baru apabila proyekmu menggunakan nama atau mekanisme yang berbeda.

## ⚙️ Menjalankan Aplikasi

Petunjuk berikut merupakan gambaran umum. Perintah dan konfigurasi akhir perlu disesuaikan dengan struktur source code serta dependensi proyek.

### 1. Clone Repository

```bash
git clone https://github.com/samsa12345/PVMBG_Projek_KP.git
cd PVMBG_Projek_KP
```

### 2. Buat Virtual Environment

```bash
python -m venv venv_env
```

Aktifkan lingkungan virtual di Windows:

```bash
venv_env\Scripts\activate
```

### 3. Instal Dependensi

Apabila repository menyediakan file `requirements.txt`, jalankan:

```bash
pip install -r requirements.txt
```

Jika file tersebut belum tersedia, dependensi perlu disusun berdasarkan library yang benar-benar digunakan oleh source code.

### 4. Siapkan Konfigurasi

Pastikan konfigurasi database, lokasi model, dataset, dan variabel lingkungan sudah sesuai dengan lingkungan yang digunakan. Jangan mengunggah kata sandi database, API key, atau informasi rahasia lainnya ke repository publik.

### 5. Jalankan Aplikasi

Jalankan perintah sesuai entry point aplikasi yang digunakan. Contohnya, apabila aplikasi memang menggunakan `app.py`:

```bash
.\venv\Scripts\python.exe app.py
```

Perintah tersebut hanya berlaku jika `app.py` merupakan entry point yang benar pada proyek.

## ⚠️ Keterbatasan Sistem

- Hasil klasifikasi bergantung pada kualitas, variasi, dan representasi data pelatihan.
- Perubahan pencahayaan, cuaca, kabut, sudut pandang, dan kualitas citra CCTV dapat memengaruhi karakteristik visual.
- Ketidakseimbangan kelas dapat memengaruhi performa model pada kategori yang memiliki sampel lebih sedikit.
- *Silhouette Score* yang diperoleh merupakan ukuran kualitas pengelompokan, bukan ukuran akurasi deteksi anomali.
- Deteksi kandidat anomali menggunakan jarak terhadap centroid dan ambang batas statistik. Tanpa label acuan atau verifikasi independen, hasilnya tidak dapat langsung dinyatakan sebagai kejadian erupsi.
- Sistem ini ditujukan sebagai alat bantu analisis citra dan bukan sebagai pengganti sistem peringatan dini atau keputusan resmi PVMBG.

## 👥 Tim Pengembang

**Pelaksana Kerja Praktik**

- Samsa Faridah
- Wildan Saeful Millah

**Instansi**

Pusat Vulkanologi dan Mitigasi Bencana Geologi (PVMBG)  
Badan Geologi, Kementerian Energi dan Sumber Daya Mineral Republik Indonesia.

**Pembimbing Lapangan**

Dr. Devy Kamil Syahbana
Achmad Fathony, S.T.

## 📚 Dokumentasi

Repository ini mendokumentasikan pengembangan sistem monitoring gunung api, mulai dari pemrosesan citra CCTV, penerapan model *Machine Learning*, evaluasi hasil eksperimen, hingga integrasi hasil analisis ke aplikasi web.

Untuk informasi lebih lengkap mengenai latar belakang, metodologi, implementasi, dan hasil pengujian, silakan merujuk pada laporan kerja praktik proyek ini.

---

<p align="center">
  <strong>Volcano Monitoring System — PVMBG</strong><br>
  Sistem bantu analisis citra CCTV gunung api berbasis Machine Learning.
</p>
