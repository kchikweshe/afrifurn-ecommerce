# Use the official MongoDB image as a base
FROM mongo:7.0

# Set environment variables
ENV MONGO_INITDB_DATABASE=afrifurn

# Create directories
RUN mkdir -p /data/seed

# Copy your seed data
COPY ./seed/ /data/seed/


# Copy your initialization script
COPY ./init.js /docker-entrypoint-initdb.d/
COPY ./init-mongo.sh /docker-entrypoint-initdb.d/


# Make sure MongoDB can read the files
RUN chmod -R 755 /data/seed /docker-entrypoint-initdb.d

# MongoDB runs on port 27017
EXPOSE 27017

# Use the default MongoDB entrypoint
CMD ["mongod"]