"""
utils/training.py
Training VGG16 dan ResNet50 untuk BananaDetect
"""

import os
import sys
import json
import argparse
import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

# =========================================================
# FIX IMPORT PATH
# =========================================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =========================================================
# CONFIG
# =========================================================

IMG_SIZE = (224, 224)

NUM_CLASSES = 3

BATCH_SIZE = 16

EPOCHS = 20

LEARNING_RATE = 1e-5

# WAJIB SESUAI class_indices
CLASS_NAMES = [
    'Overripe',
    'Ripe',
    'Unripe'
]

DATASET_DIR = os.path.join(
    ROOT_DIR,
    'dataset'
)

MODEL_DIR = os.path.join(
    ROOT_DIR,
    'models'
)

HISTORY_DIR = os.path.join(
    ROOT_DIR,
    'history'
)

# =========================================================
# BUILD VGG16
# =========================================================

def build_vgg16_model():

    import tensorflow as tf

    from tensorflow.keras.applications import VGG16

    from tensorflow.keras.layers import (
        GlobalAveragePooling2D,
        Dense,
        Dropout,
        BatchNormalization
    )

    from tensorflow.keras.models import Model

    print("[Training] Build VGG16...")

    base_model = VGG16(
        include_top=False,
        weights='imagenet',
        input_shape=(*IMG_SIZE, 3)
    )

    # Fine tuning
    for layer in base_model.layers[:-4]:
        layer.trainable = False

    for layer in base_model.layers[-4:]:
        layer.trainable = True

    x = GlobalAveragePooling2D()(base_model.output)

    x = Dense(256, activation='relu')(x)

    x = BatchNormalization()(x)

    x = Dropout(0.5)(x)

    output = Dense(
        NUM_CLASSES,
        activation='softmax'
    )(x)

    model = Model(
        inputs=base_model.input,
        outputs=output,
        name='BananaDetect_VGG16'
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print(f"[Training] VGG16 siap.")
    print(f"Total Params: {model.count_params():,}")

    return model

# =========================================================
# BUILD RESNET50
# =========================================================

def build_resnet50_model():

    import tensorflow as tf

    from tensorflow.keras.applications import ResNet50

    from tensorflow.keras.layers import (
        GlobalAveragePooling2D,
        Dense,
        Dropout,
        BatchNormalization
    )

    from tensorflow.keras.models import Model

    print("[Training] Build ResNet50...")

    base_model = ResNet50(
        include_top=False,
        weights='imagenet',
        input_shape=(*IMG_SIZE, 3)
    )

    # Fine tuning
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    for layer in base_model.layers[-30:]:
        layer.trainable = True

    x = GlobalAveragePooling2D()(base_model.output)

    x = Dense(256, activation='relu')(x)

    x = BatchNormalization()(x)

    x = Dropout(0.5)(x)

    output = Dense(
        NUM_CLASSES,
        activation='softmax'
    )(x)

    model = Model(
        inputs=base_model.input,
        outputs=output,
        name='BananaDetect_ResNet50'
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print(f"[Training] ResNet50 siap.")
    print(f"Total Params: {model.count_params():,}")

    return model

# =========================================================
# CALLBACKS
# =========================================================

def get_callbacks(model_name):

    import tensorflow as tf

    os.makedirs(MODEL_DIR, exist_ok=True)

    best_model_path = os.path.join(
    MODEL_DIR,
    f'{model_name}_best.h5'
)

    callbacks = [

        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),

        tf.keras.callbacks.ModelCheckpoint(
            filepath=best_model_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]

    return callbacks

# =========================================================
# SAVE HISTORY
# =========================================================

def save_history_json(history, model_name):

    os.makedirs(HISTORY_DIR, exist_ok=True)

    history_path = os.path.join(
        HISTORY_DIR,
        f'{model_name}_history.json'
    )

    with open(history_path, 'w') as f:

        json.dump(
            history,
            f,
            indent=2
        )

    print(f"[Training] History saved: {history_path}")

# =========================================================
# PLOT HISTORY
# =========================================================

def plot_history(history, model_name):

    os.makedirs(
        'static/images',
        exist_ok=True
    )

    epochs = range(
        1,
        len(history['accuracy']) + 1
    )

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 5)
    )

    # Accuracy
    ax1.plot(
        epochs,
        history['accuracy'],
        label='Train Accuracy'
    )

    ax1.plot(
        epochs,
        history['val_accuracy'],
        label='Validation Accuracy'
    )

    ax1.set_title(
        f'{model_name.upper()} Accuracy'
    )

    ax1.set_xlabel('Epoch')

    ax1.set_ylabel('Accuracy')

    ax1.legend()

    # Loss
    ax2.plot(
        epochs,
        history['loss'],
        label='Train Loss'
    )

    ax2.plot(
        epochs,
        history['val_loss'],
        label='Validation Loss'
    )

    ax2.set_title(
        f'{model_name.upper()} Loss'
    )

    ax2.set_xlabel('Epoch')

    ax2.set_ylabel('Loss')

    ax2.legend()

    plt.tight_layout()

    save_path = os.path.join(
        'static/images',
        f'{model_name}_learning_curve.png'
    )

    plt.savefig(save_path)

    plt.close()

    print(f"[Training] Plot saved: {save_path}")

