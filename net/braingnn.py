import torch
import torch.nn as nn
import torch.nn.functional as F
from net.braingraphconv import MyNNConv
from net.pool import TopKPool
import numpy as np
from torch_geometric.nn import global_max_pool, global_mean_pool

class Network(torch.nn.Module):
    def __init__(self, indim, ratio, nclass, k=8, R=116):
        super(Network, self).__init__()
        self.indim = indim
        self.k = k
        self.R = R 

        self.dim1 = 32
        self.dim2 = 32
        self.dim3 = 32

        self.n1 = nn.Sequential(nn.Linear(self.R, self.k, bias=False), nn.ReLU(), nn.Linear(self.k, self.dim1 * self.indim))
        self.conv1 = MyNNConv(self.indim, self.dim1, self.n1, aggr='mean')
        self.pool1 = TopKPool(self.dim1, ratio, R=self.R)

        self.n2 = nn.Sequential(nn.Linear(self.R, self.k, bias=False), nn.ReLU(), nn.Linear(self.k, self.dim2 * self.dim1))
        self.conv2 = MyNNConv(self.dim1, self.dim2, self.n2, aggr='mean')
        self.pool2 = TopKPool(self.dim2, ratio, R=self.R)

        self.n3 = nn.Sequential(nn.Linear(self.R, self.k, bias=False), nn.ReLU(), nn.Linear(self.k, self.dim3 * self.dim2))
        self.conv3 = MyNNConv(self.dim2, self.dim3, self.n3, aggr='mean')
        self.pool3 = TopKPool(self.dim3, ratio, R=self.R)
        
        self.fc1 = nn.Linear(self.dim3 * 2, 16)
        self.bn1 = nn.BatchNorm1d(16)
        self.fc2 = nn.Linear(16, nclass)

    def forward(self, x, edge_index, batch, edge_attr=None, pos=None):
        if pos is None:
            pos = torch.eye(x.size(0), device=x.device)

        x = self.conv1(x, edge_index, edge_attr, pos)
        x, edge_index, edge_attr, batch, perm1, score1 = self.pool1(x, edge_index, edge_attr, batch)
        pos = pos[perm1]
        x1 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = self.conv2(x, edge_index, edge_attr, pos)
        x, edge_index, edge_attr, batch, perm2, score2 = self.pool2(x, edge_index, edge_attr, batch)
        pos = pos[perm2]
        x2 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = self.conv3(x, edge_index, edge_attr, pos)
        x, edge_index, edge_attr, batch, perm3, score3 = self.pool3(x, edge_index, edge_attr, batch)
        x3 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)
        
        x = x1 + x2 + x3

        x = self.bn1(F.relu(self.fc1(x)))
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.log_softmax(self.fc2(x), dim=-1)

        return x, perm1, score1, perm2, score2, perm3, score3

BrainGNN = Network
