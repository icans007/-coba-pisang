"""
utils/evaluation.py
Evaluasi model BananaDetect:
  - Accuracy, Precision, Recall, F1-Score
  - Confusion Matrix
  - Classification Report
  - Visualisasi
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CLASS_NAMES = ['Unripe', 'Ripe', 'Overripe']


def evaluate_model(model_path: str, test_dir: str, img_size=(224, 224), batch_size=32):
    """
    Evaluasi lengkap model pada test set.

    Args:
        model_path: path ke file model .h5
        test_dir:   path ke folder test (berisi subfolder per kelas)
        img_size:   ukuran input gambar
        batch_size: ukuran batch

    Returns:
        dict berisi semua metrik evaluasi
    """
    import tensorflow as tf
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report
    )
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    # Load model
    print(f"[Eval] Loading model: {model_path}")
    model = tf.keras.models.load_model(model_path)

    # Test generator (tanpa augmentasi)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    print(f"[Eval] Test set: {test_gen.samples} gambar")

    # Prediksi
    preds_prob = model.predict(test_gen, verbose=1)
    preds      = np.argmax(preds_prob, axis=1)
    y_true     = test_gen.classes

    # Metrik
    acc   = accuracy_score(y_true, preds)
    prec  = precision_score(y_true, preds, average='macro', zero_division=0)
    rec   = recall_score(y_true, preds, average='macro', zero_division=0)
    f1    = f1_score(y_true, preds, average='macro', zero_division=0)
    cm    = confusion_matrix(y_true, preds)
    report = classification_report(y_true, preds, target_names=CLASS_NAMES, output_dict=True)

    results = {
        'accuracy':  round(acc, 4),
        'precision': round(prec, 4),
        'recall':    round(rec, 4),
        'f1_score':  round(f1, 4),
        'confusion_matrix': cm.tolist(),
        'classification_report': report,
        'num_samples': int(test_gen.samples)
    }

    print(f"\n{'='*40}")
    print(f"  Accuracy  : {acc*100:.2f}%")
    print(f"  Precision : {prec*100:.2f}%")
    print(f"  Recall    : {rec*100:.2f}%")
    print(f"  F1-Score  : {f1*100:.2f}%")
    print(f"{'='*40}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_true, preds, target_names=CLASS_NAMES))

    return results


def plot_confusion_matrix(cm: list, model_name: str, save_dir: str = 'static/images'):
    """
    Visualisasi confusion matrix yang elegan.
    """
    cm_arr = np.array(cm)
    os.makedirs(save_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor('#FAFAF8')
    ax.set_facecolor('#FAFAF8')

    # Color map
    colors = plt.cm.YlGn(cm_arr / cm_arr.max())

    for i in range(len(CLASS_NAMES)):
        for j in range(len(CLASS_NAMES)):
            val = cm_arr[i, j]
            bg  = colors[i, j]
            rect = mpatches.FancyBboxPatch(
                (j, len(CLASS_NAMES) - i - 1), 0.9, 0.9,
                boxstyle="round,pad=0.05",
                facecolor=bg, edgecolor='white', linewidth=2
            )
            ax.add_patch(rect)

            text_color = 'white' if val > cm_arr.max() * 0.6 else '#2A2825'
            ax.text(j + 0.45, len(CLASS_NAMES) - i - 0.55, str(val),
                    ha='center', va='center',
                    fontsize=20, fontweight='bold', color=text_color)

    ax.set_xlim(0, len(CLASS_NAMES))
    ax.set_ylim(0, len(CLASS_NAMES))
    ax.set_xticks([i + 0.45 for i in range(len(CLASS_NAMES))])
    ax.set_yticks([i + 0.45 for i in range(len(CLASS_NAMES))])
    ax.set_xticklabels(CLASS_NAMES, fontsize=12)
    ax.set_yticklabels(CLASS_NAMES[::-1], fontsize=12)
    ax.set_xlabel('Predicted', fontsize=13, fontweight='600', labelpad=10)
    ax.set_ylabel('Actual',    fontsize=13, fontweight='600', labelpad=10)
    ax.set_title(f'Confusion Matrix – {model_name.upper()}',
                 fontsize=14, fontweight='600', pad=15)
    ax.tick_params(length=0)

    plt.tight_layout()
    path = os.path.join(save_dir, f'{model_name}_confusion_matrix.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='#FAFAF8')
    plt.close()
    print(f"[Eval] Confusion matrix disimpan: {path}")
    return path


def plot_metrics_bar(results_vgg16: dict, results_resnet50: dict, save_dir: str = 'static/images'):
    """Visualisasi perbandingan metrik VGG16 vs ResNet50."""
    os.makedirs(save_dir, exist_ok=True)

    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    labels  = ['Accuracy', 'Precision', 'Recall', 'F1-Score']

    v_vals = [results_vgg16.get(m, 0) for m in metrics]
    r_vals = [results_resnet50.get(m, 0) for m in metrics]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#FAFAF8')
    ax.set_facecolor('#FAFAF8')

    bars1 = ax.bar(x - width/2, v_vals, width, label='VGG16',   color='#F5C518CC', edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, r_vals, width, label='ResNet50', color='#4CAF72CC', edgecolor='white', linewidth=1.5)

    # Value labels
    for bar in bars1 + bars2:
        h = bar.get_height()
        ax.annotate(f'{h*100:.1f}%',
                    xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', fontsize=10, fontweight='600')

    ax.set_ylim(0, 1.1)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Perbandingan Metrik VGG16 vs ResNet50', fontsize=14, fontweight='600')
    ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0%','20%','40%','60%','80%','100%'])

    plt.tight_layout()
    path = os.path.join(save_dir, 'model_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='#FAFAF8')
    plt.close()
    print(f"[Eval] Comparison chart disimpan: {path}")
    return path


if __name__ == '__main__':
    """Jalankan evaluasi manual:
       python utils/evaluation.py --model resnet50
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='resnet50', choices=['vgg16', 'resnet50'])
    args = parser.parse_args()

    model_path = os.path.join('models', f'{args.model}_model.h5')
    test_dir   = os.path.join('dataset', 'test')

    results = evaluate_model(model_path, test_dir)
    plot_confusion_matrix(results['confusion_matrix'], args.model)
