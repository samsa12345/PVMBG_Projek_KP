import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import desc, or_

from config import Config
from database import db, init_db, Gunung, AnalisisLewotolok, AnalisisTangkuban, get_dashboard_summary
from services.lewotolok_service import predict_lewotolok
from services.tangkuban_service import predict_tangkuban

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize database
init_db(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Logo static helper
@app.route('/logo/<path:filename>')
def serve_logo(filename):
    logo_dir = os.path.join(app.root_path, 'logo')
    return send_from_directory(logo_dir, filename)

# Dashboard Route
@app.route('/')
@app.route('/dashboard')
def dashboard():
    summary = get_dashboard_summary()
    return render_template('dashboard.html', summary=summary, page='dashboard')

# Lewotolok Route
@app.route('/lewotolok')
def lewotolok():
    return render_template('lewotolok.html', page='lewotolok')

# Tangkuban Route
@app.route('/tangkuban')
def tangkuban():
    return render_template('tangkuban.html', page='tangkuban')

# History Route
@app.route('/riwayat')
def riwayat():
    return render_template('riwayat.html', page='riwayat')

# About Route
@app.route('/tentang')
def tentang():
    return render_template('tentang.html', page='tentang')

# API Predict Lewotolok
@app.route('/api/predict/lewotolok', methods=['POST'])
def api_predict_lewotolok():
    start_time = datetime.now()
    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Tidak ada file yang diunggah"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Tidak ada file yang dipilih"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Format file tidak didukung. Harap gunakan format .jpg, .jpeg, .png, atau .webp"}), 400
        
    try:
        # Generate safe unique filename
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)
        
        # Perform inference
        result = predict_lewotolok(filepath)
        
        # Save analysis result to PostgreSQL database
        raw_probs = result["raw_probabilities"]
        record = AnalisisLewotolok(
            id_gunung=1,
            nama_file=unique_name,
            waktu_mulai_prediksi=start_time,
            hasil_prediksi=result["prediction"],
            confidence=result["confidence"],
            prob_tertutup_awan=raw_probs["prob_tertutup_awan"],
            prob_asap_putih=raw_probs["prob_asap_putih"],
            prob_erupsi_awan_kelabu=raw_probs["prob_erupsi_awan_kelabu"],
            prob_tenang=raw_probs["prob_tenang"],
            durasi_eksekusi=result["duration"]
        )
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "duration": result["duration"],
            "filename": unique_name,
            "timestamp": start_time.strftime("%d %B %Y, %H:%M:%S")
        })
        
    except Exception as e:
        app.logger.error(f"Error prediction Lewotolok: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Terjadi kesalahan saat memproses gambar Lewotolok. Pastikan file gambar valid."
        }), 500

# API Predict Tangkuban Perahu
@app.route('/api/predict/tangkuban', methods=['POST'])
def api_predict_tangkuban():
    start_time = datetime.now()
    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Tidak ada file yang diunggah"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Tidak ada file yang dipilih"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Format file tidak didukung. Harap gunakan format .jpg, .jpeg, .png, atau .webp"}), 400
        
    try:
        # Generate safe unique filename
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)
        
        # Perform inference
        result = predict_tangkuban(filepath)
        
        # Save analysis result to PostgreSQL database
        record = AnalisisTangkuban(
            id_gunung=2,
            nama_file=unique_name,
            waktu_mulai_prediksi=start_time,
            hasil_anomali=result["status"],
            anomaly_score=result["anomaly_score"],
            durasi_eksekusi=result["duration"]
        )
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "status": result["status"],
            "anomaly_score": result["anomaly_score"],
            "threshold": result["threshold"],
            "interpretation": result["interpretation"],
            "duration": result["duration"],
            "filename": unique_name,
            "timestamp": start_time.strftime("%d %B %Y, %H:%M:%S")
        })
        
    except Exception as e:
        app.logger.error(f"Error prediction Tangkuban: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Terjadi kesalahan saat memproses gambar Tangkuban Perahu. Pastikan file gambar valid."
        }), 500

