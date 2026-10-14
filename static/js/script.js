/* VOLCANO MONITORING SYSTEM - JavaScript Frontend Controller */

document.addEventListener('DOMContentLoaded', () => {
    initUploadControls();
    initHistoryPage();
});

/* FILE UPLOAD & PREVIEW CONTROLLER */
function initUploadControls() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const analyzeBtn = document.getElementById('analyze-btn');
    const uploadForm = document.getElementById('upload-form');
    
    if (!uploadArea || !fileInput) return;

    // Trigger click on file input
    uploadArea.addEventListener('click', (e) => {
        if (e.target !== fileInput) {
            fileInput.click();
        }
    });

    // Drag and drop handlers
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        }, false);
    });

    uploadArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (fileInput.files && fileInput.files.length > 0) {
            handleFileSelect(fileInput.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Validate image format
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            alert('Format file tidak didukung! Harap unggah gambar bertipe JPG, PNG, atau WEBP.');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewFilename.textContent = file.name;
            previewContainer.style.display = 'block';
            if (analyzeBtn) {
                analyzeBtn.disabled = false;
            }
        };
        reader.readAsDataURL(file);
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const volcanoType = uploadForm.getAttribute('data-volcano');
            if (volcanoType === 'lewotolok') {
                submitLewotolokAnalysis();
            } else if (volcanoType === 'tangkuban') {
                submitTangkubanAnalysis();
            }
        });
    }
}

/* SUBMIT LEWOTOLOK ANALYSIS */
function submitLewotolokAnalysis() {
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultsContainer = document.getElementById('results-container');
    const errorBox = document.getElementById('error-box');

    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Harap pilih gambar terlebih dahulu!');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // UI Loading state
    analyzeBtn.disabled = true;
    loadingOverlay.style.display = 'flex';
    resultsContainer.style.display = 'none';
    if (errorBox) errorBox.style.display = 'none';

    fetch('/api/predict/lewotolok', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;

        if (data.success) {
            renderLewotolokResults(data);
            resultsContainer.style.display = 'block';
        } else {
            showError(data.error || 'Gagal menganalisis gambar Lewotolok.');
        }
    })
    .catch(err => {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;
        showError('Terjadi kesalahan jaringan atau koneksi server.');
        console.error(err);
    });
}

function renderLewotolokResults(data) {
    const mainValue = document.getElementById('res-main-value');
    const confidenceVal = document.getElementById('res-confidence-val');
    const confidenceBar = document.getElementById('res-confidence-bar');
    const filenameVal = document.getElementById('res-filename');
    const timeVal = document.getElementById('res-timestamp');
    const durationVal = document.getElementById('res-duration');

    if (mainValue) mainValue.textContent = data.prediction;
    if (confidenceVal) confidenceVal.textContent = data.confidence.toFixed(2) + '%';
    if (confidenceBar) confidenceBar.style.width = data.confidence + '%';
    if (filenameVal) filenameVal.textContent = data.filename;
    if (timeVal) timeVal.textContent = data.timestamp;
    if (durationVal) durationVal.textContent = data.duration + ' detik';

    // Update probabilities
    const probs = data.probabilities;
    for (const key in probs) {
        const bar = document.getElementById(`prob-bar-${formatKey(key)}`);
        const val = document.getElementById(`prob-val-${formatKey(key)}`);
        if (bar) bar.style.width = probs[key] + '%';
        if (val) val.textContent = probs[key].toFixed(2) + '%';
    }
}

/* SUBMIT TANGKUBAN ANALYSIS */
function submitTangkubanAnalysis() {
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultsContainer = document.getElementById('results-container');
    const errorBox = document.getElementById('error-box');

    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Harap pilih gambar terlebih dahulu!');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // UI Loading state
    analyzeBtn.disabled = true;
    loadingOverlay.style.display = 'flex';
    resultsContainer.style.display = 'none';
    if (errorBox) errorBox.style.display = 'none';

    fetch('/api/predict/tangkuban', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;

        if (data.success) {
            renderTangkubanResults(data);
            resultsContainer.style.display = 'block';
        } else {
            showError(data.error || 'Gagal menganalisis gambar Tangkuban Perahu.');
        }
    })
    .catch(err => {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;
        showError('Terjadi kesalahan jaringan atau koneksi server.');
        console.error(err);
    });
}

