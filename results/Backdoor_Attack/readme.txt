This is the backdoor function used:


def add_backdoor_to_image(image):
    # The plus sign will be 3 pixels tall and wide

    image[0:3, 1] = 255
    image[1, 0:3] = 255
    return image



%%%%%%%%%%%%%% HOW TO USE %%%%%%%%%%%%%%

## Navigate to working directory
cd /Users/Edvin/Desktop/Project/Evaluating-Model-Poisoning-Attacks-in-Federated-Machine-Learning/fedn/examples/mnist-pytorch



## Start Docker
docker-compose up



## Upload default compute package and seed



## Split data
bin/split_data --n_splits=5




## Create poison data
Backdoor_Attack/backdoor_attack.py data 5 0.4

- data is the path which holds the clients directory
- 5 is the target label to add the backdoor to 
- 0.8 is the ratio of clients to poison all their data



## Run poisoned clients 
Label_Flipping/run_poisoned_clients.sh 5




## Go to reducer dashboard and start training
