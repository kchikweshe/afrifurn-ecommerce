// MongoDB initialization script for Docker container
// This is the JavaScript equivalent of the original bash script

const MONGO_HOST = "localhost";
const MONGO_PORT = "27017";
const MONGO_USER = "kchikweshe";
const MONGO_PASSWORD = "mypassword";
const MONGO_DB = "afrifurn";
const DATA_DIR = "/data";

// Helper function to sleep/wait
async function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

// Function to check if MongoDB is ready
async function waitForMongoReady() {
  print("Waiting for MongoDB to be ready...");
  
  while (true) {
    try {
      // Try to connect to MongoDB without authentication
      const conn = new Mongo(`mongodb://${MONGO_HOST}:${MONGO_PORT}`);
      const adminDb = conn.getDB("admin");
      adminDb.runCommand({ ping: 1 });
      print("MongoDB is up and running!");
      return;
    } catch (err) {
      print("MongoDB is not ready yet - sleeping 2 seconds");
      await sleep(2);
    }
  }
}

// Function to wait for authentication to be ready
async function waitForAuthReady() {
  print("Waiting for MongoDB authentication to be ready...");
  
  while (true) {
    try {
      // Try to connect with authentication
      const conn = new Mongo(`mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DB}`);
      const testDb = conn.getDB(MONGO_DB);
      testDb.runCommand({ ping: 1 });
      print("MongoDB authentication is ready!");
      return;
    } catch (err) {
      print("MongoDB authentication not ready yet - sleeping 2 seconds");
      await sleep(2);
    }
  }
}

// Function to check if a collection has data
function collectionHasData(collection) {
  const conn = new Mongo(`mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DB}`);
  const db = conn.getDB(MONGO_DB);
  const count = db.getCollection(collection).countDocuments({});
  return count > 0;
}

// Function to import data from a JSON file
function importJsonFile(filePath, collection) {
  try {
    // Read the JSON file
    const fileContent = cat(filePath);
    const jsonData = JSON.parse(fileContent);
    
    // Connect to database
    const conn = new Mongo(`mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DB}`);
    const db = conn.getDB(MONGO_DB);
    
    // Insert the data
    if (Array.isArray(jsonData)) {
      db.getCollection(collection).insertMany(jsonData);
    } else {
      db.getCollection(collection).insertOne(jsonData);
    }
    
    print(`Data imported into collection '${collection}' successfully.`);
    return true;
  } catch (err) {
    print(`Error importing data into '${collection}': ${err.message}`);
    return false;
  }
}

// Function to get all JSON files in the data directory
function getJsonFiles() {
  // This is a simplified approach as JavaScript in MongoDB shell doesn't have direct file system access
  // In a real environment, you'd need to implement this according to your specific setup
  const fileList = listFiles(DATA_DIR);
  return fileList
    .filter(file => file.name.match(/afrifurn\..+\.json$/))
    .map(file => ({ 
      path: file.name,
      collection: file.name.match(/afrifurn\.(.+)\.json$/)[1]
    }));
}

// Main function to run the script
async function main() {
  try {
    // Wait for MongoDB to be ready
    await waitForMongoReady();
    
    // Wait for authentication to be ready
    await waitForAuthReady();
    
    // Import JSON files if collections are empty
    print("Checking and importing seed data...");
    
    const jsonFiles = getJsonFiles();
    
    for (const file of jsonFiles) {
      if (collectionHasData(file.collection)) {
        print(`Collection '${file.collection}' already has data, skipping import.`);
      } else {
        print(`Importing data into collection '${file.collection}'...`);
        importJsonFile(file.path, file.collection);
      }
    }
    
    print("Data import completed successfully!");
  } catch (err) {
    print(`Error during initialization: ${err.message}`);
  }
}

// Run the main function
main().catch(err => {
  print(`Fatal error: ${err.message}`);
  quit(1);
});