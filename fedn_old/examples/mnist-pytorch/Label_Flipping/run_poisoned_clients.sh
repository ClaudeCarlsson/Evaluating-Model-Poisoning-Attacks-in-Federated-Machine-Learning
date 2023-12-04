#!/bin/bash

# Number of clients to start
NUM_CLIENTS=$1

if [ -z "$NUM_CLIENTS" ]
then
  echo "Please specify the number of clients to start."
  exit 1
fi

for (( i=1; i<=NUM_CLIENTS; i++ ))
do
  docker run -d \
  -v $PWD/client.yaml:/app/client.yaml \
  -v $PWD/data/poisoned_clients/$i:/var/data \
  -e ENTRYPOINT_OPTS=--data_path=/var/data/mnist.pt \
  --network=fedn_default \
  ghcr.io/scaleoutsystems/fedn/fedn:0.5.0-mnist-pytorch run client -in client.yaml --name client$i
done
