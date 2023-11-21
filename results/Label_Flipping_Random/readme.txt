## Navigate to working directory
cd /Users/Edvin/Desktop/Project/Evaluating-Model-Poisoning-Attacks-in-Federated-Machine-Learning/fedn/examples/mnist-pytorch



## Start Docker
docker-compose up



## Upload default compute package and seed



## Split data
bin/split_data --n_splits=5




## Create poison data
Label_Flipping/poison_data.py data 0.8  

-data is the path which holds the clients directory
-0.8 is the ratio of clients to poison all their data



## Run poisoned clients 
Label_Flipping/run_poisoned_clients.sh 5




## Go to reducer dashboard and start training
