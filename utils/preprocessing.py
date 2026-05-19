"""
utils/preprocessing.py
Pipeline preprocessing gambar untuk BananaDetect:
  - Resize 224x224
  - Normalisasi RGB
  - Konversi HSV
  - RGB + HSV gabungan
"""

import cv2
import numpy as np


IMG_SIZE = (224, 224)


def load_image(path: str) -> np.ndarray:
    """Baca gambar dari path, kembalikan array RGB."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resize_image(img: np.ndarray, size=IMG_SIZE) -> np.ndarray:
    """Resize gambar ke ukuran target."""
    return cv2.resize(img, size)


def normalize_rgb(img: np.ndarray) -> np.ndarray:
    """Normalisasi pixel ke rentang [0, 1]."""
    return img.astype(np.float32) / 255.0


def convert_to_hsv(img_rgb: np.ndarray) -> np.ndarray:
    """Konversi gambar RGB ke ruang warna HSV."""
    img_uint8 = (img_rgb * 255).astype(np.uint8) if img_rgb.max() <= 1.0 else img_rgb
    hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)
    return hsv.astype(np.float32) / 255.0


def preprocess_rgb(img_path: str) -> np.ndarray:
    """
    Preprocessing RGB standar:
    1. Load gambar
    2. Resize 224x224
    3. Normalisasi [0,1]
    4. Expand batch dimension

    Returns: np.ndarray shape (1, 224, 224, 3)
    """
    img = load_image(img_path)
    img = resize_image(img)
    img = normalize_rgb(img)
    return np.expand_dims(img, axis=0)


def preprocess_hsv(img_path: str) -> np.ndarray:
    """
    Preprocessing HSV:
    1. Load gambar
    2. Resize 224x224
    3. Konversi ke HSV & normalisasi
    4. Expand batch dimension

    Returns: np.ndarray shape (1, 224, 224, 3)
    """
    img = load_image(img_path)
    img = resize_image(img)
    img = normalize_rgb(img)
    img = convert_to_hsv(img)
    return np.expand_dims(img, axis=0)


def preprocess_rgb_hsv(img_path: str) -> np.ndarray:
    """
    Preprocessing gabungan RGB + HSV:
    Menggabungkan channel RGB (3 ch) dan HSV (3 ch) → 6 channel

    Returns: np.ndarray shape (1, 224, 224, 6)
    """
    img = load_image(img_path)
    img = resize_image(img)
    rgb = normalize_rgb(img)
    hsv = convert_to_hsv(img)
    combined = np.concatenate([rgb, hsv], axis=-1)  # (224, 224, 6)
    return np.expand_dims(combined, axis=0)


def extract_color_stats(img_path: str) -> dict:
    """
    Ekstrak statistik warna sederhana (mean, std per channel RGB dan HSV).
    Berguna untuk analisis dataset.
    """
    img = load_image(img_path)
    img = resize_image(img)
    rgb = img.astype(np.float32) / 255.0
    hsv = convert_to_hsv(rgb)

    stats = {}
    for i, ch in enumerate(['R', 'G', 'B']):
        stats[f'rgb_{ch}_mean'] = float(rgb[:, :, i].mean())
        stats[f'rgb_{ch}_std']  = float(rgb[:, :, i].std())

    for i, ch in enumerate(['H', 'S', 'V']):
        stats[f'hsv_{ch}_mean'] = float(hsv[:, :, i].mean())
        stats[f'hsv_{ch}_std']  = float(hsv[:, :, i].std())

    return stats


# ── Augmentation helper (untuk training) ─────────────────────────
def get_augmentation_generator(train_dir: str, val_dir: str, img_size=IMG_SIZE, batch_size: int = 32):
    """
    Membuat ImageDataGenerator dengan augmentasi untuk training
    dan generator tanpa augmentasi untuk validasi.
    """
    try:
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
    except ImportError:
        raise ImportError("TensorFlow belum terinstall. Jalankan: pip install tensorflow")

    # Generator training (dengan augmentasi)
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )

    # Generator validasi (hanya rescale)
    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )

    val_gen = val_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    return train_gen, val_gen
