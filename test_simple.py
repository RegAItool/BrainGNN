import torch
from imports.PainGraphDataset import PainGraphDataset
from net.braingnn import BrainGNN

print("Testing dataset loading...")
dataset = PainGraphDataset('/workspace/data/pain_data/all_graphs')
print(f"Dataset size: {len(dataset)}")

print("Testing data attributes...")
data = dataset[0]
print(f"x shape: {data.x.shape}")
print(f"pos shape: {data.pos.shape}")
print(f"batch shape: {data.batch.shape}")
print(f"y: {data.y}")

print("Testing model creation...")
num_features = data.x.size(1)
num_classes = len(torch.unique(torch.tensor([d.y.item() for d in dataset])))
print(f"num_features: {num_features}, num_classes: {num_classes}")

model = BrainGNN(num_features=num_features, num_classes=num_classes)
print("Model created successfully!")

print("Testing forward pass...")
out = model(data)
print(f"Output shape: {out.shape}")
print("Forward pass successful!")

print("All tests passed!") 