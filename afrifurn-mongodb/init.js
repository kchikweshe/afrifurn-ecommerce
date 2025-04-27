// MongoDB init script to create a user and database

// Define database and user details
const databaseName = "afrifurn";
const username = "kchikweshe";
const password = "mypassword"; // Replace with a strong password

// MongoDB connection URL (adjust if needed)
const mongoUrl = "mongodb://localhost:27017/";

import { MongoClient } from 'mongodb';

async function initializeMongo() {
  const client = new MongoClient(mongoUrl);

  try {
    await client.connect();
    const db = client.db(databaseName);

    // Check if the user exists
    const userExists = await db.system.users.findOne({ user: username });

    if (!userExists) {
      // Create the user
      await db.createUser({
        user: username,
        pwd: password,
        roles: [ { role: "readWrite", db: databaseName } ]
      });
      console.log(`User ${username} created successfully for database ${databaseName}`);
    } else {
      console.log(`User ${username} already exists for database ${databaseName}`);
    }

  } catch (error) {
    console.error("Error initializing MongoDB:", error);
  } finally {
    await client.close();
  }
}

// Execute the initialization function
initializeMongo().catch(console.error);