# Predictive Maintenance MLOps Pipeline

**Author**: Nathenael Ermias  
**Dataset**: AI4I 2020 Predictive Maintenance Dataset (UCI Repository)  
**Deployment Stack**: FastAPI, Pydantic v2, XGBoost, Docker, Render, GitHub Actions  

---

## 📌 Project Overview

This repository contains a **production-grade MLOps REST API pipeline** built around an XGBoost model trained on the AI4I 2020 Predictive Maintenance Dataset.

In industrial smart manufacturing, false discoveries (false alarms) cause unnecessary machine maintenance shutdowns and waste valuable technician hours. This pipeline operates at an **FDR-Optimized Decision Threshold of 0.76**, reducing False Discovery Rate from **53.12% to 31.15%** while retaining an operational safety recall target $\ge 70\%$.

Key features:
- **FastAPI Core**: Asynchronous, high-performance web service with automated OpenAPI (Swagger) interactive documentation.
- **Pydantic v2 Schema Validation**: Strict input range validation, enum constraints (`L`, `M`, `H`), and custom domain validation ensuring $Process\_Temperature > Air\_Temperature$.
- **Model Artifact Lazy Loading**: Efficient memory management loading serialized XGBoost classifier, StandardScaler, and feature schema.
- **Production Containerization**: Multi-stage Docker image with non-root security principles.
- **Cloud Ready**: Render Infrastructure as Code Blueprint (`render.yaml`) and GitHub Actions CI/CD pipeline.

---

## 🏗 Architecture Diagram

```
                             +----------------------------------------+
                             |   Machine Telemetry Request (JSON)     |
                             +----------------------------------------+
                                                 |
                                                 v
                             +----------------------------------------+
                             |      FastAPI Server (app/main.py)      |
                             +----------------------------------------+
                                                 |
                                                 v
                             +----------------------------------------+
                             |   Pydantic Validation (schemas.py)     |
                             |   - Range checks & L/M/H enum          |
                             |   - ProcessTemp > AirTemp check        |
                             +----------------------------------------+
                                                 |
                                                 v
                             +----------------------------------------+
                             |     Inference Engine (app/predict.py)   |
                             |   - Preprocess & One-Hot Encoding      |
                             |   - XGBoost Probability Inference      |
                             |   - Apply FDR Threshold (0.76)         |
                             +----------------------------------------+
                                                 |
                                                 v
                             +----------------------------------------+
                             |  JSON Response: Risk, Prediction,      |
                             |  Confidence & Action Recommendation    |
                             +----------------------------------------+
```

---

## 📁 Repository Structure

```
mlops-pipeline/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── main.py               # FastAPI application & route declarations
│   ├── schemas.py            # Pydantic v2 schemas & custom validators
│   ├── predict.py            # Feature engineering & inference engine
│   └── model_artifacts/
│       ├── model.pkl         # XGBoost model binary
│       ├── scaler.pkl        # StandardScaler binary
│       └── feature_names.pkl # Model feature column names
├── tests/
│   └── test_main.py          # Pytest suite testing API routes & validation
├── Dockerfile                # Multi-stage security Docker container
├── docker-compose.yml        # Docker Compose configuration
├── render.yaml               # Render Infrastructure as Code Blueprint
├── deploy.sh                 # Local / server deployment shell script
├── requirements.txt          # Pinned Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
└── LICENSE                   # MIT License
```

---

## 🚀 Quick Start Guide

### Option 1: Local Python Environment

1. **Clone & Navigate into directory**:
   ```bash
   cd mlops-pipeline
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start FastAPI Application**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Access Swagger Interactive Documentation**:
   Navigate to **`http://localhost:8000/docs`** in your browser.

---

### Option 2: Docker Container Execution

1. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```

2. **Probe Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

---

### Option 3: Deploy to Render

This repository includes a native `render.yaml` Blueprint file for seamless deployment on Render:

1. Push code to GitHub.
2. Connect repository to [Render.com](https://render.com).
3. Select **New Web Service** -> **Blueprint**.
4. Render will automatically configure build and launch commands.

---

## 🧪 Running Pytest Test Suite

Execute unit tests covering health checks, valid predictions, and invalid Pydantic validation cases:

```bash
pytest tests/test_main.py -v
```

---

## 🌐 API Reference

### 1. Predict Machine Failure (`POST /predict`)
- **Request Body**:
  ```json
  {
    "air_temperature": 300.0,
    "process_temperature": 310.0,
    "rotational_speed": 1500.0,
    "torque": 40.0,
    "tool_wear": 45.0,
    "product_type": "L"
  }
  ```
- **Response**:
  ```json
  {
    "risk_score": 12.4,
    "prediction": "No Failure",
    "is_failure": false,
    "confidence": 91.8,
    "threshold_used": 0.76,
    "recommended_action": "NORMAL: All machine sensors operating within optimal nominal specifications.",
    "timestamp": "2026-08-29T21:50:00.000000Z"
  }
  ```

### 2. Health Check (`GET /health`)
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "optimal_threshold": 0.76,
    "version": "1.0.0",
    "author": "Nathenael Ermias"
  }
  ```

---

## 📜 License

Distributed under the **MIT License**. Author: **Nathenael Ermias**.
