import requests
import json

def test_engine_locally():
    url = "http://127.0.0.1:8080"
    
    # Mock payload for Step 1 (Frame Validation)
    payload = {
        "step_id": "step_1",
        "case_id": "case_01",
        "condition": "c",
        "input_frame": {
            "id": "frame_001",
            "text": "The project must scale to 1000 users without downtime.",
            "locked_at_iso": "2026-06-04T12:00:00Z",
            "doctrinal_scope_tag": "STABILITY",
            "companion_case": "case_01"
        },
        "prior_outputs": {},
        "run_context_data": {
            "started_at_iso": "2026-06-04T12:00:00Z",
            "run_id": "RUN_TEST_XYZ",
            "max_llm_calls": 22
        },
        "model_id": "sonnet",
        "offline_mode": True  # Crucial for test simplicity
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_engine_locally()
