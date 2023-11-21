#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Please specify the number of clients as an argument."
  exit 1
fi

# Use the first argument as the number of clients
NUM_CLIENTS=$1


# Loop through the number of clients
for (( client=1; client<=NUM_CLIENTS; client++ ))
do

    docker run -d \
    -v $PWD/clients/client.yaml:/app/client.yaml \
    -v $PWD/clients/data/poisoned_clients/$client:/var/data \
    -e ENTRYPOINT_OPTS=--data_path=/var/data/mnist.pt \
    --network=fedn_default \
    ghcr.io/scaleoutsystems/fedn/fedn:master-mnist-pytorch run client -in client.yaml --name client$client
done
