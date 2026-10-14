import os
import io
import time
import psycopg2
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def ensure_database():
    """Ensure PostgreSQL database 'volcano_monitoring' exists."""
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "volcano_monitoring")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "postgres")
    
    print(f"[TEST] Checking PostgreSQL connection ({db_host}:{db_port}, DB: {db_name})...")
    
    # Try connecting to volcano_monitoring database
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        conn.close()
        print(f"[TEST] Database '{db_name}' exists and connected successfully.")
        return True
    except Exception as e:
        print(f"[TEST] Could not connect directly to '{db_name}': {e}")
        print("[TEST] Attempting to create database 'volcano_monitoring' via default postgres database...")
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name};")
            cursor.close()
            conn.close()
            print(f"[TEST] Database '{db_name}' created successfully!")
            return True
        except Exception as create_err:
            print(f"[TEST] Error creating database '{db_name}': {create_err}")
            return False

def test_models_and_endpoints():
    print("\n--- STARTING COMPREHENSIVE VOLCANO MONITORING SYSTEM TESTS ---")
    
    # 1. Database connection check
    db_ok = ensure_database()
    assert db_ok, "Database initialization failed!"
    
    from app import app, db, Gunung, AnalisisLewotolok, AnalisisTangkuban
    from services.lewotolok_service import predict_lewotolok
    from services.tangkuban_service import predict_tangkuban
    
    # Create test dummy image file
    test_img_path = "test_cctv_dummy.jpg"
    img = Image.new('RGB', (400, 300), color=(120, 150, 180))
    img.save(test_img_path)
    
    print("\n[TEST 1] Testing Lewotolok ResNet50 Inference Service...")
    res_l = predict_lewotolok(test_img_path)
    print("Lewotolok Result:", res_l)
    assert res_l["prediction"] in ["Tertutup Awan", "Asap Putih", "Erupsi/Awan Kelabu", "Tenang"]
    assert 0 <= res_l["confidence"] <= 100
    assert "duration" in res_l
    print("[PASS] Lewotolok ResNet50 inference verified!")
    
    print("\n[TEST 2] Testing Tangkuban Perahu MobileNetV2 + K-Means Anomaly Service...")
    res_t = predict_tangkuban(test_img_path)
    print("Tangkuban Result:", res_t)
    assert res_t["status"] in ["Kondisi Normal", "Kandidat Anomali"]
    assert res_t["anomaly_score"] > 0
    assert "interpretation" in res_t
    print("[PASS] Tangkuban anomaly detection verified!")
    
    print("\n[TEST 3] Testing Flask Application Client & Endpoints...")
    with app.test_client() as client:
        # GET Dashboard
        resp = client.get('/')
        assert resp.status_code == 200
        assert b"VOLCANO MONITORING" in resp.data
        
        # POST Lewotolok API
        with open(test_img_path, 'rb') as f:
            resp_l = client.post('/api/predict/lewotolok', data={'file': (f, 'test_cctv_dummy.jpg')})
            assert resp_l.status_code == 200
            json_l = resp_l.get_json()
            assert json_l["success"] is True
            assert "prediction" in json_l
            print("API Lewotolok Response:", json_l["prediction"], f"({json_l['confidence']}%)")
            
        # POST Tangkuban API
        with open(test_img_path, 'rb') as f:
            resp_t = client.post('/api/predict/tangkuban', data={'file': (f, 'test_cctv_dummy.jpg')})
            assert resp_t.status_code == 200
            json_t = resp_t.get_json()
            assert json_t["success"] is True
            assert "status" in json_t
            print("API Tangkuban Response:", json_t["status"], f"(Score: {json_t['anomaly_score']})")
            
        # GET History API
        resp_h = client.get('/api/history')
        assert resp_h.status_code == 200
        json_h = resp_h.get_json()
        assert json_h["success"] is True
        assert len(json_h["data"]) >= 2
        item0 = json_h["data"][0]
        assert "image_url" in item0
        print(f"API History Response: {len(json_h['data'])} records found in database. Image URL verified: {item0['image_url']}")
        
        # DELETE single history item
        del_item = json_h["data"][0]
        resp_del = client.delete(f"/api/history/{del_item['gunung_id']}/{del_item['id']}")
        assert resp_del.status_code == 200
        assert resp_del.get_json()["success"] is True
        print(f"[PASS] Single history item #{del_item['id']} deleted successfully.")
        
        # DELETE all history
        resp_del_all = client.delete("/api/history/delete-all")
        assert resp_del_all.status_code == 200
        assert resp_del_all.get_json()["success"] is True
        print("[PASS] Delete all history records verified.")
        
    # Clean up dummy image
    if os.path.exists(test_img_path):
        os.remove(test_img_path)
        
    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_models_and_endpoints()
