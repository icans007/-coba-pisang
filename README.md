# 🍌 BananaDetect

**Sistem Klasifikasi Tingkat Kematangan Buah Pisang Menggunakan ResNet50 dan VGG16**

> Tugas Akhir / Skripsi · Deep Learning · Transfer Learning · Flask

---

## 📋 Deskripsi

BananaDetect adalah sistem klasifikasi kematangan buah pisang berbasis Deep Learning yang menggunakan metode Transfer Learning dengan arsitektur **VGG16** dan **ResNet50**. Sistem ini mampu mengklasifikasikan gambar pisang ke dalam tiga kategori: **Unripe**, **Ripe**, dan **Overripe** dengan akurasi hingga **93.7%**.

### Hasil Penelitian

| Model    | Accuracy | Precision | Recall | F1-Score |
|----------|----------|-----------|--------|----------|
| ResNet50 | **93.7%** | **93.4%** | **93.1%** | **93.3%** |
| VGG16    | 92.4%    | 92.1%    | 91.8% | 92.0%   |

---

## 🗂️ Struktur Folder

```
BananaDetect/
│
├── app.py                  # Flask backend utama
├── requirements.txt        # Daftar library Python
├── README.md               # Dokumentasi ini
│
├── static/
│   ├── css/
│   │   └── style.css       # CSS premium modern
│   ├── js/
│   │   └── script.js       # JavaScript interaktif
│   ├── images/             # Gambar output (chart, dll)
│   └── uploads/            # Gambar yang diupload user
│
├── templates/
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Dashboard statistik
│   ├── predict.html        # Upload & prediksi
│   ├── training.html       # Kurva training
│   ├── evaluation.html     # Evaluasi model
│   ├── comparison.html     # Perbandingan model
│   └── about.html          # Tentang penelitian
│
├── models/
│   ├── vgg16_model.h5      # Model VGG16 terlatih
│   └── resnet50_model.h5   # Model ResNet50 terlatih
│
├── dataset/
│   ├── train/
│   │   ├── Unripe/
│   │   ├── Ripe/
│   │   └── Overripe/
│   ├── val/
│   │   ├── Unripe/
│   │   ├── Ripe/
│   │   └── Overripe/
│   └── test/
│       ├── Unripe/
│       ├── Ripe/
│       └── Overripe/
│
├── utils/
│   ├── preprocessing.py    # Preprocessing RGB, HSV
│   ├── training.py         # Training VGG16 & ResNet50
│   ├── evaluation.py       # Evaluasi & confusion matrix
│   └── glcm_feature.py     # Ekstraksi fitur GLCM
│
└── history/                # Riwayat prediksi & training JSON
```

---

## 🚀 Tutorial Instalasi & Menjalankan

### 1. Instalasi Python

