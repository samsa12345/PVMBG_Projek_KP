import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "volcano-monitoring-secret-key-2026")
    
    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "volcano_monitoring")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    
    # Model Paths
    LEWOTOLOK_MODEL_PATH = os.path.join(BASE_DIR, "models", "lewotolok", "best_resnet50_oversampling_siangmalam.keras")
    TANGKUBAN_MODEL_PATH = os.path.join(BASE_DIR, "models", "tangkuban", "mobilenetv2_feature_extractor.keras")
    TANGKUBAN_KMEANS_PATH = os.path.join(BASE_DIR, "models", "tangkuban", "kmeans_final.pkl")
    TANGKUBAN_CONFIG_PATH = os.path.join(BASE_DIR, "models", "tangkuban", "config.json")
    
    # Lewotolok Classes (0: Tertutup Awan, 1: Asap Putih, 2: Erupsi/Awan Kelabu, 3: Tenang)
    LEWOTOLOK_CLASSES = [
        "Tertutup Awan",
        "Asap Putih",
        "Erupsi/Awan Kelabu",
        "Tenang"
    ]
