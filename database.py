from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc, text

db = SQLAlchemy()

class Gunung(db.Model):
    __tablename__ = 'gunung'
    
    id_gunung = db.Column(db.Integer, primary_key=True)
    nama_gunung = db.Column(db.String(100), nullable=False)
    jenis_model = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            "id_gunung": self.id_gunung,
            "nama_gunung": self.nama_gunung,
            "jenis_model": self.jenis_model,
            "deskripsi": self.deskripsi
        }

class AnalisisLewotolok(db.Model):
    __tablename__ = 'analisis_lewotolok'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_gunung = db.Column(db.Integer, db.ForeignKey('gunung.id_gunung'), nullable=False, default=1)
    nama_file = db.Column(db.String(255), nullable=False)
    waktu_mulai_prediksi = db.Column(db.DateTime, nullable=False, default=datetime.now)
    hasil_prediksi = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    prob_tertutup_awan = db.Column(db.Float, nullable=False)
    prob_asap_putih = db.Column(db.Float, nullable=False)
    prob_erupsi_awan_kelabu = db.Column(db.Float, nullable=False)
    prob_tenang = db.Column(db.Float, nullable=False)
    durasi_eksekusi = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_gunung": self.id_gunung,
            "nama_gunung": "Gunung Lewotolok",
            "nama_file": self.nama_file,
            "waktu_mulai_prediksi": self.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S"),
            "hasil": self.hasil_prediksi,
            "confidence": self.confidence,
            "probabilities": {
                "Tertutup Awan": self.prob_tertutup_awan,
                "Asap Putih": self.prob_asap_putih,
                "Erupsi/Awan Kelabu": self.prob_erupsi_awan_kelabu,
                "Tenang": self.prob_tenang
            },
            "durasi_eksekusi": round(self.durasi_eksekusi, 2)
        }

class AnalisisTangkuban(db.Model):
    __tablename__ = 'analisis_tangkuban'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_gunung = db.Column(db.Integer, db.ForeignKey('gunung.id_gunung'), nullable=False, default=2)
    nama_file = db.Column(db.String(255), nullable=False)
    waktu_mulai_prediksi = db.Column(db.DateTime, nullable=False, default=datetime.now)
    hasil_anomali = db.Column(db.String(100), nullable=False)
    anomaly_score = db.Column(db.Float, nullable=False)
    durasi_eksekusi = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_gunung": self.id_gunung,
            "nama_gunung": "Gunung Tangkuban Perahu",
            "nama_file": self.nama_file,
            "waktu_mulai_prediksi": self.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S"),
            "hasil": self.hasil_anomali,
            "anomaly_score": round(self.anomaly_score, 2),
            "durasi_eksekusi": round(self.durasi_eksekusi, 2)
        }

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_gunung()

def seed_gunung():
    # Ensure initial volcano entries exist
    g1 = Gunung.query.get(1)
    if not g1:
        g1 = Gunung(
            id_gunung=1,
            nama_gunung="Gunung Lewotolok",
            jenis_model="Supervised Learning",
            deskripsi="Klasifikasi kondisi gunung menggunakan ResNet50"
        )
        db.session.add(g1)
        
    g2 = Gunung.query.get(2)
    if not g2:
        g2 = Gunung(
            id_gunung=2,
            nama_gunung="Gunung Tangkuban Perahu",
            jenis_model="Anomaly Detection",
            deskripsi="Deteksi penyimpangan citra menggunakan MobileNetV2 dan K-Means"
        )
        db.session.add(g2)
        
    db.session.commit()

def get_dashboard_summary():
    latest_lewotolok = AnalisisLewotolok.query.order_by(desc(AnalisisLewotolok.id)).first()
    latest_tangkuban = AnalisisTangkuban.query.order_by(desc(AnalisisTangkuban.id)).first()
    
    return {
        "lewotolok": {
            "status": latest_lewotolok.hasil_prediksi if latest_lewotolok else "Belum ada analisis",
            "confidence": f"{latest_lewotolok.confidence:.2f}%" if latest_lewotolok else "-",
            "waktu": latest_lewotolok.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S") if latest_lewotolok else "-"
        },
        "tangkuban": {
            "status": latest_tangkuban.hasil_anomali if latest_tangkuban else "Belum ada analisis",
            "anomaly_score": f"{latest_tangkuban.anomaly_score:.2f}" if latest_tangkuban else "-",
            "waktu": latest_tangkuban.waktu_mulai_prediksi.strftime("%d %B %Y, %H:%M:%S") if latest_tangkuban else "-"
        }
    }
