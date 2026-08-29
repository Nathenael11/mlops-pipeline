"""
FastAPI Application Entry Point
Author: Nathenael Ermias
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas import MachineTelemetryInput, PredictionResponse, HealthResponse
from app.predict import predict_machine_failure, load_artifacts, OPTIMAL_THRESHOLD

AUTHOR_NAME = "Nathenael Ermias"
API_VERSION = "1.0.0"

app = FastAPI(
    title="Predictive Maintenance MLOps API",
    description=(
        "Production-ready MLOps REST API pipeline for machine failure risk classification "
        "using the AI4I 2020 dataset. Features strict Pydantic input validation, "
        "FDR-optimized decision thresholding (0.76), and automated Swagger documentation."
    ),
    version=API_VERSION,
    contact={
        "name": AUTHOR_NAME,
        "url": "https://github.com/Nathenael11",
    }
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "service": "Predictive Maintenance MLOps API",
        "status": "online",
        "author": AUTHOR_NAME,
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    try:
        model, _, _ = load_artifacts()
        model_loaded = model is not None
    except Exception:
        model_loaded = False

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        optimal_threshold=OPTIMAL_THRESHOLD,
        version=API_VERSION,
        author=AUTHOR_NAME
    )

@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Prediction"],
    summary="Predict Machine Failure Risk",
    response_description="Evaluated risk score, failure classification, confidence, and action recommendations."
)
def predict(telemetry: MachineTelemetryInput):
    try:
        response = predict_machine_failure(telemetry)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )
