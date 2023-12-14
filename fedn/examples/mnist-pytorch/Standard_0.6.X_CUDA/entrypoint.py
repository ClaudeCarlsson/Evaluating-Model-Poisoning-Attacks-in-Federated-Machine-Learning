#!./.mnist-pytorch/bin/python
import collections
import math
import os

import docker
import fire
import torch

from fedn.utils.helpers import get_helper, save_metadata, save_metrics

#### Cuda client

HELPER_MODULE = 'pytorchhelper'
NUM_CLASSES = 10


def _get_data_path():
    """ For test automation using docker-compose. """
    # Figure out FEDn client number from container name
    client = docker.from_env()
    container = client.containers.get(os.environ['HOSTNAME'])
    number = container.name[-1]

    # Return data path
    return f"/var/data/clients/{number}/mnist.pt"


def _compile_model():
    """ Compile the pytorch model.

    :return: The compiled model.
    :rtype: torch.nn.Module
    """
    class Net(torch.nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = torch.nn.Linear(784, 64)
            self.fc2 = torch.nn.Linear(64, 32)
            self.fc3 = torch.nn.Linear(32, 10)

        def forward(self, x):
            x = torch.nn.functional.relu(self.fc1(x.reshape(x.size(0), 784)))
            x = torch.nn.functional.dropout(x, p=0.5, training=self.training)
            x = torch.nn.functional.relu(self.fc2(x))
            x = torch.nn.functional.log_softmax(self.fc3(x), dim=1)
            return x

    # Return model
    # Move model to GPU if available
    if torch.cuda.is_available():
        model = Net().to('cuda')
    else:
        model = Net()
    return model


def _load_data(data_path, is_train=True):
    """ Load data from disk. 

    :param data_path: Path to data file.
    :type data_path: str
    :param is_train: Whether to load training or test data.
    :type is_train: bool
    :return: Tuple of data and labels.
    :rtype: tuple
    """
    if data_path is None:
        data = torch.load(_get_data_path())
    else:
        data = torch.load(data_path)

    if is_train:
        X = data['x_train']
        y = data['y_train']
    else:
        X = data['x_test']
        y = data['y_test']

    # Normalize
    X = X / 255

    return X, y


def _save_model(model, out_path):
    """ Save model to disk. """
    # Get model weights as a state dictionary
    weights = model.state_dict()
    # Create a new OrderedDict to store CPU tensors
    weights_cpu = collections.OrderedDict()

    # Iterate through all model weights and move them to CPU
    for k, v in weights.items():
        weights_cpu[k] = v.cpu()

    # Use the helper to save the CPU tensors
    helper = get_helper(HELPER_MODULE)
    helper.save(weights_cpu, out_path)




def _load_model(model_path):
    """ Load model from disk.

    param model_path: The path to load from.
    :type model_path: str
    :return: The loaded model.
    :rtype: torch.nn.Module
    """
    helper = get_helper(HELPER_MODULE)
    weights_np = helper.load(model_path)
    weights = collections.OrderedDict()
    for w in weights_np:
        weights[w] = torch.tensor(weights_np[w])
    model = _compile_model()
    model.load_state_dict(weights)
    model.eval()
    return model


def init_seed(out_path='seed.npz'):
    """ Initialize seed model.

    :param out_path: The path to save the seed model to.
    :type out_path: str
    """
    # Init and save
    model = _compile_model()
    _save_model(model, out_path)


def train(in_model_path, out_model_path, data_path=None, batch_size=32, epochs=1, lr=0.01):
    """ Train model.

    :param in_model_path: The path to the input model.
    :type in_model_path: str
    :param out_model_path: The path to save the output model to.
    :type out_model_path: str
    :param data_path: The path to the data file.
    :type data_path: str
    :param batch_size: The batch size to use.
    :type batch_size: int
    :param epochs: The number of epochs to train.
    :type epochs: int
    :param lr: The learning rate to use.
    :type lr: float
    """
    # Load data
    x_train, y_train = _load_data(data_path)

    # Load model
    model = _load_model(in_model_path)
    # Move model to GPU if available
    if torch.cuda.is_available():
        model = model.to('cuda')

    # Train
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    n_batches = int(math.ceil(len(x_train) / batch_size))
    criterion = torch.nn.NLLLoss()
    for e in range(epochs):  # epoch loop
        for b in range(n_batches):  # batch loop
            # Retrieve current batch
            batch_x = x_train[b * batch_size:(b + 1) * batch_size]
            batch_y = y_train[b * batch_size:(b + 1) * batch_size]

            # Move batch to GPU if available
            if torch.cuda.is_available():
                batch_x = batch_x.to('cuda')
                batch_y = batch_y.to('cuda')

            # Train on batch
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()

            optimizer.step()
            # Log
            if b % 100 == 0:
                print(
                    f"Epoch {e}/{epochs-1} | Batch: {b}/{n_batches-1} | Loss: {loss.item()}")

    # Metadata needed for aggregation server side
    metadata = {
        'num_examples': len(x_train),
        'batch_size': batch_size,
        'epochs': epochs,
        'lr': lr
    }

    # Save JSON metadata file
    save_metadata(metadata, out_model_path)

    # Save model update
    _save_model(model, out_model_path)


def validate(in_model_path, out_json_path, data_path=None):
    """ Validate model.

    :param in_model_path: The path to the input model.
    :type in_model_path: str
    :param out_json_path: The path to save the output JSON to.
    :type out_json_path: str
    :param data_path: The path to the data file.
    :type data_path: str
    """
    # Load data
    x_train, y_train = _load_data(data_path)
    x_test, y_test = _load_data(data_path, is_train=False)

    # Move data to GPU if available
    if torch.cuda.is_available():
        x_train = x_train.to('cuda')
        y_train = y_train.to('cuda')
        x_test = x_test.to('cuda')
        y_test = y_test.to('cuda')

    # Load model
    model = _load_model(in_model_path)
    # Move model to GPU if available
    if torch.cuda.is_available():
        model = model.to('cuda')

    # Evaluate
    criterion = torch.nn.NLLLoss()
    with torch.no_grad():
        train_out = model(x_train)
        training_loss = criterion(train_out, y_train)
        training_accuracy = torch.sum(torch.argmax(
            train_out, dim=1) == y_train) / len(train_out)
        test_out = model(x_test)
        test_loss = criterion(test_out, y_test)
        test_accuracy = torch.sum(torch.argmax(
            test_out, dim=1) == y_test) / len(test_out)

    # JSON schema
    report = {
        "training_loss": training_loss.item(),
        "training_accuracy": training_accuracy.item(),
        "test_loss": test_loss.item(),
        "test_accuracy": test_accuracy.item(),
    }

    # Save JSON
    save_metrics(report, out_json_path)


if __name__ == '__main__':
    fire.Fire({
        'init_seed': init_seed,
        'train': train,
        'validate': validate,
        # '_get_data_path': _get_data_path,  # for testing
    })
###
### Cuda Client
###