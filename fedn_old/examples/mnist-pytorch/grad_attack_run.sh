#!/bin/bash

# Function to stop Docker containers safely
stop_containers() {
    containers=$(docker ps -q --filter ancestor="$1")
    if [ -n "$containers" ]; then
        docker stop $containers
    else
        echo "No running containers found for ancestor: $1"
    fi
}

# Stop containers with specific ancestor images
stop_containers "ghcr.io/scaleoutsystems/fedn/fedn:0.5.0-mnist-pytorch"
stop_containers "grad-fedn-client"
stop_containers "grad-x10-fedn-client"
stop_containers "grad-x100-fedn-client"
stop_containers "grad-inv-fedn-client"

docker-compose up -d

# Navigate to Gradient_Attack and build image
cd Gradient_Attack
docker build . -t grad-fedn-client
cd ..

# Navigate to Gradient_Inv_Attack and build image
cd Gradient_Inv_Attack
docker build . -t grad-inv-fedn-client
cd ..

# Check if at least three arguments are provided
if [ $# -ne 3 ]; then
    echo "Give three arguments: [type_of_attack] [n_clients] [mal_ratio]"
    exit 1
fi

arg1_type_of_attack=$1
arg2_n_clients=$2
arg3_mal_ratio=$3

# Perform integer multiplication
product=$(($arg2_n_clients*$arg3_mal_ratio/100))
remaining=$(($arg2_n_clients - $product))

if [ "$arg1_type_of_attack" = "1" ]; then
    Gradient_Attack/run_grad_clients.sh $product
elif [ "$arg1_type_of_attack" = "2" ]; then
    Gradient_Inv_Attack/run_grad_inv_clients.sh $product
fi

Standard/run_clients.sh $remaining
