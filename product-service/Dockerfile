# Use Python slim-bullseye as base - smaller than regular slim
FROM python:3.12.1-slim-bullseye AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set the working directory
WORKDIR /app

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Install FastAPI if not included in requirements.txt
RUN pip install fastapi["standard"]
# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt "passlib[bcrypt]"

# Start a new stage for a smaller final image
FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary files
COPY . .

# Expose the port
EXPOSE 8000

# Run as non-root user for better security
RUN adduser --disabled-password --no-create-home appuser
RUN mkdir -p /app/static &&   chmod 777 -R /app/static  
RUN touch /app/app.log && chmod 666 /app/app.log


USER appuser
# Command to run the FastAPI app