# =========================================================
# TRAIN MODEL
# =========================================================

def train_model(
        model_name='vgg16',
        epochs=EPOCHS
):

    from utils.preprocessing import (
        get_augmentation_generator
    )

    train_dir = os.path.join(
        DATASET_DIR,
        'train'
    )

    val_dir = os.path.join(
        DATASET_DIR,
        'val'
    )

    # VALIDASI DATASET
    if not os.path.exists(train_dir):

        print(f"[ERROR] Train folder tidak ada:")
        print(train_dir)

        return

    if not os.path.exists(val_dir):

        print(f"[ERROR] Validation folder tidak ada:")
        print(val_dir)

        return

    # BUILD MODEL
    if model_name == 'vgg16':

        model = build_vgg16_model()

    elif model_name == 'resnet50':

        model = build_resnet50_model()

    else:

        raise ValueError(
            f"Model tidak dikenal: {model_name}"
        )

    # DATA GENERATOR
    train_gen, val_gen = get_augmentation_generator(
        train_dir,
        val_dir,
        IMG_SIZE,
        BATCH_SIZE
    )

    print("\n========== CLASS INDICES ==========")
    print(train_gen.class_indices)
    print("===================================\n")

    # SAVE CLASS INDICES
    os.makedirs(HISTORY_DIR, exist_ok=True)

    class_indices_path = os.path.join(
        HISTORY_DIR,
        'class_indices.json'
    )

    with open(class_indices_path, 'w') as f:

        json.dump(
            train_gen.class_indices,
            f,
            indent=2
        )

    print(f"[Training] Class indices saved:")
    print(class_indices_path)

    print(f"\n[Training] Total Train : {train_gen.samples}")
    print(f"[Training] Total Val   : {val_gen.samples}")

    # TRAINING
    print(f"\n[Training] Start training {model_name.upper()}...")

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=get_callbacks(model_name),
        verbose=1
    )

    # SAVE MODEL
    os.makedirs(MODEL_DIR, exist_ok=True)

    final_model_path = os.path.join(
    MODEL_DIR,
    f'{model_name}_model.h5'
)

    model.save(final_model_path)

    print(f"\n[Training] Model saved:")
    print(final_model_path)

    # SAVE HISTORY
    history_dict = {

        k: [float(v) for v in vals]

        for k, vals in history.history.items()
    }

    save_history_json(
        history_dict,
        model_name
    )

    plot_history(
        history_dict,
        model_name
    )

    # FINAL RESULT
    best_acc = max(
        history_dict.get(
            'val_accuracy',
            [0]
        )
    )

    print("\n" + "=" * 50)

    print(f"MODEL           : {model_name.upper()}")

    print(f"BEST VAL ACC    : {best_acc*100:.2f}%")

    print(f"MODEL LOCATION  : {final_model_path}")

    print("=" * 50 + "\n")

    return history

# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Training BananaDetect'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='vgg16',
        choices=['vgg16', 'resnet50']
    )

    parser.add_argument(
        '--epochs',
        type=int,
        default=EPOCHS
    )

    args = parser.parse_args()

    train_model(
        model_name=args.model,
        epochs=args.epochs
    )