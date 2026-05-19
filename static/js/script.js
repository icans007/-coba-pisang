/* ============================================================
   BananaDetect – Interactive JavaScript
   ============================================================ */

// ── Theme Toggle ──────────────────────────────────────────────
const themeToggle = document.getElementById('theme-toggle');
const THEME_KEY = 'banana-theme';

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const pref  = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  setTheme(saved || pref);
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
  if (themeToggle) {
    themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    themeToggle.title = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
  }
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}
initTheme();

// ── Sidebar Toggle (Mobile) ────────────────────────────────────
const sidebarToggle = document.querySelector('.sidebar-toggle');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.sidebar-overlay');

if(sidebarToggle){

    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('show');
    });

}

if(overlay){

    overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    });

}

// ── Active Nav Link ────────────────────────────────────────────
document.querySelectorAll('.sidebar-nav a, .navbar-nav a').forEach(a => {
  if (a.getAttribute('href') === window.location.pathname ||
      window.location.pathname.startsWith(a.getAttribute('href')) && a.getAttribute('href') !== '/') {
    a.classList.add('active');
  }
});

document.addEventListener('DOMContentLoaded', () => {

    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('mobileSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const closeSidebar = document.getElementById('closeSidebar');

    // OPEN SIDEBAR
    menuToggle.addEventListener('click', () => {

        sidebar.classList.add('open');
        overlay.classList.add('show');

        document.body.style.overflow = 'hidden';

    });

    // CLOSE FUNCTION
    function closeMenu(){

        sidebar.classList.remove('open');
        overlay.classList.remove('show');

        document.body.style.overflow = '';

    }

    // CLOSE BUTTON
    closeSidebar.addEventListener('click', closeMenu);

    // CLICK OVERLAY
    overlay.addEventListener('click', closeMenu);

});

// ── Toast Notification ─────────────────────────────────────────
function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toast-container') || createToastContainer();
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || '📢'}</span>
    <span class="toast-msg">${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;
  container.appendChild(toast);
  setTimeout(() => toast.style.animation = 'fadeOut 0.3s ease forwards', duration - 300);
  setTimeout(() => toast.remove(), duration);
}

function createToastContainer() {
  const c = document.createElement('div');
  c.id = 'toast-container';
  c.className = 'toast-container';
  document.body.appendChild(c);
  return c;
}

