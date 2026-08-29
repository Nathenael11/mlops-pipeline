"""
Pytest Unit Tests for FastAPI MLOps Endpoints and Pydantic Validation
Author: Nathenael Ermias
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["author"] == "Nathenael Ermias"
    assert "documentation" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["optimal_threshold"] == 0.76
    assert data["author"] == "Nathenael Ermias"

def test_predict_valid_input():
    payload = {
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 40.0,
        "tool_wear": 45.0,
        "product_type": "L"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["prediction"] in ["Failure", "No Failure"]
    assert "recommended_action" in data
    assert data["threshold_used"] == 0.76

def test_predict_invalid_temperature_relationship():
    # Process temp (295.0 K) <= Air temp (300.0 K) should trigger Pydantic root validation error
    payload = {
        "air_temperature": 300.0,
        "process_temperature": 295.0,
        "rotational_speed": 1500.0,
        "torque": 40.0,
        "tool_wear": 45.0,
        "product_type": "L"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("strictly greater than air temperature" in str(err) for err in data["detail"])

def test_predict_invalid_product_type():
    # Product type 'X' is invalid (must be L, M, or H)
    payload = {
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 40.0,
        "tool_wear": 45.0,
        "product_type": "X"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_out_of_bounds_inputs():
    # Torque 150.0 Nm exceeds upper limit of 100.0 Nm
    payload = {
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 150.0,
        "tool_wear": 45.0,
        "product_type": "L"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_missing_fields():
    # Payload missing 'torque' and 'tool_wear'
    payload = {
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "product_type": "L"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
