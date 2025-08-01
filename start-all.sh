#!/bin/bash

set -e

# Configurable parameters
EUREKA_PORT=8761
API_GATEWAY_PORT=8080
PRODUCT_SERVICE_PORT=8000
FRONTEND_PORT=3000

EUREKA_DIR="eureka-server"
API_GATEWAY_DIR="api-gateway"
PRODUCT_SERVICE_DIR="product-service"
FRONTEND_DIR="afrifurn-frontend"

RETRY_INTERVAL=3
MAX_RETRIES=30

log() {
  echo -e "\033[1;34m[$(date '+%H:%M:%S')] $1\033[0m"
}

start_service() {
  local dir=$1
  local cmd=$2
  local log_file=$3
  log "Starting $dir..."
  (cd "$dir" && eval "$cmd" > "../$log_file" 2>&1 &)
}

# 1. Start Eureka Server (find the JAR file automatically)
EUREKA_JAR=$(find "$EUREKA_DIR\target" -maxdepth 1 -name "*.jar" | head -n 1)
if [ -z "$EUREKA_JAR" ]; then
  echo "ERROR: No JAR file found in $EUREKA_DIR/target"
  exit 1
fi
start_service "$EUREKA_DIR" "java -jar \"$EUREKA_JAR\"" "eureka.log"

# 2. Start API Gateway (find the JAR file automatically)
API_GATEWAY_JAR=$(find "$API_GATEWAY_DIR/target" -maxdepth 1 -name "*.jar" | head -n 1)
if [ -z "$API_GATEWAY_JAR" ]; then
  echo "ERROR: No JAR file found in $API_GATEWAY_DIR/target"
  exit 1
fi
start_service "$API_GATEWAY_DIR" "java -jar \"$API_GATEWAY_JAR\"" "api-gateway.log"

# 3. Start Product Service
start_service "$PRODUCT_SERVICE_DIR" "fastapi dev main.py" "product-service.log"

# 4. Start Afrifurn Frontend
start_service "$FRONTEND_DIR" "npm run dev" "frontend.log"

log "All services started successfully!"