import sys
import json
import joblib

def run_tests():
    print("=== STARTING ENVIRONMENT & MODEL VERIFICATION TESTS ===")
    
    # 1. Test import tensorflow
    print("\n[Test 1] Importing TensorFlow...")
    import tensorflow as tf
    print(f"-> SUCCESS: TensorFlow version {tf.__version__}")

    # 2. Test import keras
    print("\n[Test 2] Importing Keras...")
    import keras
    print(f"-> SUCCESS: Keras version {keras.__version__}")

    # 3. Load model Lewotolok
    lewotolok_path = "models/lewotolok/best_resnet50_oversampling_siangmalam.keras"
    print(f"\n[Test 3] Loading Lewotolok model from '{lewotolok_path}'...")
    model_lewotolok = tf.keras.models.load_model(lewotolok_path)
    print(f"-> SUCCESS: Lewotolok model loaded successfully. Input shape: {model_lewotolok.input_shape}")

    # 4. Load MobileNetV2 feature extractor Tangkuban
    tangkuban_model_path = "models/tangkuban/mobilenetv2_feature_extractor.keras"
    print(f"\n[Test 4] Loading Tangkuban feature extractor from '{tangkuban_model_path}'...")
    model_tangkuban = tf.keras.models.load_model(tangkuban_model_path)
    print(f"-> SUCCESS: Tangkuban model loaded successfully. Input shape: {model_tangkuban.input_shape}")

    # 5. Load kmeans_final.pkl
    kmeans_path = "models/tangkuban/kmeans_final.pkl"
    print(f"\n[Test 5] Loading K-Means model from '{kmeans_path}'...")
    kmeans_model = joblib.load(kmeans_path)
    print(f"-> SUCCESS: K-Means loaded successfully. Cluster count (n_clusters): {kmeans_model.n_clusters}")

    # 6. Read config.json
    config_path = "models/tangkuban/config.json"
    print(f"\n[Test 6] Reading Tangkuban config from '{config_path}'...")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    print(f"-> SUCCESS: Config read successfully. Keys: {list(config_data.keys())}")
    
    print("\n=== ALL 6 VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
