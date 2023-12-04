#!/bin/bash

# The image name to match
IMAGE_NAME="ghcr.io/scaleoutsystems/fedn/fedn:0.5.0-mnist-pytorch"

# Find all container IDs created from the specified image
CONTAINER_IDS=$(docker ps -q -f ancestor="$IMAGE_NAME")

# Check if any containers were found
if [ -z "$CONTAINER_IDS" ]; then
    echo "No containers found for the image $IMAGE_NAME"
    exit 0
fi

# Loop through each container ID and remove it
for CONTAINER_ID in $CONTAINER_IDS
do
    # Stop the container
    docker stop $CONTAINER_ID

    # Remove the container
    docker rm $CONTAINER_ID

    echo "Removed container (Container ID: $CONTAINER_ID)"
done

echo "All containers created from the image $IMAGE_NAME have been removed."
