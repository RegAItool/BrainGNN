from imports.PainGraphDataset import PainGraphDataset
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    dataset = PainGraphDataset('data/graph_data')
    loader = DataLoader(dataset, batch_size=1, shuffle=False)
    for i, data in enumerate(loader):
        print(f"Sample {i}: x={data.x.shape}, y={data.y}, task_type={data.task_type}, dataset={data.dataset}")
        if hasattr(data, 'edge_index'):
            print(f"  edge_index: {data.edge_index.shape}")
        if hasattr(data, 'edge_attr'):
            print(f"  edge_attr: {data.edge_attr.shape}")
        if hasattr(data, 'pos'):
            print(f"  pos: {data.pos.shape}")
        if hasattr(data, 'batch'):
            print(f"  batch: {data.batch.shape}")
        if i >= 10:
            break 