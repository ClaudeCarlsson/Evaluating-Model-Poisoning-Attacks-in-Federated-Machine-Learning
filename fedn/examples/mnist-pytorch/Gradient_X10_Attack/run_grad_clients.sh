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
  -v $PWD/data/clients/$i:/var/data \
  -e ENTRYPOINT_OPTS=--data_path=/var/data/mnist.pt \
  --network=fedn_default \
  grad-x10-fedn-client run client -in client.yaml --name grad-client$i
done