function renderTangkubanResults(data) {
    const statusVal = document.getElementById('res-status-val');
    const scoreVal = document.getElementById('res-score-val');
    const interpVal = document.getElementById('res-interpretation');
    const filenameVal = document.getElementById('res-filename');
    const timeVal = document.getElementById('res-timestamp');
    const durationVal = document.getElementById('res-duration');

    if (statusVal) {
        statusVal.textContent = data.status;
        if (data.status === 'Kondisi Normal') {
            statusVal.className = 'status-value badge-normal';
        } else {
            statusVal.className = 'status-value badge-anomali';
        }
    }
    if (scoreVal) scoreVal.textContent = data.anomaly_score.toFixed(2);
    if (interpVal) interpVal.textContent = data.interpretation;
    if (filenameVal) filenameVal.textContent = data.filename;
    if (timeVal) timeVal.textContent = data.timestamp;
    if (durationVal) durationVal.textContent = data.duration + ' detik';
}

function formatKey(key) {
    return key.toLowerCase().replace(/[^a-z0-9]/g, '-');
}

function showError(msg) {
    const errorBox = document.getElementById('error-box');
    if (errorBox) {
        errorBox.textContent = msg;
        errorBox.style.display = 'block';
    } else {
        alert(msg);
    }
}

/* HISTORY PAGE CONTROLLER */
let currentHistoryPage = 1;

function initHistoryPage() {
    const volcanoFilter = document.getElementById('history-volcano-filter');
    const searchInput = document.getElementById('history-search-input');
    const prevBtn = document.getElementById('prev-page-btn');
    const nextBtn = document.getElementById('next-page-btn');
    const deleteAllBtn = document.getElementById('btn-delete-all');
    const modalCloseBtn = document.getElementById('modal-close');
    const modalOverlay = document.getElementById('image-modal');

    if (!volcanoFilter) return;

    volcanoFilter.addEventListener('change', () => {
        currentHistoryPage = 1;
        fetchHistory();
    });

    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                currentHistoryPage = 1;
                fetchHistory();
            }, 300);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentHistoryPage > 1) {
                currentHistoryPage--;
                fetchHistory();
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentHistoryPage++;
            fetchHistory();
        });
    }

    if (deleteAllBtn) {
        deleteAllBtn.addEventListener('click', () => {
            deleteAllHistory();
        });
    }

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeImageModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeImageModal();
            }
        });
    }

    fetchHistory();
}

