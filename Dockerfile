# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY /backend/requirements.txt requirements.txt
RUN pip install  --no-cache-dir -r requirements.txt  "passlib[bcrypt]"

# Copy the local code to the container image
COPY /backend/src .

# Expose the port the FastAPI app runs on
EXPOSE 6590

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6590"]
