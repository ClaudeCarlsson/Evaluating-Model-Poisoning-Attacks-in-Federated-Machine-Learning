#!/bin/bash

# Path to the MongoDB command file
MONGO_COMMANDS="mongo-commands.js"

# Docker container ID
CONTAINER_ID="397bc197ec0c"

# MongoDB credentials and connection details
MONGO_HOST="localhost:6534"
MONGO_USER="fedn_admin"
MONGO_PASS="password"
AUTH_DB="admin"

# Executing MongoDB commands inside the Docker container
docker exec -i $CONTAINER_ID mongo --host $MONGO_HOST -u $MONGO_USER -p $MONGO_PASS --authenticationDatabase $AUTH_DB < $MONGO_COMMANDS
