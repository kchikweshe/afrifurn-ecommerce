// This script runs automatically when MongoDB starts with empty data
// It creates the required user and database

print('Starting MongoDB initialization script...');

// Create the database
db = db.getSiblingDB('afrifurn');
print('Switched to database: afrifurn');

// Create application user if it doesn't exist
const userExists = db.getUser('kchikweshe');
if (!userExists) {
  print('Creating user: kchikweshe');
  db.createUser({
    user: 'kchikweshe',
    pwd: 'mypassword',
    roles: [
      { role: 'readWrite', db: 'afrifurn' },
      { role: 'dbAdmin', db: 'afrifurn' }
    ]
  });
  print('User created successfully');
} else {
  print('User kchikweshe already exists');
}

print('MongoDB initialization completed.');