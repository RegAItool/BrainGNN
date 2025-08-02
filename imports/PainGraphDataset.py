import os
import torch
from torch_geometric.data import Dataset, Data

class PainGraphDataset(Dataset):
    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir
        self.pt_files = []
        
        # Filter for valid .pt files
        for f in os.listdir(root_dir):
            if f.endswith('.pt'):
                file_path = os.path.join(root_dir, f)
                try:
                    # Test if the file can be loaded
                    test_data = torch.load(file_path)
                    if hasattr(test_data, 'x') and hasattr(test_data, 'y'):
                        self.pt_files.append(file_path)
                except:
                    print(f"Skipping corrupted file: {f}")
                    continue
        
        self.pt_files.sort()
        print(f"Loaded {len(self.pt_files)} valid graph files")

    def len(self):
        return len(self.pt_files)

    def get(self, idx):
        file_path = self.pt_files[idx]
        data = torch.load(file_path)
        # Ensure 'pos' attribute exists and is not None, as it's required by MyNNConv
        if not hasattr(data, 'pos') or data.pos is None:
            data.pos = torch.eye(data.x.size(0))
        # Remove the 'dataset' attribute if it exists to avoid collation issues
        if hasattr(data, 'dataset'):
            delattr(data, 'dataset')
        return data 