Download Python 3.10+ dari [python.org](https://www.python.org/downloads/).

**Verifikasi:**
```bash
python --version
# Python 3.10.x
```

### 2. Instalasi VSCode

Download dari [code.visualstudio.com](https://code.visualstudio.com/). Install ekstensi **Python** dari Microsoft.

### 3. Clone / Download Proyek

```bash
# Download ZIP atau clone
git clone <url-repo> BananaDetect
cd BananaDetect
```

### 4. Buat Virtual Environment

```bash
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Linux/Mac)
source venv/bin/activate
```

### 5. Install Library

```bash
pip install -r requirements.txt
```

> ⚠️ TensorFlow cukup besar (~500 MB). Pastikan koneksi internet stabil.

---

## 📦 Download Dataset Kaggle

### Langkah 1 – Install Kaggle CLI
```bash
pip install kaggle
```

### Langkah 2 – Download API Token
1. Login ke [kaggle.com](https://www.kaggle.com)
2. Klik avatar → **Account** → **Create API Token**
3. File `kaggle.json` akan terunduh
4. Letakkan di `~/.kaggle/kaggle.json`

### Langkah 3 – Download Dataset
```bash
kaggle datasets download -d atrithakar/banana-classification
unzip banana-classification.zip -d dataset_raw
```

### Langkah 4 – Susun Folder Dataset
Setelah download, susun gambar ke dalam struktur berikut:

```
dataset/
├── train/
│   ├── Unripe/    ← 224 gambar
│   ├── Ripe/      ← 220 gambar
│   └── Overripe/  ← 230 gambar
├── val/
│   ├── Unripe/    ← 48 gambar
│   ├── Ripe/      ← 48 gambar
│   └── Overripe/  ← 49 gambar
└── test/
    ├── Unripe/    ← 48 gambar
    ├── Ripe/      ← 47 gambar
    └── Overripe/  ← 49 gambar
```

Rasio split yang disarankan: **70% train / 15% val / 15% test**

---

## 🏋️ Training Model

### Training ResNet50
```bash
python utils/training.py --model resnet50 --epochs 20
```

### Training VGG16
```bash
python utils/training.py --model vgg16 --epochs 20
```

Model akan tersimpan di:
- `models/resnet50_model.h5`
- `models/vgg16_model.h5`

Learning curve tersimpan di `static/images/`.

---

## ▶️ Menjalankan Flask

```bash
python app.py
```

Buka browser: **http://localhost:5000**

---

## 🖼️ Tutorial Upload & Prediksi

1. Buka **http://localhost:5000/predict**
2. Pilih model: **ResNet50** (rekomendasi) atau **VGG16**
3. Drag & drop gambar pisang ke area upload, atau klik untuk pilih file
4. Klik **"Analisis Gambar"**
5. Lihat hasil prediksi: kelas, confidence score, dan distribusi probabilitas

---

## 📊 Evaluasi Model

```bash
python utils/evaluation.py --model resnet50
```

Output: Accuracy, Precision, Recall, F1-Score, Confusion Matrix, Classification Report.

---

## 🌐 Tutorial Deployment Gratis

### Option 1 – Render

1. Push kode ke GitHub
2. Daftar di [render.com](https://render.com)
3. New → Web Service → Connect GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Deploy

### Option 2 – Railway

1. Daftar di [railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo
3. Tambahkan environment variable jika perlu
4. Railway otomatis detect Flask dan deploy

### Option 3 – HuggingFace Spaces

1. Daftar di [huggingface.co](https://huggingface.co)
2. New Space → **Gradio** atau **Docker**
3. Upload kode, tambahkan `app.py` sebagai entry point

---

## 🔧 Troubleshooting Error Umum

### ModuleNotFoundError
```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### TensorFlow Error (Versi)
```bash
pip install tensorflow==2.14.0
```

### Model Not Found
```bash
# Pastikan training sudah selesai
python utils/training.py --model resnet50

# Cek file model:
ls models/
# resnet50_model.h5  vgg16_model.h5
```

### Shape Mismatch Error
Pastikan semua gambar dipreprocess ke ukuran **224×224×3** sebelum prediksi.

```python
import cv2
img = cv2.resize(img, (224, 224))
```

### CUDA / GPU Error
Jika tidak ada GPU, TensorFlow akan otomatis menggunakan CPU:
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU
```

### Flask Port Already in Use
```bash
# Ganti port
python app.py  # Edit app.run(port=5001) di app.py
# atau kill proses lama
lsof -ti:5000 | xargs kill -9  # Linux/Mac
```

---

## 📚 Teknologi

| Library        | Versi   | Fungsi                          |
|----------------|---------|----------------------------------|
| Flask          | 3.0.0   | Web framework backend            |
| TensorFlow     | 2.14.0  | Deep learning framework          |
| Keras          | 2.14.0  | High-level neural network API    |
| OpenCV         | 4.8.x   | Image processing                 |
| NumPy          | 1.26.x  | Array operations                 |
| Scikit-learn   | 1.3.x   | Metrics evaluation               |
| Matplotlib     | 3.8.x   | Plotting & visualization         |
| Chart.js       | 4.4.0   | Interactive charts (frontend)    |
| Bootstrap      | 5.x     | UI framework (CDN)               |

---

## 👤 Informasi Penelitian

- **Judul:** Klasifikasi Tingkat Kematangan Buah Pisang Menggunakan ResNet50 dan VGG16 dengan Transfer Learning
- **Dataset:** [Banana Classification – Kaggle](https://www.kaggle.com/datasets/atrithakar/banana-classification)
- **Metode:** Transfer Learning, CNN, Data Augmentation
- **Kelas:** Unripe · Ripe · Overripe
- **Akurasi Terbaik:** 93.7% (ResNet50)

---

© 2024 BananaDetect · Tugas Akhir / Skripsi
