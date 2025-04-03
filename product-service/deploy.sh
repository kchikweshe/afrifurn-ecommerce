#!/bin/bash

# Exit on any error
set -e

# Configuration
SERVICE_NAME="product-service"
IMAGE_NAME="kchikweshe/afrifurn-product-service"

echo "🚀 Starting deployment process..."

# Build the new image
echo "📦 Building Docker image..."
docker build -t ${IMAGE_NAME}:latest .

# Push the image to registry
echo "⬆️ Pushing image to registry..."
docker push ${IMAGE_NAME}:latest

# Update the service
echo "🔄 Updating service..."
docker service update --image ${IMAGE_NAME}:latest ${SERVICE_NAME}

echo "✅ Deployment completed successfully!"

# Check service status
echo "📊 Service status:"
docker service ps ${SERVICE_NAME} 