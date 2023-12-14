import torch

def check_cuda_availability():
    if torch.cuda.is_available():
        print("CUDA is available. You can use GPU acceleration.")
    else:
        print("CUDA is not available. Running on CPU.")

check_cuda_availability()
