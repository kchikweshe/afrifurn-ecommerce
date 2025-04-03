#!/bin/bash

# Function to retrieve the local IP address
get_local_ip() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows command to retrieve the local IP address
        ipconfig | findstr "IPv4 Address" | awk '{print $NF}' | sed '4!d'
    else
        # This command retrieves the local IP address. Adjust the interface name if necessary.
        ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -n 1
    fi
}

# Default to localhost
HOST_IP="localhost"

# Parse command-line options
while getopts "db" opt; do
  case $opt in
    d)
      # Enable dynamic IP
      HOST_IP=$(get_local_ip)
      if [ -z "$HOST_IP" ]; then
          echo "Could not retrieve local IP address. Defaulting to localhost."
          HOST_IP="localhost"
      fi
      ;;
    b)
      # Build the project if necessary
      BUILD_JAR=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Export the HOST_IP environment variable
export HOST_IP
echo "HOST_IP set to $HOST_IP"

# Build the project (assuming Maven is used)
if [ "$BUILD_JAR" = true ]; then
    ./mvnw clean package
fi

# Run the JAR file (assuming the JAR is located in the target directory)
JAR_FILE=$(ls target/*.jar | head -n 1)
if [ -f "$JAR_FILE" ]; then
    java -jar "$JAR_FILE"
else
    echo "JAR file not found in target directory."
    exit 1
fi