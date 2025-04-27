#!/bin/bash
set -e

# MongoDB connection details
MONGO_HOST="afrifurn-mongodb"
MONGO_PORT="27017"
MONGO_USER="kchikweshe"
MONGO_PASSWORD="mypassword"
MONGO_DB="afrifurn"

# Wait for MongoDB to be ready - this is needed since the script might run
# before MongoDB is fully initialized
echo "Waiting for MongoDB to be ready..."
until mongosh ; do
  echo "MongoDB is really not ready yet - sleeping 2 seconds"
  sleep 2
done

echo "MongoDB is up and running!"

# Wait for auth to be enabled and user to be created
echo "Waiting for MongoDB authentication to be ready..."
until mongosh --host $MONGO_HOST --port $MONGO_PORT --authenticationDatabase $MONGO_DB \
              --username $MONGO_USER --password $MONGO_PASSWORD \
              --eval "db.version()" $MONGO_DB &>/dev/null; do
  echo "MongoDB authentication not ready yet - sleeping 2 seconds"
  sleep 2
done

echo "MongoDB authentication is ready!"

# Function to check if a collection has data
collection_has_data() {
  local collection=$1
  
  local count=$(mongosh --host $MONGO_HOST --port $MONGO_PORT \
                --authenticationDatabase $MONGO_DB \
                --username $MONGO_USER --password $MONGO_PASSWORD \
                --quiet --eval "db.$collection.countDocuments({})" $MONGO_DB)
  
  if [ "$count" -gt 0 ]; then
    return 0  # Collection has data
  else
    return 1  # Collection is empty
  fi
}

# Import JSON files if collections are empty
echo "Checking and importing seed data..."

# Loop through each JSON file in the data directory
for file in /data/seed/afrifurn.*.json; do
  if [ -f "$file" ]; then  # Check if file exists
    # Extract collection name from filename
    collection=$(basename "$file" | sed -E 's/afrifurn\.(.*)\.json/\1/')
    
    # Check if collection already has data
    if collection_has_data "$collection"; then
      echo "Collection '$collection' already has data, skipping import."
    else
      echo "Importing data into collection '$collection'..."
      
      # Import the JSON file
      mongoimport --host $MONGO_HOST --port $MONGO_PORT \
                  --authenticationDatabase $MONGO_DB \
                  --username $MONGO_USER --password $MONGO_PASSWORD \
                  --db $MONGO_DB --collection "$collection" \
                  --file "$file" --jsonArray
      
      echo "Data imported into collection '$collection' successfully."
    fi
  fi
done

echo "Data import completed successfully!"