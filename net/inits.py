import torch
import math

def uniform(size, tensor):
    """
    Uniform weight initialization.
    """
    if tensor is not None:
        bound = 1.0 / math.sqrt(size)
        tensor.data.uniform_(-bound, bound) 