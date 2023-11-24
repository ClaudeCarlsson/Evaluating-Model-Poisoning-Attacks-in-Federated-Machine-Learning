#!/usr/bin/env python3

import torch
import os
import numpy as np
import sys


def count_folders(directory):
    """Count the number of folders in the specified directory."""
    if not os.path.exists(directory):
        return "Directory does not exist."

    folder_count = 0
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            folder_count += 1


    return folder_count


    
def add_backdoor_to_image(image):
    # The plus sign will be 3 pixels tall and wide

    image[0:3, 1] = 255
    image[1, 0:3] = 255
    return image



def backdoor_attack(path, target_label, fraction):
    """
    Adds a backdoor to the training images by adding a small white dot in the top left corner
    for a fraction of the mnist.pt files in numbered subfolders. The backdoor is only added to images
    with the specified target_label. Saves them in the backdoor_clients directory.

    :param path: The root directory where the 'clients' folder is located.
    :param target_label: The label for which the backdoor will be added.
    :param fraction: The fraction of clients that should have the backdoor.
    """
    clients_dir = os.path.join(path, 'clients')
    backdoor_clients_dir = os.path.join(path, 'backdoor_clients')

    num_folders = count_folders(clients_dir)
    num_backdoor_folders = int(fraction * num_folders)

    if not os.path.exists(backdoor_clients_dir):
        os.makedirs(backdoor_clients_dir)

    if not os.path.exists(clients_dir):
        return "Clients directory does not exist."

    i = 0
    for folder in sorted(os.listdir(clients_dir)):
        folder_path = os.path.join(clients_dir, folder)

        if os.path.isdir(folder_path) and folder.isdigit():
            mnist_file = os.path.join(folder_path, 'mnist.pt')

            if os.path.isfile(mnist_file):
                data = torch.load(mnist_file)

                if i < num_backdoor_folders:
                    x_train_backdoor = np.array(data['x_train'])
                    y_train = np.array(data['y_train'])

                    # Apply the backdoor only to images with the target label
                    for j in range(len(x_train_backdoor)):
                        if y_train[j] == target_label:
                            x_train_backdoor[j] = add_backdoor_to_image(x_train_backdoor[j])

                    data['x_train'] = torch.tensor(x_train_backdoor)

                backdoor_subdir = os.path.join(backdoor_clients_dir, folder)
                if not os.path.exists(backdoor_subdir):
                    os.makedirs(backdoor_subdir)

                backdoor_file_path = os.path.join(backdoor_subdir, 'mnist.pt')
                torch.save(data, backdoor_file_path)

                i += 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python backdoor_attack.py <root_dir> <target_label> <ratio_of_pois_clients>")
        sys.exit(1)

    root_dir = sys.argv[1]
    target_label = float(sys.argv[2])
    p_ratio = float(sys.argv[3])

    # Assuming you always want to use example_swap_function for now
    backdoor_attack(root_dir, target_label, p_ratio)