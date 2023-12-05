#!/bin/bash

# Check if exactly two arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <n_clients> <rounds>"
    exit 1
fi

n_clients="$1"
rounds="$2"

# Check if n_clients is at least 10
if [ "$n_clients" -lt 10 ]; then
    echo "Error: n_clients must be at least 10."
    exit 1
fi

# Directories containing the scripts
directories=("bin" "Gradient_X10_Attack" "Gradient_X100_Attack" "Backdoor_Attack" "Label_Flipping" "Gradient_Inv_Attack" "Standard_0.6")

# Loop through each directory and set executable permissions for .sh files
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        chmod +x $dir/*
    else
        echo "Directory $dir not found."
    fi
done

# Setting executable permissions for Python files in the current directory
chmod +x *.py

echo "All necessary files have been set to executable"

echo "Downloading and installing requirements"
pip install numpy > /dev/null 2>&1
pip install pymongo > /dev/null 2>&1
pip install pyyaml > /dev/null 2>&1
pip install fedn > /dev/null 2>&1
pip install torch > /dev/null 2>&1
apt install python3-venv -y > /dev/null 2>&1
apt install pip -y > /dev/null 2>&1
apt install python3 -y> /dev/null 2>&1
echo "Installation complete"

echo "Building images"

# Navigate to Gradient_X10_Attack and build image
cd Gradient_X10_Attack > /dev/null 2>&1
docker build . -t grad-x10-fedn-client > /dev/null 2>&1
cd ..

# Navigate to Gradient_X100_Attack and build image
cd Gradient_X100_Attack
docker build . -t grad-x100-fedn-client > /dev/null 2>&1
cd ..

# Navigate to Gradient_Inv_Attack and build image
cd Gradient_Inv_Attack
docker build . -t grad-inv-fedn-client > /dev/null 2>&1
cd ..

echo "Images have been successfully built"

echo "Preparing enviroment"
bin/init_venv.sh > /dev/null 2>&1
bin/build.sh > /dev/null 2>&1
bin/get_data > /dev/null 2>&1
echo "Enviroment complete"

read -p $'\e[1;31mGiven the same configuration, this script will overwrite previously results. Please confirm by pressing the \'Enter\' key to proceed.\e[0m'

# Define the subdirectory paths without the leading slash
DIR_PATH_1="Attacks/Gradient_X10"
DIR_PATH_2="Attacks/Gradient_X100"
DIR_PATH_3="Attacks/Gradient_Inv"
DIR_PATH_4="Attacks/Label_Flipping"
DIR_PATH_5="Attacks/Backdoor"

# Create the required directory structure, including parent directories
mkdir -p "Attacks"
mkdir -p "$DIR_PATH_1"
mkdir -p "$DIR_PATH_2"
mkdir -p "$DIR_PATH_3"
mkdir -p "$DIR_PATH_4"
mkdir -p "$DIR_PATH_5"

# Define the directory path with variables and create it
ATTACK_DIR_1="Attacks/Gradient_X10/${n_clients}_clients_${rounds}_rounds"
ATTACK_DIR_2="Attacks/Gradient_X100/${n_clients}_clients_${rounds}_rounds"
ATTACK_DIR_3="Attacks/Gradient_Inv/${n_clients}_clients_${rounds}_rounds"
ATTACK_DIR_4="Attacks/Label_Flipping/${n_clients}_clients_${rounds}_rounds"
ATTACK_DIR_5="Attacks/Backdoor/${n_clients}_clients_${rounds}_rounds"

mkdir -p "$ATTACK_DIR_1"
mkdir -p "$ATTACK_DIR_2"
mkdir -p "$ATTACK_DIR_3"
mkdir -p "$ATTACK_DIR_4"
mkdir -p "$ATTACK_DIR_5"

# Attacks
attacks=(1 4 5)
mal_ratios=(5 10 15 20)

for attack in "${attacks[@]}"; do
    echo "Performing attack: $attack"
    for mal_ratio in "${mal_ratios[@]}"; do
        # Loop 3 times
        for (( i=1; i<=3; i++ ))
        do
            # Initialization to reset the experiment
            echo "Removing old containers and prepare a new experiment"
            docker-compose down > /dev/null 2>&1

            # Function to stop Docker containers safely
            stop_containers() {
                containers=$(docker ps -q --filter ancestor="$1")
                if [ -n "$containers" ]; then
                    docker stop $containers > /dev/null 2>&1
                fi
            }

            # Stop containers with specific ancestor images
            stop_containers "ghcr.io/scaleoutsystems/fedn/fedn:0.5.0-mnist-pytorch"
            stop_containers "ghcr.io/scaleoutsystems/fedn/fedn:master-mnist-pytorch"
            stop_containers "grad-fedn-client"
            stop_containers "grad-x10-fedn-client"
            stop_containers "grad-x100-fedn-client"
            stop_containers "grad-inv-fedn-client"

            echo "Cleanup complete, restarting experiment"
            python3 bin/split_data --n_splits=$n_clients > /dev/null 2>&1
            python3 bin/random_seed > /dev/null 2>&1

            docker-compose up -d > /dev/null 2>&1

            # String to wait for
            wait_for_string="COMBINER: combiner started, ready for requests."

            # Wait for the string in the docker-compose logs
            while : ; do
                # Fetch the latest logs and check for the specific string
                if docker-compose logs | grep "$wait_for_string"; then
                    echo "Restart complete"
                    break
                else
                    echo "Waiting for reducer and combiner..."
                    sleep 2 # Check every 2 seconds
                fi
            done

            # Upload package and download the client.yaml file
            echo "Uploading the package"
            python3 upload.py
            echo "Downloading the client.yaml file"
            python3 client.py

            # Perform calculations
            product=$((n_clients * mal_ratio / 100))
            remaining=$((n_clients - product))
            #fraction=$(echo "scale=2; $mal_ratio / 100" | bc)

            echo "Performing attack"
            echo "Starting clients"
            # Start clients
            if [ "$attack" = "1" ]; then
                Gradient_X10_Attack/run_grad_clients.sh $product > /dev/null 2>&1
            elif [ "$attack" = "2" ]; then
                Gradient_X100_Attack/run_grad_clients.sh $product > /dev/null 2>&1
            elif [ "$attack" = "3" ]; then
                Gradient_Inv_Attack/run_grad_inv_clients.sh $product > /dev/null 2>&1
            elif [ "$attack" = "4" ]; then
                Label_Flipping/poison_data.py data 0.8
                Label_Flipping/run_poisoned_clients.sh $product > /dev/null 2>&1
            elif [ "$attack" = "5" ]; then
                Backdoor_Attack/backdoor_attack.py data 5 0.8
                Backdoor_Attack/run_poisoned_clients.sh $product > /dev/null 2>&1
            fi
            Standard_0.6/run_clients.sh $remaining > /dev/null 2>&1

            echo "Clients started"
            # Run training
            python3 run_training.py --rounds $rounds --n_clients $n_clients

            echo "Attack complete, waiting for results"
            sleep 5

            # Determine the output file path based on the attack value
            if [ "$attack" = "1" ]; then
                OUTPUT_FILE="${ATTACK_DIR_1}/${n_clients}_client_${mal_ratio}_${i}.json"
            elif [ "$attack" = "2" ]; then
                OUTPUT_FILE="${ATTACK_DIR_2}/${n_clients}_client_${mal_ratio}_${i}.json"
            elif [ "$attack" = "3" ]; then
                OUTPUT_FILE="${ATTACK_DIR_3}/${n_clients}_client_${mal_ratio}_${i}.json"
            elif [ "$attack" = "4" ]; then
                OUTPUT_FILE="${ATTACK_DIR_4}/${n_clients}_client_${mal_ratio}_${i}.json"
            elif [ "$attack" = "5" ]; then
                OUTPUT_FILE="${ATTACK_DIR_5}/${n_clients}_client_${mal_ratio}_${i}.json"
            else
                echo "Invalid attack value"
                exit 1
            fi

            echo "Downloading the results"
            sleep 5
            # Run the Python script with the output file path
            python3 download.py $OUTPUT_FILE

            echo "Experiment done"
        done
    done
done
