import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from imports.PainGraphDataset import PainGraphDataset
from net.braingnn import BrainGNN
import os

print("Starting simple training test...")

# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# 加载数据集
print("Loading dataset...")
dataset = PainGraphDataset('/workspace/data/pain_data/all_graphs')
print(f"Dataset size: {len(dataset)}")

# 创建数据加载器
train_loader = DataLoader(dataset, batch_size=4, shuffle=True)
print("DataLoader created")

# 获取样本数据以确定输入维度
sample_data = dataset[0]
num_features = sample_data.x.size(1)
num_classes = len(torch.unique(torch.tensor([data.y.item() for data in dataset])))
print(f"Input features: {num_features}")
print(f"Number of classes: {num_classes}")

# 创建模型
model = BrainGNN(num_features=num_features, num_classes=num_classes).to(device)
print(f"Model created with {sum(p.numel() for p in model.parameters())} parameters")

# 优化器
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练一个epoch
print("Starting training...")
model.train()
for batch_idx, batch in enumerate(train_loader):
    if batch_idx >= 2:  # 只训练前2个batch
        break
    
    batch = batch.to(device)
    print(f"Batch {batch_idx}: x shape {batch.x.shape}, y shape {batch.y.shape}")
    
    optimizer.zero_grad()
    out = model(batch)
    print(f"Output shape: {out.shape}")
    
    loss = F.cross_entropy(out, batch.y)
    print(f"Loss: {loss.item():.4f}")
    
    loss.backward()
    optimizer.step()
    
    print(f"Batch {batch_idx} completed successfully!")

print("Training test completed successfully!") 