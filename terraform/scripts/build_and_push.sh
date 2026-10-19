#!/usr/bin/env bash
set -euo pipefail

# Build & Push WorkPilot Docker Images to Azure Container Registry (Linux / macOS)

if [ -z "${1:-}" ]; then
  echo "Usage: ./build_and_push.sh <ACR_NAME> [TAG]"
  exit 1
fi

ACR_NAME="$1"
TAG="${2:-latest}"
LOGIN_SERVER="${ACR_NAME}.azurecr.io"

echo "Logging in to Azure Container Registry: ${ACR_NAME}..."
az acr login --name "${ACR_NAME}"

SERVICES=(
  "auth-service:auth-service/Dockerfile:.:prod"
  "hr-service:hr-service/Dockerfile:.:prod"
  "it-service:it-service/Dockerfile:.:prod"
  "workflow-service:workflow-service/Dockerfile:.:prod"
  "notification-service:notification-service/Dockerfile:.:prod"
  "analytics-service:analytics-service/Dockerfile:.:prod"
  "ai-service:ai-service/Dockerfile:.:prod"
  "frontend:frontend/Dockerfile:./frontend:prod"
  "prometheus:monitoring/prometheus/Dockerfile:.:"
  "grafana:monitoring/grafana/Dockerfile:.:"
)

for entry in "${SERVICES[@]}"; do
  IFS=":" read -r NAME DOCKERFILE CONTEXT TARGET <<< "${entry}"
  IMAGE_NAME="${LOGIN_SERVER}/workpilot/${NAME}:${TAG}"
  echo "--> Building ${NAME}..."
  if [ -n "${TARGET}" ]; then
    docker build -f "${DOCKERFILE}" -t "${IMAGE_NAME}" --target "${TARGET}" "${CONTEXT}"
  else
    docker build -f "${DOCKERFILE}" -t "${IMAGE_NAME}" "${CONTEXT}"
  fi
  echo "--> Pushing ${NAME} to ACR..."
  docker push "${IMAGE_NAME}"
done

echo "All images pushed to ${LOGIN_SERVER} successfully!"
