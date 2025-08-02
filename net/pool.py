import torch
import torch.nn.functional as F
from torch_geometric.nn import TopKPooling
from torch.nn import Linear

class TopKPool(torch.nn.Module):
    def __init__(self, in_channels, ratio, R):
        super(TopKPool, self).__init__()
        self.in_channels = in_channels
        self.ratio = ratio
        self.R = R # Total number of ROIs in the original graph
        self.k = int(R * ratio) # Number of nodes to keep
        
        # The TopKPooling layer from PyG does most of the work.
        # We wrap it to handle the score projection.
        self.pool = TopKPooling(in_channels, self.ratio)
        
    def forward(self, x, edge_index, edge_attr=None, batch=None):
        # The standard TopKPooling returns the pooled features, edges, etc.
        x, edge_index, edge_attr, batch, perm, score = self.pool(x, edge_index, edge_attr, batch)
        return x, edge_index, edge_attr, batch, perm, score 