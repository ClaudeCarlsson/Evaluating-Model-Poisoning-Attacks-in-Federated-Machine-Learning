#!/usr/bin/env python3

import os
import torch
import sys
import random


def count_folders(directory):
    """Count the number of folders in the specified directory."""
    if not os.path.exists(directory):
        return "Directory does not exist."

    folder_count = 0
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            folder_count += 1

    return folder_count



def label_flip(root_dir, swap_function, p_ratio):
    """
    Swaps labels in the y_train of mnist.pt files located in numbered subfolders and saves them in corresponding subdirectories
    within the poisoned_clients directory.

    :param root_dir: The root directory where the 'clients' folder is located.
    :param num_folders: The number of folders to process.
    :param swap_function: A function that takes a label and returns a swapped label.
    """
    
    clients_dir = os.path.join(root_dir, 'clients')
    poisoned_clients_dir = os.path.join(root_dir, 'poisoned_clients')
    
    num_folders = count_folders(clients_dir)

    # Create the poisoned_clients directory if it does not exist
    if not os.path.exists(poisoned_clients_dir):
        os.makedirs(poisoned_clients_dir)

    # Check if the clients directory exists
    if not os.path.exists(clients_dir):
        return "Clients directory does not exist."

    num_pois_folders = int(p_ratio * num_folders)
    i = 0
            
    for folder in sorted(os.listdir(clients_dir)):
        
        folder_path = os.path.join(clients_dir, folder)

        # Check if the folder is a directory and named with a number
        if os.path.isdir(folder_path) and folder.isdigit():
            mnist_file = os.path.join(folder_path, 'mnist.pt')
            
            # Check if mnist.pt exists in this folder
            if os.path.isfile(mnist_file):
                
                # Load mnist.pt file
                data = torch.load(mnist_file)
                if i < num_pois_folders:
                
                    # Swap labels in y_train
                    y_train_swapped = [swap_function(label.item()) for label in data['y_train']]
                    data['y_train'] = torch.tensor(y_train_swapped)
                

                # Define the poisoned clients subdirectory
                poisoned_subdir = os.path.join(poisoned_clients_dir, folder)
                if not os.path.exists(poisoned_subdir):
                    os.makedirs(poisoned_subdir)

                # Define the path for the poisoned mnist file
                poisoned_file_path = os.path.join(poisoned_subdir, 'mnist.pt')

                # Save the modified mnist.pt file in the corresponding poisoned_clients subdirectory
                torch.save(data, poisoned_file_path)


                i += 1



def swap_function(label):
    choices = [i for i in range(10) if i != label]
    return random.choice(choices)




def show_data(path,nr_of_clients):
    # Loop through each file
    for i in range(1, nr_of_clients+1):
        # Construct the file path
        file = f"{path}/{i}/mnist.pt"

        # Load the file
        data = torch.load(file)

        # Check the type and contents of the loaded data
        print(f"\nClient {i}:")
        print(data["y_train"])
        print(len(data["y_train"]))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python poison_data.py <root_dir> <p_ratio>")
        sys.exit(1)

    root_dir = sys.argv[1]
    p_ratio = float(sys.argv[2])

    # Assuming you always want to use example_swap_function for now
    label_flip(root_dir, swap_function, p_ratio)