# API History List
@app.route('/api/history', methods=['GET'])
def api_history():
    gunung_id = request.args.get('gunung', 'all')
    search_q = request.args.get('q', '').strip().lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    items = []
    
    # Query Lewotolok records
    if gunung_id in ['all', '1', 'lewotolok']:
        q_lewotolok = AnalisisLewotolok.query
        if search_q:
            q_lewotolok = q_lewotolok.filter(AnalisisLewotolok.nama_file.ilike(f"%{search_q}%"))
        for rec in q_lewotolok.all():
            items.append({
                "id": rec.id,
                "gunung_id": 1,
                "gunung": "Gunung Lewotolok",
                "nama_file": rec.nama_file,
                "image_url": f"/uploads/{rec.nama_file}",
                "waktu": rec.waktu_mulai_prediksi,
                "waktu_str": rec.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S"),
                "hasil": rec.hasil_prediksi,
                "metric_label": "Confidence",
                "metric_value": f"{rec.confidence:.2f}%",
                "durasi": f"{rec.durasi_eksekusi:.2f}s"
            })
            
    # Query Tangkuban records
    if gunung_id in ['all', '2', 'tangkuban']:
        q_tangkuban = AnalisisTangkuban.query
        if search_q:
            q_tangkuban = q_tangkuban.filter(AnalisisTangkuban.nama_file.ilike(f"%{search_q}%"))
        for rec in q_tangkuban.all():
            items.append({
                "id": rec.id,
                "gunung_id": 2,
                "gunung": "Gunung Tangkuban Perahu",
                "nama_file": rec.nama_file,
                "image_url": f"/uploads/{rec.nama_file}",
                "waktu": rec.waktu_mulai_prediksi,
                "waktu_str": rec.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S"),
                "hasil": rec.hasil_anomali,
                "metric_label": "Anomaly Score",
                "metric_value": f"{rec.anomaly_score:.2f}",
                "durasi": f"{rec.durasi_eksekusi:.2f}s"
            })
            
    # Sort descending by time
    items.sort(key=lambda x: x["waktu"], reverse=True)
    
    total_count = len(items)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]
    
    # Remove datetime object before sending JSON
    for item in paginated_items:
        del item["waktu"]
        
    return jsonify({
        "success": True,
        "data": paginated_items,
        "page": page,
        "per_page": per_page,
        "total_items": total_count,
        "total_pages": (total_count + per_page - 1) // per_page if total_count > 0 else 1
    })

def remove_upload_file(filename):
    if not filename:
        return
    try:
        l_count = AnalisisLewotolok.query.filter_by(nama_file=filename).count()
        t_count = AnalisisTangkuban.query.filter_by(nama_file=filename).count()
        if l_count == 0 and t_count == 0:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
    except Exception as e:
        app.logger.warning(f"Failed to delete upload file {filename}: {e}")

# API Delete Single History Item
@app.route('/api/history/<int:gunung_id>/<int:item_id>', methods=['DELETE'])
def api_delete_single_history(gunung_id, item_id):
    try:
        filename_to_delete = None
        if gunung_id == 1:
            rec = AnalisisLewotolok.query.get(item_id)
            if not rec:
                return jsonify({"success": False, "error": "Data riwayat tidak ditemukan"}), 404
            filename_to_delete = rec.nama_file
            db.session.delete(rec)
        elif gunung_id == 2:
            rec = AnalisisTangkuban.query.get(item_id)
            if not rec:
                return jsonify({"success": False, "error": "Data riwayat tidak ditemukan"}), 404
            filename_to_delete = rec.nama_file
            db.session.delete(rec)
        else:
            return jsonify({"success": False, "error": "ID Gunung tidak valid"}), 400
            
        db.session.commit()
        
        if filename_to_delete:
            remove_upload_file(filename_to_delete)
            
        return jsonify({"success": True, "message": "Riwayat berhasil dihapus"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting history item: {str(e)}")
        return jsonify({"success": False, "error": "Gagal menghapus data riwayat"}), 500

# API Delete All History
@app.route('/api/history/delete-all', methods=['DELETE'])
def api_delete_all_history():
    gunung_id = request.args.get('gunung', 'all')
    try:
        filenames_to_check = []
        if gunung_id in ['all', '1', 'lewotolok']:
            records = AnalisisLewotolok.query.all()
            filenames_to_check.extend([r.nama_file for r in records])
            AnalisisLewotolok.query.delete()
            
        if gunung_id in ['all', '2', 'tangkuban']:
            records = AnalisisTangkuban.query.all()
            filenames_to_check.extend([r.nama_file for r in records])
            AnalisisTangkuban.query.delete()
            
        db.session.commit()
        
        for fname in set(filenames_to_check):
            remove_upload_file(fname)
            
        return jsonify({"success": True, "message": "Semua data riwayat berhasil dihapus"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting all history: {str(e)}")
        return jsonify({"success": False, "error": "Gagal menghapus seluruh riwayat"}), 500

# API Dashboard Summary
@app.route('/api/dashboard-summary')
def api_dashboard_summary():
    return jsonify({"success": True, "summary": get_dashboard_summary()})

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": "Endpoint tidak ditemukan"}), 404
    return render_template('dashboard.html', summary=get_dashboard_summary(), error="Halaman tidak ditemukan"), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": "Terjadi kesalahan pada server"}), 500
    return render_template('dashboard.html', summary=get_dashboard_summary(), error="Terjadi kesalahan internal server"), 500

if __name__ == '__main__':
    print("[INFO] Starting Volcano Monitoring System...")
    app.run(host='127.0.0.1', port=5000, debug=True)
