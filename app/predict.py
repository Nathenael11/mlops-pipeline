"""
Model Loading and Predictive Diagnostics Logic
Author: Nathenael Ermias
"""

import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from app.schemas import MachineTelemetryInput, PredictionResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'model_artifacts')

MODEL_PATH = os.path.join(ARTIFACTS_DIR, 'model.pkl')
SCALER_PATH = os.path.join(ARTIFACTS_DIR, 'scaler.pkl')
FEATURES_PATH = os.path.join(ARTIFACTS_DIR, 'feature_names.pkl')

OPTIMAL_THRESHOLD = 0.76

# Lazy loading singletons
_model = None
_scaler = None
_feature_names = None

def load_artifacts():
    global _model, _scaler, _feature_names
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file missing at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)

    if _scaler is None and os.path.exists(SCALER_PATH):
        _scaler = joblib.load(SCALER_PATH)

    if _feature_names is None:
        if os.path.exists(FEATURES_PATH):
            _feature_names = joblib.load(FEATURES_PATH)
        else:
            _feature_names = [
                'Air_temperature_K', 'Process_temperature_K', 'Rotational_speed_rpm',
                'Torque_Nm', 'Tool_wear_min', 'Type_H', 'Type_L', 'Type_M'
            ]
            
    return _model, _scaler, _feature_names

def transform_input_to_features(telemetry: MachineTelemetryInput) -> pd.DataFrame:
    p_type = str(telemetry.product_type).upper()
    
    raw_dict = {
        'Air_temperature_K': float(telemetry.air_temperature),
        'Process_temperature_K': float(telemetry.process_temperature),
        'Rotational_speed_rpm': float(telemetry.rotational_speed),
        'Torque_Nm': float(telemetry.torque),
        'Tool_wear_min': float(telemetry.tool_wear),
        'Type_L': 1 if p_type == 'L' else 0,
        'Type_M': 1 if p_type == 'M' else 0,
        'Type_H': 1 if p_type == 'H' else 0,
    }
    
    _, _, feature_names = load_artifacts()
    df = pd.DataFrame([raw_dict])
    return df.reindex(columns=feature_names, fill_value=0)

def generate_action_recommendation(telemetry: MachineTelemetryInput, is_failure: bool) -> str:
    tool_wear = telemetry.tool_wear
    torque = telemetry.torque
    speed = telemetry.rotational_speed
    temp_diff = telemetry.process_temperature - telemetry.air_temperature
    
    recs = []
    if is_failure:
        if tool_wear >= 200:
            recs.append("CRITICAL: Tool wear limit exceeded (>= 200 min). Replace cutting head immediately.")
        if torque >= 60 or speed <= 1200:
            recs.append("HIGH RISK: Spindle overstrain detected. Check drive shaft alignment & lubrication.")
        if temp_diff < 8.6:
            recs.append("THERMAL ALERT: Dissipation rate low. Inspect coolant circulation and heat exchangers.")
        if not recs:
            recs.append("IMMEDIATE ACTION: Halt machine operation for emergency preventative inspection.")
    else:
        if tool_wear >= 180:
            recs.append("ATTENTION: Tool wear approaching threshold limit (>= 180 min). Plan replacement for next cycle.")
        elif torque >= 55:
            recs.append("MONITOR: Elevated torque observed. Keep under close telemetry monitoring.")
        else:
            recs.append("NORMAL: All machine sensors operating within optimal nominal specifications.")
            
    return " | ".join(recs)

def predict_machine_failure(telemetry: MachineTelemetryInput) -> PredictionResponse:
    model, _, _ = load_artifacts()
    features_df = transform_input_to_features(telemetry)
    
    proba = float(model.predict_proba(features_df)[0, 1])
    risk_score = round(proba * 100, 2)
    is_failure = proba >= OPTIMAL_THRESHOLD
    prediction = "Failure" if is_failure else "No Failure"
    
    # Confidence calculation based on distance from threshold
    denom = (1.0 - OPTIMAL_THRESHOLD) if is_failure else OPTIMAL_THRESHOLD
    dist = abs(proba - OPTIMAL_THRESHOLD) / denom
    confidence = round(min(max(dist * 50.0 + 50.0, 50.0), 99.9), 2)
    
    action = generate_action_recommendation(telemetry, is_failure)
    timestamp = datetime.now(timezone.utc).isoformat()
    
    return PredictionResponse(
        risk_score=risk_score,
        prediction=prediction,
        is_failure=is_failure,
        confidence=confidence,
        threshold_used=OPTIMAL_THRESHOLD,
        recommended_action=action,
        timestamp=timestamp
    )
