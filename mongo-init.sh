set -a
source .env
set +a

mongosh admin -u $MONGO_USER -p $MONGODB_PASSWORD --eval '
  db = db.getSiblingDB("afrifurn");
  db.createUser({
    user: "'$MONGO_USER'",
    pwd: "'$MONGODB_PASSWORD'",
    roles: [
      { role: "readWrite", db: "afrifurn" }
    ]
  });
' 