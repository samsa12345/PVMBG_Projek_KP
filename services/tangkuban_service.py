import os
import json
import time
import joblib
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from config import Config

_TANGKUBAN_SYSTEM = None

def get_tangkuban_system():
    """
    Lazy loads and caches MobileNetV2 feature extractor, K-Means model, and threshold config for Tangkuban Perahu.
    """
    global _TANGKUBAN_SYSTEM
    if _TANGKUBAN_SYSTEM is None:
        model_path = Config.TANGKUBAN_MODEL_PATH
        kmeans_path = Config.TANGKUBAN_KMEANS_PATH
        config_path = Config.TANGKUBAN_CONFIG_PATH
        
        for p in [model_path, kmeans_path, config_path]:
            if not os.path.exists(p):
                raise FileNotFoundError(f"Required file not found at: {p}")
                
        print(f"[INFO] Loading Tangkuban Perahu anomaly detection system...")
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            
        feature_extractor = tf.keras.models.load_model(model_path)
        kmeans_model = joblib.load(kmeans_path)
        
        _TANGKUBAN_SYSTEM = {
            "feature_extractor": feature_extractor,
            "kmeans": kmeans_model,
            "config": config_data,
            "threshold": config_data.get("threshold", 17.305027)
        }
        print(f"[INFO] Tangkuban system loaded (Threshold: {_TANGKUBAN_SYSTEM['threshold']:.4f}).")
        
    return _TANGKUBAN_SYSTEM

def predict_tangkuban(image_path):
    """
    Runs anomaly detection on an image file using MobileNetV2 + K-Means distance.
    Returns:
        dict containing anomaly status, anomaly score, threshold, duration, and user interpretation text.
    """
    start_time = time.time()
    
    # 1. Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img_resized = img.resize((224, 224))
    
    img_array = np.array(img_resized, dtype=np.float32)
    img_batch = np.expand_dims(img_array, axis=0)
    
    # Preprocess input for MobileNetV2
    processed_img = preprocess_input(img_batch)
    
    # 2. Extract feature vector
    system = get_tangkuban_system()
    features = system["feature_extractor"].predict(processed_img, verbose=0)
    
    # Flatten features if necessary (e.g. 1x1280)
    if len(features.shape) > 2:
        features = np.reshape(features, (features.shape[0], -1))
        
    # 3. Calculate distance to nearest K-Means cluster center
    kmeans = system["kmeans"]
    cluster_centers = kmeans.cluster_centers_
    
    # Distances from feature vector to all cluster centers
    distances = np.linalg.norm(features - cluster_centers, axis=1)
    min_distance = float(np.min(distances))
    
    threshold = system["threshold"]
    
    # 4. Determine Anomaly Status based on threshold
    if min_distance > threshold:
        status = "Kandidat Anomali"
        interpretation = "Citra memiliki karakteristik visual yang menyimpang dari pola kondisi normal yang digunakan sebagai acuan."
    else:
        status = "Kondisi Normal"
        interpretation = "Citra memiliki karakteristik yang masih berada dalam pola kondisi normal yang digunakan sebagai acuan."
        
    execution_duration = time.time() - start_time
    
    return {
        "status": status,
        "anomaly_score": round(min_distance, 2),
        "threshold": round(threshold, 2),
        "interpretation": interpretation,
        "duration": round(execution_duration, 2)
    }
