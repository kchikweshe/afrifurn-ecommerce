// MongoDB init script to create a user and database

// Define database and user details
const databaseName = "afrifurn";
const username = "kchikweshe";
const password = "mypassword"; // Replace with a strong password

db.createUser({
  user: username,
  pwd: password,
  roles: [{
      role: "readWrite",
      db: databaseName
  }]
});
