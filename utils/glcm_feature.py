"""
utils/glcm_feature.py
Ekstraksi fitur tekstur menggunakan Gray Level Co-occurrence Matrix (GLCM).
Fitur: Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM
"""

import cv2
import numpy as np


def rgb_to_gray(img_rgb: np.ndarray) -> np.ndarray:
    """Konversi gambar RGB ke grayscale."""
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)


def compute_glcm(gray_img: np.ndarray, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256) -> np.ndarray:
    """
    Hitung GLCM secara manual (tanpa skimage untuk menghindari dependensi tambahan).
    Mengembalikan matriks GLCM shape (levels, levels, len(distances), len(angles)).
    """
    # Quantize ke 64 level untuk efisiensi
    gray_q = (gray_img // 4).astype(np.uint8)
    q_levels = 64

    n_dist   = len(distances)
    n_angles = len(angles)
    glcm     = np.zeros((q_levels, q_levels, n_dist, n_angles), dtype=np.float64)

    h, w = gray_q.shape
    for d_idx, dist in enumerate(distances):
        for a_idx, angle in enumerate(angles):
            dx = int(round(dist * np.cos(angle)))
            dy = int(round(dist * np.sin(angle)))
            for r in range(h):
                for c in range(w):
                    r2 = r + dy
                    c2 = c + dx
                    if 0 <= r2 < h and 0 <= c2 < w:
                        i = gray_q[r, c]
                        j = gray_q[r2, c2]
                        glcm[i, j, d_idx, a_idx] += 1

    # Normalisasi
    for d in range(n_dist):
        for a in range(n_angles):
            total = glcm[:, :, d, a].sum()
            if total > 0:
                glcm[:, :, d, a] /= total

    return glcm


def glcm_features(glcm: np.ndarray) -> dict:
    """
    Hitung properti GLCM:
    - Contrast
    - Dissimilarity
    - Homogeneity
    - Energy (ASM)
    - Correlation
    """
    n = glcm.shape[0]
    i_vals = np.arange(n)
    j_vals = np.arange(n)
    I, J   = np.meshgrid(i_vals, j_vals, indexing='ij')

    # Rata-rata & std per sudut/jarak
    glcm_mean = glcm.mean(axis=(2, 3))  # shape: (n, n)

    contrast     = np.sum(glcm_mean * (I - J) ** 2)
    dissimilarity= np.sum(glcm_mean * np.abs(I - J))
    homogeneity  = np.sum(glcm_mean / (1 + (I - J) ** 2))
    energy       = np.sqrt(np.sum(glcm_mean ** 2))
    asm          = np.sum(glcm_mean ** 2)

    mu_i  = np.sum(I * glcm_mean)
    mu_j  = np.sum(J * glcm_mean)
    sig_i = np.sqrt(np.sum(glcm_mean * (I - mu_i) ** 2))
    sig_j = np.sqrt(np.sum(glcm_mean * (J - mu_j) ** 2))

    if sig_i * sig_j > 0:
        correlation = np.sum(glcm_mean * (I - mu_i) * (J - mu_j)) / (sig_i * sig_j)
    else:
        correlation = 0.0

    return {
        'contrast':      float(contrast),
        'dissimilarity': float(dissimilarity),
        'homogeneity':   float(homogeneity),
        'energy':        float(energy),
        'asm':           float(asm),
        'correlation':   float(correlation),
    }


def extract_glcm_from_path(img_path: str) -> dict:
    """
    Ekstrak fitur GLCM dari path gambar.
    1. Baca gambar
    2. Resize 224x224
    3. Konversi ke grayscale
    4. Hitung GLCM
    5. Ekstrak properti

    Returns:
        dict fitur GLCM
    """
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {img_path}")

    img = cv2.resize(img, (224, 224))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    glcm = compute_glcm(gray, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4])
    features = glcm_features(glcm)

    return features


def extract_glcm_vector(img_path: str) -> np.ndarray:
    """
    Kembalikan vektor fitur GLCM sebagai numpy array untuk input ML.
    Urutan: [contrast, dissimilarity, homogeneity, energy, asm, correlation]
    """
    feats = extract_glcm_from_path(img_path)
    return np.array(list(feats.values()), dtype=np.float32)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        feats = extract_glcm_from_path(path)
        print("\nGLCM Features:")
        for k, v in feats.items():
            print(f"  {k:15s}: {v:.6f}")
    else:
        print("Usage: python utils/glcm_feature.py <path_to_image>")