function fetchHistory() {
    const volcanoFilter = document.getElementById('history-volcano-filter');
    const searchInput = document.getElementById('history-search-input');
    const tableBody = document.getElementById('history-table-body');
    const pageInfo = document.getElementById('page-info');
    const prevBtn = document.getElementById('prev-page-btn');
    const nextBtn = document.getElementById('next-page-btn');

    const volcano = volcanoFilter ? volcanoFilter.value : 'all';
    const q = searchInput ? searchInput.value.trim() : '';

    fetch(`/api/history?gunung=${volcano}&q=${encodeURIComponent(q)}&page=${currentHistoryPage}&per_page=10`)
    .then(res => res.json())
    .then(res => {
        if (!res.success) return;
        
        tableBody.innerHTML = '';
        if (res.data.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 2rem; color: var(--text-muted);">Tidak ada data riwayat analisis.</td></tr>`;
            if (pageInfo) pageInfo.textContent = 'Halaman 1 dari 1';
            if (prevBtn) prevBtn.disabled = true;
            if (nextBtn) nextBtn.disabled = true;
            return;
        }

        res.data.forEach(item => {
            const badgeClass = getBadgeClass(item.hasil);
            const tr = document.createElement('tr');
            const safeFileName = escapeHtml(item.nama_file);
            const safeGunung = escapeHtml(item.gunung);
            const titleText = `${safeGunung} - ${safeFileName}`;
            
            tr.innerHTML = `
                <td>#${item.id}</td>
                <td>
                    <div class="history-thumb-wrapper" onclick="openImageModal('${item.image_url}', '${titleText}')" title="Klik untuk memperbesar gambar">
                        <img src="${item.image_url}" alt="${safeFileName}" class="history-thumb" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                        <div class="history-thumb-placeholder" style="display:none;">No Img</div>
                    </div>
                </td>
                <td><strong>${item.gunung}</strong></td>
                <td><code style="color: var(--accent-cyan);">${item.nama_file}</code></td>
                <td>${item.waktu_str}</td>
                <td><span class="badge ${badgeClass}">${item.hasil}</span></td>
                <td><strong>${item.metric_value}</strong></td>
                <td>${item.durasi}</td>
                <td style="text-align: center;">
                    <button class="btn-delete-row" onclick="deleteSingleHistory(${item.gunung_id}, ${item.id}, '${safeFileName}')" title="Hapus Riwayat Ini">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                        Hapus
                    </button>
                </td>
            `;
            tableBody.appendChild(tr);
        });

        if (pageInfo) pageInfo.textContent = `Halaman ${res.page} dari ${res.total_pages}`;
        if (prevBtn) prevBtn.disabled = (res.page <= 1);
        if (nextBtn) nextBtn.disabled = (res.page >= res.total_pages);
    })
    .catch(err => console.error('Error fetching history:', err));
}

/* DELETE SINGLE HISTORY ITEM */
function deleteSingleHistory(gunungId, itemId, fileName) {
    if (!confirm(`Apakah Anda yakin ingin menghapus riwayat analisis file "${fileName}"?`)) {
        return;
    }

    fetch(`/api/history/${gunungId}/${itemId}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            fetchHistory();
        } else {
            alert(data.error || 'Gagal menghapus riwayat.');
        }
    })
    .catch(err => {
        console.error('Error deleting single history:', err);
        alert('Terjadi kesalahan saat menghapus data riwayat.');
    });
}

/* DELETE ALL HISTORY ITEMS */
function deleteAllHistory() {
    const volcanoFilter = document.getElementById('history-volcano-filter');
    const volcano = volcanoFilter ? volcanoFilter.value : 'all';

    let scopeText = 'SELURUH';
    if (volcano === '1') scopeText = 'seluruh data Gunung Lewotolok';
    if (volcano === '2') scopeText = 'seluruh data Gunung Tangkuban Perahu';

    if (!confirm(`Apakah Anda yakin ingin menghapus ${scopeText} riwayat analisis? Tindakan ini tidak dapat dibatalkan.`)) {
        return;
    }

    fetch(`/api/history/delete-all?gunung=${volcano}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            currentHistoryPage = 1;
            fetchHistory();
        } else {
            alert(data.error || 'Gagal menghapus seluruh riwayat.');
        }
    })
    .catch(err => {
        console.error('Error deleting all history:', err);
        alert('Terjadi kesalahan saat menghapus seluruh data riwayat.');
    });
}

/* IMAGE LIGHTBOX MODAL HANDLERS */
function openImageModal(imgUrl, title) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    const modalTitle = document.getElementById('modal-title');

    if (!modal || !modalImg) return;

    modalImg.src = imgUrl;
    if (modalTitle) modalTitle.textContent = title || 'Pratinjau Citra CCTV';
    modal.classList.add('active');
}

function closeImageModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function getBadgeClass(hasil) {
    if (hasil === 'Kondisi Normal' || hasil === 'Tenang') return 'badge-normal';
    if (hasil === 'Kandidat Anomali' || hasil === 'Erupsi/Awan Kelabu') return 'badge-anomali';
    if (hasil === 'Asap Putih') return 'badge-asap';
    if (hasil === 'Tertutup Awan') return 'badge-awan';
    return 'badge-asap';
}
