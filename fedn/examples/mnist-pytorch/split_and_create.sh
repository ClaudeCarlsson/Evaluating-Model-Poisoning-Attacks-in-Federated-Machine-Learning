#!/bin/bash


# Check if the number of clients is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 NUM_CLIENTS"
    exit 1
fi
NUM_CLIENTS=$1




# Remove the ../data/clients directory
echo "Removing existing /data/clients directory..."
rm -rf ./data/clients




# Step 1: Split data
echo "Splitting data into $NUM_CLIENTS parts..."
bin/split_data --n_splits=$NUM_CLIENTS

# Check if split_data was successful
if [ $? -ne 0 ]; then
    echo "Data splitting failed."
    exit 1
fi
echo "Data split successfully."





# Step 2: Run clients
echo "Running $NUM_CLIENTS clients..."
Standard/run_clients.sh $NUM_CLIENTS

# Check if run_clients was successful
if [ $? -ne 0 ]; then
    echo "Running clients failed."
    exit 1
fi
echo "Clients are running."
