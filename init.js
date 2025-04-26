// MongoDB initialization script for Docker container
// This is the JavaScript equivalent of the original bash script

const MONGO_HOST = "localhost";
const MONGO_PORT = "27017";
const MONGO_DB = "afrifurn";
const USER_NAME = "kchikweshe";
const PASSWORD = "mypassword";

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

// Function to create user if it doesn't exist
async function createUser() {
  try {
    const conn = new Mongo(`mongodb://${MONGO_HOST}:${MONGO_PORT}`);
    const db = conn.getDB(MONGO_DB);
    
    // Check if user already exists
    const usersInfo = db.getUsers();
    const userExists = usersInfo.users && usersInfo.users.some(user => user.user === USER_NAME);
    
    if (!userExists) {
      print(`Creating user '${USER_NAME}' for database '${MONGO_DB}'...`);
      
      // Create the user with appropriate roles
      db.createUser({
        user: USER_NAME,
        pwd: PASSWORD,
        roles: [
          { role: "readWrite", db: MONGO_DB },
          { role: "dbAdmin", db: MONGO_DB }
        ]
      });
      
      print(`User '${USER_NAME}' created successfully!`);
    } else {
      print(`User '${USER_NAME}' already exists.`);
    }
    
    // Create a test document to ensure the database exists
    db.test.insertOne({ 
      createdAt: new Date(), 
      message: "Database initialization complete" 
    });
    
    print(`Database '${MONGO_DB}' initialized successfully!`);
    
  } catch (err) {
    print(`Error creating user: ${err.message}`);
    throw err;
  }
}

// Main function to run the script
async function main() {
  try {
    // Wait for MongoDB to be ready
    await waitForMongoReady();
    
    // Create the user
    await createUser();
    
    print("MongoDB initialization completed successfully!");
  } catch (err) {
    print(`Error during initialization: ${err.message}`);
  }
}

// Run the main function
main().catch(err => {
  print(`Fatal error: ${err.message}`);
  quit(1);
});