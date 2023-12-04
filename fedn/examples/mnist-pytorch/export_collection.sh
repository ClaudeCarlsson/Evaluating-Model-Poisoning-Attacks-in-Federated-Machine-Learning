#!/bin/bash

# Check if an output file name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <output_file.json>"
    exit 1
fi

# MongoDB connection parameters
MONGO_HOST="localhost" # or the hostname where your MongoDB is running
MONGO_PORT="6534"
MONGO_DB="fedn-network"
MONGO_COLLECTION="control.validations"
MONGO_USER="fedn_admin"
MONGO_PASSWORD="password"
# Output file name is the first argument to the script
OUTPUT_FILE=$1

# Exporting MongoDB collection to a JSON file
mongoexport --host=$MONGO_HOST --port=$MONGO_PORT --username=$MONGO_USER --password=$MONGO_PASSWORD --db=$MONGO_DB --collection=$MONGO_COLLECTION --out=$OUTPUT_FILE --authenticationDatabase=admin

echo "Collection exported to $OUTPUT_FILE"
