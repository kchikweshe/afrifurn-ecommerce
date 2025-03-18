HOST="localhost"
APP_NAME="order-service"

API_GATEWAY=f"http://{HOST}:8090"
PORT=8004
EURKEKA_SERVER=f"http://{HOST}:8761"
KAFKA_INSTANCE = f"localhost:9092"
DATABASE_URL = "postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/afrifurn_order_service"
# DATABASE_URL_DOCKER = "postgresql://fastapi_traefik:fastapi_traefik@db:5432/afrifurn_order_service"
