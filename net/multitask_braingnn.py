import torch
import torch.nn as nn
import torch.nn.functional as F
from net.braingnn import Network

class MultiTaskBrainGNN(nn.Module):
    def __init__(self, in_dim, hidden_dim=32, n_roi=None):
        super().__init__()
        # 动态确定ROI数量，如果没有指定就用默认值
        if n_roi is None:
            n_roi = 116
        # 共享GNN encoder
        self.encoder = Network(indim=in_dim, ratio=0.8, nclass=hidden_dim, k=8, R=n_roi)
        # 多任务head，按编号顺序：0-性别(2), 1-痛感(3), 2-年龄(1), 3-刺激(2)
        self.task_heads = nn.ModuleList([
            nn.Linear(hidden_dim, 2),   # 0: gender
            nn.Linear(hidden_dim, 3),   # 1: pain_level
            nn.Linear(hidden_dim, 1),   # 2: age (regression)
            nn.Linear(hidden_dim, 2),   # 3: stimulus_class
        ])
        self.task_types = ['cls', 'cls', 'reg', 'cls']

    def forward(self, data):
        x, *_ = self.encoder(data.x, data.edge_index, data.batch, data.edge_attr, data.pos)
        # 支持batch_size=1或同一batch同一task_type
        if hasattr(data, 'task_type'):
            task_id = int(data.task_type[0]) if isinstance(data.task_type, torch.Tensor) else int(data.task_type)
        else:
            task_id = 0
        out = self.task_heads[task_id](x)
        return out, self.task_types[task_id] 