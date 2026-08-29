# ⚙️ MLOps Predictive Maintenance Pipeline

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat&logo=render&logoColor=white)](https://mlops-pipeline-8gpe.onrender.com)
[![Tests](https://img.shields.io/badge/Tests-7%20Passed-brightgreen?style=flat&logo=pytest&logoColor=white)](tests/test_main.py)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Live Demo: [https://mlops-pipeline-8gpe.onrender.com](https://mlops-pipeline-8gpe.onrender.com)  
Interactive API Docs: [https://mlops-pipeline-8gpe.onrender.com/docs](https://mlops-pipeline-8gpe.onrender.com/docs)

---

## 📌 Overview

MLOps Predictive Maintenance Pipeline is a project I built to take my trained XGBoost model (from Task 9) and turn it into a production-ready API service. The application accepts machine sensor readings and predicts the likelihood of equipment failure. I trained the model on the AI4I 2020 dataset and tuned its decision threshold to 0.76 to minimize costly false alarms in manufacturing environments.

---

## ✨ Key Features

- **REST API with FastAPI**: Fast, asynchronous web endpoints for real-time model inference.
- **Input Validation with Pydantic v2**: Rejects out-of-range sensor readings, invalid product types, and enforces physical constraints like `process_temperature > air_temperature`.
- **FDR-Optimized Inference**: Uses a 0.76 probability threshold to lower False Discovery Rate (false alarms) while keeping recall high.
- **Auto-Generated Swagger Docs**: Interactive API testing available out of the box at `/docs`.
- **Docker Containerization**: Multi-stage Dockerfile setup for lightweight, reproducible deployment.
- **CI/CD Pipeline**: GitHub Actions workflow that runs unit tests and builds Docker images automatically on code pushes.
- **Comprehensive Testing**: 7 passing unit tests covering API responses, valid predictions, and edge-case validation errors.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Nathenael11/mlops-pipeline.git
cd mlops-pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run locally
```bash
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to test the API.

### 4. Run tests
```bash
pytest tests/test_main.py -v
```

---

## 📖 API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root endpoint returning service status, author, and documentation links. |
| `GET` | `/health` | Health check endpoint verifying model loading and system status. |
| `POST` | `/predict` | Evaluates sensor telemetry data and returns failure risk prediction. |
| `GET` | `/docs` | Interactive OpenAPI / Swagger documentation interface. |

### Example Request (`POST /predict`)

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

### Example Response

```json
{
  "risk_score": 12.4,
  "prediction": "No Failure",
  "is_failure": false,
  "confidence": 91.8,
  "threshold_used": 0.76,
  "recommended_action": "NORMAL: All machine sensors operating within optimal nominal specifications.",
  "timestamp": "2026-08-29T21:50:00Z"
}
```

---

## 🐳 Deployment

### Docker Setup

Build and run the container locally:

```bash
docker build -t mlops-pipeline .
docker run -p 8000:8000 mlops-pipeline
```

Or run with Docker Compose:

```bash
docker-compose up --build -d
```

### Render Deployment

I deployed this service on Render using the included `render.yaml` blueprint. Any push to the `main` branch automatically triggers GitHub Actions tests and updates the Render deployment.

---

## 📁 Project Structure

```
mlops-pipeline/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── main.py               # FastAPI routes and app initialization
│   ├── schemas.py            # Pydantic v2 models and custom validators
│   ├── predict.py            # Model loading and inference logic
│   └── model_artifacts/
│       ├── model.pkl         # Trained XGBoost model
│       ├── scaler.pkl        # StandardScaler object
│       └── feature_names.pkl # Feature column names
├── tests/
│   └── test_main.py          # Pytest suite (7 passing tests)
├── Dockerfile                # Multi-stage Docker image definition
├── docker-compose.yml        # Local container orchestrator
├── render.yaml               # Render Cloud blueprint
├── deploy.sh                 # Deployment script
├── requirements.txt          # Python package requirements
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
└── LICENSE                   # MIT License
```

---

## 🛠 Technologies Used

- **FastAPI**: Modern Python web framework for building APIs.
- **Pydantic v2**: Data validation and settings management using Python type hints.
- **XGBoost**: Gradient boosting framework used for machine failure prediction.
- **Scikit-Learn**: Machine learning utilities and scaling preprocessing.
- **Uvicorn**: Lightning-fast ASGI server implementation.
- **Docker**: Containerization platform for consistent environments.
- **Pytest & HTTPX**: Testing frameworks for API routes and validation rules.
- **GitHub Actions**: Continuous Integration & Continuous Deployment pipeline.
- **Render**: Cloud hosting platform for API deployment.

---

## 👨‍💻 Author

**Nathenael Ermias**  
- **Email**: [nathnaelermias@gmail.com](mailto:nathnaelermias@gmail.com)  
- **GitHub**: [github.com/Nathenael11](https://github.com/Nathenael11)  
- **LinkedIn**: [linkedin.com/in/nathenael-ermias-753746428](https://www.linkedin.com/in/nathenael-ermias-753746428)  

---

## 🙏 Acknowledgments

- **Elevvo Internship Program** for the predictive maintenance project guidance.
- **UCI Machine Learning Repository** for providing the AI4I 2020 Predictive Maintenance Dataset.
- Open-source communities behind **FastAPI**, **Pydantic**, and **XGBoost**.
