import torch
import torch.nn.functional as F
from torch_geometric.data import Data, DataLoader
from imports.PainGraphDataset import PainGraphDataset
from net.multitask_braingnn import MultiTaskBrainGNN
import os

def debug_model():
    print("Starting debug...")
    
    # Load a single sample
    dataset = PainGraphDataset('data/pain_data/all_graphs')
    print(f"Dataset size: {len(dataset)}")
    
    # Get first sample
    sample_data = dataset[0]
    print(f"Sample data x.shape: {sample_data.x.shape}")
    print(f"Sample data edge_index.shape: {sample_data.edge_index.shape}")
    print(f"Sample data edge_attr.shape: {sample_data.edge_attr.shape}")
    print(f"Sample data pos.shape: {sample_data.pos.shape}")
    print(f"Sample data y: {sample_data.y}")
    
    # Create model
    num_features = sample_data.x.size(1)
    n_roi = sample_data.x.size(0)
    print(f"num_features: {num_features}, n_roi: {n_roi}")
    
    device = torch.device('cpu')
    model = MultiTaskBrainGNN(in_dim=num_features, hidden_dim=32, n_roi=n_roi).to(device)
    print("Model created successfully")
    
    # Test forward pass
    print("Testing forward pass...")
    sample_data = sample_data.to(device)
    
    try:
        with torch.no_grad():
            # Set model to eval mode to avoid BatchNorm issues
            model.eval()
            out, task_kind = model(sample_data)
            print(f"Forward pass successful! Output shape: {out.shape}, task_kind: {task_kind}")
    except Exception as e:
        print(f"Forward pass failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_model() 