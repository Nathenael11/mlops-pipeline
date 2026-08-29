#!/usr/bin/env bash
# ==============================================================================
# MLOps Predictive Maintenance Pipeline Deployment Script
# Author: Nathenael Ermias
# ==============================================================================

set -eo pipefail

APP_NAME="predictive_maintenance_mlops"
PORT=8000

echo "[1/4] Checking Docker Environment..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install Docker first."
    exit 1
fi

echo "[2/4] Building Docker Image..."
docker build -t ${APP_NAME}:latest .

echo "[3/4] Running Container on Port ${PORT}..."
if [ $(docker ps -aq -f name=${APP_NAME}) ]; then
    echo "Stopping existing container..."
    docker stop ${APP_NAME} || true
    docker rm ${APP_NAME} || true
fi

docker run -d \
  --name ${APP_NAME} \
  -p ${PORT}:8000 \
  --restart unless-stopped \
  ${APP_NAME}:latest

echo "[4/4] Probing Health Check Endpoint..."
sleep 4

HEALTH_RESPONSE=$(curl -s http://localhost:${PORT}/health || true)

if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo "================================================="
    echo "SUCCESS: MLOps Service Deployed & Healthy!"
    echo "Author: Nathenael Ermias"
    echo "API Docs: http://localhost:${PORT}/docs"
    echo "Health: http://localhost:${PORT}/health"
    echo "================================================="
else
    echo "ERROR: Health check probe failed. Container logs:"
    docker logs ${APP_NAME}
    exit 1
fi
