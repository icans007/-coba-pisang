"""
BananaDetect – Flask Backend
Sistem Klasifikasi Kematangan Buah Pisang
(Unripe / Ripe / Overripe)

Menggunakan:
- VGG16
- ResNet50
- Transfer Learning
"""

import os
import json
import datetime
import numpy as np

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# =========================================================
# FLASK CONFIG
# =========================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'banana-detect-secret-2025'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# WAJIB SESUAI class_indices HASIL TRAINING
CLASS_NAMES = ['Overripe', 'Ripe', 'Unripe']

MODEL_PATH = {
    'vgg16': os.path.join('models', 'vgg16_model.h5'),
    'resnet50': os.path.join('models', 'resnet50_model.h5')
}

# =========================================================
# MODEL CACHE
# =========================================================

_models = {}


def load_model_tf(model_name: str):

    if model_name not in _models:

        try:
            import tensorflow as tf

            model_path = MODEL_PATH.get(model_name)

            if not model_path or not os.path.exists(model_path):
                print(f"[ERROR] Model tidak ditemukan: {model_path}")
                return None

            print(f"[BananaDetect] Loading model {model_name}...")

            _models[model_name] = tf.keras.models.load_model(model_path)

            print(f"[BananaDetect] Model {model_name} berhasil dimuat.")

        except Exception as e:
            print(f"[ERROR] Gagal load model: {e}")
            return None

    return _models[model_name]


# =========================================================
# VALIDASI FILE
# =========================================================

def allowed_file(filename: str):

    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================================================
# PREPROCESS IMAGE
# =========================================================

def preprocess_image(
        img_path: str,
        model_name: str,
        target_size=(224, 224)
):

    import cv2

    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Gagal membaca gambar: {img_path}")

    # BGR -> RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize
    img = cv2.resize(img, target_size)

    # Float32
    img = img.astype(np.float32)

    # PREPROCESS SESUAI MODEL
    if model_name == 'resnet50':

        from tensorflow.keras.applications.resnet50 import preprocess_input

    else:

        from tensorflow.keras.applications.vgg16 import preprocess_input

    img = preprocess_input(img)

    # Batch dimension
    img = np.expand_dims(img, axis=0)

    return img


# =========================================================
# PREDICT IMAGE
# =========================================================

def predict_image(img_path: str, model_name: str = 'vgg16'):

    model = load_model_tf(model_name)

    if model is None:
        raise ValueError("Model gagal dimuat.")

    # PREPROCESS
    img = preprocess_image(img_path, model_name)

    # PREDICT
    preds = model.predict(img, verbose=0)[0]

    idx = int(np.argmax(preds))

    # DEBUG
    print("\n========== PREDICTION ==========")
    print("Predictions :", preds)
    print("Class Names :", CLASS_NAMES)
    print("Index       :", idx)
    print("Label       :", CLASS_NAMES[idx])
    print("================================\n")

    return {
        'label': CLASS_NAMES[idx],
        'confidence': float(preds[idx]),
        'scores': [float(x) for x in preds],
        'model': model_name,
        'demo': False
    }


# =========================================================
# ROUTES
# =========================================================

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')


@app.route('/predict', methods=['GET'])
def predict_page():

    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict():

    # VALIDASI FILE
    if 'file' not in request.files:

        return jsonify({
            'error': 'Tidak ada file.'
        }), 400

    file = request.files['file']

    if file.filename == '':

        return jsonify({
            'error': 'Nama file kosong.'
        }), 400

    if not allowed_file(file.filename):

        return jsonify({
            'error': 'Format file tidak didukung.'
        }), 400

    # PILIH MODEL
    model_name = request.form.get('model', 'vgg16').lower()

    if model_name not in MODEL_PATH:
        model_name = 'vgg16'

    # BUAT FOLDER
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # SIMPAN FILE
    filename = secure_filename(file.filename)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"{timestamp}_{filename}"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(filepath)

    # PREDIKSI
    try:

        result = predict_image(filepath, model_name)

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500

    # SAVE HISTORY
    save_history_file(result, filename)

    return jsonify(result)


@app.route('/training')
def training():

    return render_template('training.html')


@app.route('/evaluation')
def evaluation():

    return render_template('evaluation.html')


@app.route('/comparison')
def comparison():

    return render_template('comparison.html')


@app.route('/about')
def about():

    return render_template('about.html')


# =========================================================
# HISTORY
# =========================================================

HISTORY_FILE = os.path.join(
    'history',
    'predictions.json'
)


def save_history_file(result: dict, filename: str):

    os.makedirs('history', exist_ok=True)

    history = []

    if os.path.exists(HISTORY_FILE):

        try:

            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)

        except:
            history = []

    history.insert(0, {
        'id': datetime.datetime.now().isoformat(),
        'filename': filename,
        'label': result['label'],
        'confidence': round(result['confidence'] * 100, 2),
        'model': result['model'].upper(),
        'time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    })

    history = history[:100]

    with open(HISTORY_FILE, 'w') as f:

        json.dump(
            history,
            f,
            indent=2,
            ensure_ascii=False
        )


@app.route('/api/history')
def api_history():

    if not os.path.exists(HISTORY_FILE):
        return jsonify([])

    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    return jsonify(history)


@app.route('/api/history/clear', methods=['POST'])
def api_history_clear():

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    return jsonify({
        'message': 'Riwayat dihapus.'
    })


# =========================================================
# STATUS API
# =========================================================

@app.route('/api/status')
def api_status():

    status = {}

    for name, path in MODEL_PATH.items():

        status[name] = {
            'loaded': name in _models,
            'exists': os.path.exists(path),
            'path': path
        }

    return jsonify(status)


# =========================================================
# ERROR HANDLER
# =========================================================

@app.errorhandler(404)
def not_found(e):

    return render_template('index.html'), 404


@app.errorhandler(413)
def too_large(e):

    return jsonify({
        'error': 'Ukuran file terlalu besar.'
    }), 413


@app.errorhandler(500)
def server_error(e):

    return jsonify({
        'error': 'Server error.'
    }), 500


# =========================================================
# RUN APP
# =========================================================

if __name__ == '__main__':

    os.makedirs(
        os.path.join('static', 'uploads'),
        exist_ok=True
    )

    os.makedirs('models', exist_ok=True)

    os.makedirs('history', exist_ok=True)

    print("=" * 50)
    print("🍌 BananaDetect Flask Server")
    print("http://localhost:5000")
    print("=" * 50)

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )