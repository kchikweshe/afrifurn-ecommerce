# Use the official Python image as a base
FROM python:3.12.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install  --no-cache-dir -r requirements.txt  "passlib[bcrypt]"

# Copy the local code to the container image
COPY . /app

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--port", "8000"]