// ── Loading Overlay ────────────────────────────────────────────
function showLoading(text = 'Processing...') {
  let overlay = document.getElementById('loading-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
      <div class="spinner"></div>
      <p class="loading-text" id="loading-text">${text}</p>
    `;
    document.body.appendChild(overlay);
  }
  overlay.querySelector('#loading-text').textContent = text;
  requestAnimationFrame(() => overlay.classList.add('show'));
}

function hideLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.classList.remove('show');
  }
}

// ── File Upload (Predict Page) ─────────────────────────────────
const fileInput   = document.getElementById('file-input');
const uploadZone  = document.getElementById('upload-zone');
const imgPreview  = document.getElementById('img-preview-wrap');
const previewImg  = document.getElementById('preview-img');
const previewName = document.getElementById('preview-name');
const previewSize = document.getElementById('preview-size');
const predictBtn  = document.getElementById('predict-btn');
const uploadForm  = document.getElementById('upload-form');

if (uploadZone) {
  // Drag & Drop
  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
  uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
  uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  });
}

if (fileInput) {
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });
}

function handleFile(file) {
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    showToast('Format tidak didukung. Gunakan JPG, PNG, atau WEBP.', 'error');
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showToast('Ukuran file maksimal 10MB.', 'error');
    return;
  }

  const reader = new FileReader();
  reader.onload = e => {
    if (previewImg)  previewImg.src = e.target.result;
    if (imgPreview)  imgPreview.style.display = 'block';
    if (previewName) previewName.textContent = file.name;
    if (previewSize) previewSize.textContent = formatBytes(file.size);
    if (uploadZone)  uploadZone.style.display = 'none';
    if (predictBtn)  predictBtn.disabled = false;
    showToast('Gambar berhasil dipilih!', 'success');
  };
  reader.readAsDataURL(file);
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/(1024*1024)).toFixed(1) + ' MB';
}

// Remove preview
const removeBtn = document.getElementById('remove-img');
if (removeBtn) {
  removeBtn.addEventListener('click', () => {
    if (imgPreview)  imgPreview.style.display = 'none';
    if (uploadZone)  uploadZone.style.display = 'block';
    if (fileInput)   fileInput.value = '';
    if (predictBtn)  predictBtn.disabled = true;
    const resultSection = document.getElementById('result-section');
    if (resultSection) resultSection.style.display = 'none';
  });
}

// ── Prediction Form Submission ─────────────────────────────────
if (uploadForm) {
  uploadForm.addEventListener('submit', async e => {
    e.preventDefault();
    if (!fileInput || !fileInput.files[0]) {
      showToast('Pilih gambar terlebih dahulu.', 'error');
      return;
    }

    const model = document.querySelector('.model-tab.active')?.dataset.model || 'resnet50';
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('model', model);

    showLoading('Memproses gambar dengan ' + model.toUpperCase() + '...');

    try {
      const res  = await fetch('/predict', { method: 'POST', body: formData });
      const data = await res.json();
      hideLoading();

      if (data.error) { showToast(data.error, 'error'); return; }

      displayResult(data);
      saveHistory(data, fileInput.files[0].name, model);
      showToast('Prediksi selesai!', 'success');
    } catch (err) {
      hideLoading();
      showToast('Terjadi kesalahan. Coba lagi.', 'error');
      console.error(err);
    }
  });
}

function displayResult(data) {
  const section = document.getElementById('result-section');
  if (!section) return;
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth', block: 'start' });

  // Label langsung dari backend (sudah benar)
  const labelTag = document.getElementById('result-label');
  if (labelTag) {
    labelTag.textContent = data.label;
    labelTag.className   = 'result-label-tag ' + data.label.toLowerCase();
  }

  const confText = document.getElementById('result-confidence');
  if (confText) confText.textContent = (data.confidence * 100).toFixed(1) + '%';

  const modelInfo = document.getElementById('result-model');
  if (modelInfo) modelInfo.textContent = data.model.toUpperCase();

  // Confidence bars
  // scores dari API urutan ALPHABETICAL (sama dg flow_from_directory):
  //   scores[0] = Overripe, scores[1] = Ripe, scores[2] = Unripe
  const CLASS_ORDER = ['overripe', 'ripe', 'unripe'];
  CLASS_ORDER.forEach((cls, i) => {
    const score = data.scores[i] || 0;
    const fill  = document.getElementById('bar-' + cls);
    const pct   = document.getElementById('pct-' + cls);
    if (fill) setTimeout(() => fill.style.width = (score * 100).toFixed(1) + '%', 100);
    if (pct)  pct.textContent = (score * 100).toFixed(1) + '%';
  });
}

// ── Model Tab Switch ───────────────────────────────────────────
document.querySelectorAll('.model-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.model-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
  });
});

// ── Prediction History (localStorage) ─────────────────────────
const HISTORY_KEY = 'banana-history';

function saveHistory(data, filename, model) {
  const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  history.unshift({
    id: Date.now(),
    filename,
    label: data.label,
    confidence: (data.confidence * 100).toFixed(1),
    model: model.toUpperCase(),
    time: new Date().toLocaleString('id-ID')
  });
  // Keep latest 50
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 50)));
  renderHistory();
}

function renderHistory() {
  const tbody = document.getElementById('history-tbody');
  if (!tbody) return;
  const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  if (!history.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--gray-400); padding:2rem;">Belum ada riwayat prediksi</td></tr>';
    return;
  }
  tbody.innerHTML = history.map((h, i) => `
    <tr>
      <td class="text-muted text-xs">${i + 1}</td>
      <td>${h.filename || '-'}</td>
      <td><span class="result-label-tag ${h.label.toLowerCase()}" style="font-size:.75rem;padding:3px 10px">${h.label}</span></td>
      <td>${h.confidence}%</td>
      <td class="text-muted text-xs">${h.time}</td>
    </tr>
  `).join('');
}

// Clear History
const clearHistBtn = document.getElementById('clear-history');
if (clearHistBtn) {
  clearHistBtn.addEventListener('click', () => {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
    showToast('Riwayat dihapus.', 'info');
  });
}

// Init history on page load
renderHistory();

// ── Download Prediction Result ─────────────────────────────────
const downloadBtn = document.getElementById('download-result');
if (downloadBtn) {
  downloadBtn.addEventListener('click', () => {
    const label = document.getElementById('result-label')?.textContent || '';
    const conf  = document.getElementById('result-confidence')?.textContent || '';
    const model = document.getElementById('result-model')?.textContent || '';
    const time  = new Date().toLocaleString('id-ID');

    const text = `BananaDetect – Hasil Prediksi\n${'='.repeat(30)}\n` +
      `Kelas    : ${label}\nKonfideni : ${conf}\nModel    : ${model}\nWaktu    : ${time}\n`;

    const blob = new Blob([text], { type: 'text/plain' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = `prediksi-${label}-${Date.now()}.txt`;
    a.click(); URL.revokeObjectURL(url);
    showToast('Hasil diunduh!', 'success');
  });
}

// ── Chart.js Helpers ───────────────────────────────────────────
function getChartColors() {
  const dark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    text:  dark ? '#E0DDD6' : '#5C5A55',
    grid:  dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
    yellow: '#F5C518',
    green:  '#4CAF72',
    coral:  '#D85A30',
    blue:   '#378ADD',
  };
}

function defaultChartOpts(title = '') {
  const c = getChartColors();
  return {
    responsive: true,
    plugins: {
      legend: { labels: { color: c.text, font: { family: 'DM Sans', size: 12 } } },
      title: title ? { display: true, text: title, color: c.text, font: { family: 'DM Sans', size: 13, weight: '500' } } : { display: false },
      tooltip: { backgroundColor: '#1A1917', titleColor: '#FAF9F7', bodyColor: '#A8A59E',
                 borderColor: '#302E2A', borderWidth: 1, cornerRadius: 8, padding: 10 }
    },
    scales: {
      x: { grid: { color: c.grid }, ticks: { color: c.text } },
      y: { grid: { color: c.grid }, ticks: { color: c.text } }
    }
  };
}

// ── Training Charts ────────────────────────────────────────────
function initTrainingCharts(accData, lossData, labels) {
  const c = getChartColors();

  const accCtx = document.getElementById('acc-chart')?.getContext('2d');
  if (accCtx) {
    new Chart(accCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'Train Accuracy', data: accData.train,
            borderColor: c.yellow, backgroundColor: 'transparent',
            pointRadius: 3, tension: 0.4 },
          { label: 'Val Accuracy', data: accData.val,
            borderColor: c.green, backgroundColor: 'transparent',
            pointRadius: 3, tension: 0.4, borderDash: [5,3] }
        ]
      },
      options: { ...defaultChartOpts('Accuracy per Epoch'), ...{ plugins: { ...defaultChartOpts().plugins } } }
    });
  }

  const lossCtx = document.getElementById('loss-chart')?.getContext('2d');
  if (lossCtx) {
    new Chart(lossCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'Train Loss', data: lossData.train,
            borderColor: c.coral, backgroundColor: 'transparent',
            pointRadius: 3, tension: 0.4 },
          { label: 'Val Loss', data: lossData.val,
            borderColor: c.blue, backgroundColor: 'transparent',
            pointRadius: 3, tension: 0.4, borderDash: [5,3] }
        ]
      },
      options: defaultChartOpts('Loss per Epoch')
    });
  }
}

// ── Dataset Distribution Chart ─────────────────────────────────
function initDatasetChart(counts) {
  const c   = getChartColors();
  const ctx = document.getElementById('dataset-chart')?.getContext('2d');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Unripe', 'Ripe', 'Overripe'],
      datasets: [{
        data: counts,
        backgroundColor: [c.green, c.yellow, c.coral],
        borderWidth: 0, hoverOffset: 6
      }]
    },
    options: {
      responsive: true, cutout: '65%',
      plugins: {
        legend: { position: 'bottom', labels: { color: c.text, padding: 16, font: { family: 'DM Sans', size: 12 } } },
        tooltip: { backgroundColor: '#1A1917', titleColor: '#FAF9F7', bodyColor: '#A8A59E', borderColor: '#302E2A', borderWidth: 1, cornerRadius: 8, padding: 10 }
      }
    }
  });
}

// ── Comparison Chart ───────────────────────────────────────────
function initCompareChart(vgg16Data, resnetData) {
  const c   = getChartColors();
  const ctx = document.getElementById('compare-chart')?.getContext('2d');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
      datasets: [
        { label: 'VGG16',   data: vgg16Data,  backgroundColor: c.yellow + 'CC', borderRadius: 6 },
        { label: 'ResNet50', data: resnetData, backgroundColor: c.green  + 'CC', borderRadius: 6 }
      ]
    },
    options: {
      ...defaultChartOpts('Perbandingan Metrik Model'),
      scales: { y: { min: 0, max: 1, grid: { color: c.grid }, ticks: { color: c.text, callback: v => (v*100).toFixed(0)+'%' } },
                x: { grid: { color: c.grid }, ticks: { color: c.text } } }
    }
  });
}

// ── Smooth Scroll on anchor links ─────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});

// ── Init page-specific features ───────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Training page mock data (replace with real Flask data)
  if (document.getElementById('acc-chart')) {
    const epochs = Array.from({length: 20}, (_, i) => `Epoch ${i+1}`);
    const mockAcc = {
      train: [0.42,0.58,0.67,0.74,0.79,0.82,0.84,0.86,0.87,0.88,0.89,0.90,0.91,0.91,0.92,0.92,0.93,0.93,0.94,0.94],
      val:   [0.38,0.55,0.63,0.71,0.77,0.80,0.82,0.84,0.85,0.86,0.87,0.88,0.88,0.89,0.89,0.90,0.90,0.91,0.91,0.92]
    };
    const mockLoss = {
      train: [1.12,0.95,0.82,0.70,0.61,0.54,0.48,0.43,0.39,0.35,0.32,0.29,0.27,0.25,0.24,0.22,0.21,0.20,0.19,0.18],
      val:   [1.18,1.00,0.88,0.76,0.66,0.59,0.53,0.48,0.44,0.40,0.37,0.34,0.32,0.30,0.28,0.26,0.25,0.23,0.22,0.21]
    };
    initTrainingCharts(mockAcc, mockLoss, epochs);
  }

  if (document.getElementById('dataset-chart')) {
    initDatasetChart([320, 315, 328]);
  }

  if (document.getElementById('compare-chart')) {
    initCompareChart(
      [0.924, 0.921, 0.918, 0.920],
      [0.937, 0.934, 0.931, 0.933]
    );
  }

  // Animate stat numbers
  document.querySelectorAll('.stat-value[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const isFloat = el.dataset.float === 'true';
    let start = 0, duration = 1200;
    const step = timestamp => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      el.textContent = isFloat
        ? (progress * target).toFixed(2) + '%'
        : Math.floor(progress * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
});

// ── Camera Feature ─────────────────────────────────────────────
(function () {
  const openBtn     = document.getElementById('open-camera-btn');
  const modal       = document.getElementById('camera-modal');
  const closeBtn    = document.getElementById('close-camera-btn');
  const video       = document.getElementById('camera-video');
  const canvas      = document.getElementById('camera-canvas');
  const captureBtn  = document.getElementById('capture-btn');
  const switchBtn   = document.getElementById('switch-camera-btn');
  const timerSel    = document.getElementById('camera-timer');
  const loadingEl   = document.getElementById('camera-loading');
  const errorEl     = document.getElementById('camera-error');
  const errorMsg    = document.getElementById('camera-error-msg');
  const cdOverlay   = document.getElementById('camera-countdown-overlay');
  const cdNum       = document.getElementById('camera-countdown-num');
  const flashEl     = document.getElementById('camera-flash');

  if (!openBtn) return; // not on predict page

  let stream = null;
  let facingMode = 'environment'; // default: rear camera
  let countdownTimer = null;

  // Open modal
  openBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    startCamera();
  });

  // Close modal
  function closeModal() {
    stopCamera();
    modal.style.display = 'none';
    document.body.style.overflow = '';
    if (countdownTimer) { clearInterval(countdownTimer); countdownTimer = null; }
    if (cdOverlay) cdOverlay.style.display = 'none';
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

  // Start camera stream
  async function startCamera() {
    stopCamera();
    if (loadingEl) loadingEl.style.display = 'flex';
    if (errorEl)   errorEl.style.display = 'none';

    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode, width: { ideal: 1280 }, height: { ideal: 960 } },
        audio: false
      });
      video.srcObject = stream;
      video.onloadedmetadata = () => {
        if (loadingEl) loadingEl.style.display = 'none';
      };
    } catch (err) {
      if (loadingEl) loadingEl.style.display = 'none';
      if (errorEl)   errorEl.style.display = 'flex';
      if (errorMsg) {
        if (err.name === 'NotAllowedError') {
          errorMsg.textContent = 'Izin kamera ditolak. Izinkan akses kamera di pengaturan browser Anda.';
        } else if (err.name === 'NotFoundError') {
          errorMsg.textContent = 'Tidak ada kamera yang ditemukan pada perangkat ini.';
        } else {
          errorMsg.textContent = 'Gagal mengakses kamera: ' + err.message;
        }
      }
      console.error('Camera error:', err);
    }
  }

  // Stop camera stream
  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
    if (video) video.srcObject = null;
  }

  // Switch front/rear camera
  if (switchBtn) {
    switchBtn.addEventListener('click', () => {
      facingMode = (facingMode === 'environment') ? 'user' : 'environment';
      startCamera();
    });
  }

  // Capture photo (with optional timer)
  if (captureBtn) {
    captureBtn.addEventListener('click', () => {
      const delay = parseInt(timerSel?.value || '0', 10);
      if (delay > 0) {
        startCountdown(delay);
      } else {
        takePhoto();
      }
    });
  }

  function startCountdown(seconds) {
    captureBtn.disabled = true;
    let remaining = seconds;
    cdNum.textContent = remaining;
    cdOverlay.style.display = 'flex';

    countdownTimer = setInterval(() => {
      remaining--;
      cdNum.textContent = remaining;
      if (remaining <= 0) {
        clearInterval(countdownTimer);
        countdownTimer = null;
        cdOverlay.style.display = 'none';
        captureBtn.disabled = false;
        takePhoto();
      }
    }, 1000);
  }

  function takePhoto() {
    if (!video || !canvas) return;

    // Flash animation
    if (flashEl) {
      flashEl.style.display = 'block';
      flashEl.style.opacity = '0.8';
      setTimeout(() => { flashEl.style.opacity = '0'; }, 80);
      setTimeout(() => { flashEl.style.display = 'none'; }, 250);
    }

    // Draw frame to canvas
    canvas.width  = video.videoWidth  || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');

    // Mirror if using front camera
    if (facingMode === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      if (!blob) { showToast('Gagal mengambil foto.', 'error'); return; }

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const fileName  = `kamera-pisang-${timestamp}.jpg`;
      const file      = new File([blob], fileName, { type: 'image/jpeg' });

      closeModal();
      handleFile(file);
      showToast('Foto berhasil diambil!', 'success');
    }, 'image/jpeg', 0.92);
  }
})();
