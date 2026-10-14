import os
import time
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input

from config import Config

_LEWOTOLOK_MODEL = None

def get_lewotolok_model():
    """
    Lazy loads and caches the pre-trained ResNet50 model for Lewotolok.
    """
    global _LEWOTOLOK_MODEL
    if _LEWOTOLOK_MODEL is None:
        model_path = Config.LEWOTOLOK_MODEL_PATH
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        print(f"[INFO] Loading Lewotolok ResNet50 model from {model_path}...")
        _LEWOTOLOK_MODEL = tf.keras.models.load_model(model_path)
        print("[INFO] Lewotolok model loaded successfully.")
    
    return _LEWOTOLOK_MODEL

def predict_lewotolok(image_path):
    """
    Runs inference on an image file using the pre-trained Lewotolok ResNet50 model.
    Returns:
        dict containing primary prediction, confidence percentage, class probabilities, and execution duration.
    """
    start_time = time.time()
    
    # 1. Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img_resized = img.resize((224, 224))
    
    img_array = np.array(img_resized, dtype=np.float32)
    img_batch = np.expand_dims(img_array, axis=0)
    
    # Apply standard ResNet50 preprocessing
    processed_img = preprocess_input(img_batch)
    
    # 2. Perform prediction
    model = get_lewotolok_model()
    predictions = model.predict(processed_img, verbose=0)[0]
    
    # 3. Softmax / probability calculation if not normalized
    exp_preds = np.exp(predictions - np.max(predictions))
    probs = exp_preds / np.sum(exp_preds) if np.sum(exp_preds) > 0 else predictions
    # If predictions are already normalized probabilities
    if np.isclose(np.sum(predictions), 1.0, atol=1e-2):
        probs = predictions

    probs_list = [float(p) for p in probs]
    primary_idx = int(np.argmax(probs_list))
    
    classes = Config.LEWOTOLOK_CLASSES
    primary_class = classes[primary_idx]
    confidence = probs_list[primary_idx] * 100.0
    
    execution_duration = time.time() - start_time
    
    # Map probabilities dictionary
    prob_dict = {
        classes[i]: round(probs_list[i] * 100.0, 2)
        for i in range(len(classes))
    }
    
    return {
        "prediction": primary_class,
        "confidence": round(confidence, 2),
        "probabilities": prob_dict,
        "raw_probabilities": {
            "prob_tertutup_awan": round(probs_list[0] * 100.0, 2),
            "prob_asap_putih": round(probs_list[1] * 100.0, 2),
            "prob_erupsi_awan_kelabu": round(probs_list[2] * 100.0, 2),
            "prob_tenang": round(probs_list[3] * 100.0, 2),
        },
        "duration": round(execution_duration, 2)
    }
