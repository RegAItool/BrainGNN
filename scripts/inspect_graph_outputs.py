import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch_geometric.data import Data

DATA_ROOT = 'data/pain_data'
REPORT_PATH = 'results/graph_inspect_report.txt'
IMG_DIR = 'results/inspect_figs'
os.makedirs(IMG_DIR, exist_ok=True)

report_lines = []

def inspect_pt(pt_path):
    data = torch.load(pt_path)
    info = f"{pt_path}: x.shape={getattr(data, 'x', None).shape if hasattr(data, 'x') else None}, " \
           f"edge_index.shape={getattr(data, 'edge_index', None).shape if hasattr(data, 'edge_index') else None}, " \
           f"edge_attr.shape={getattr(data, 'edge_attr', None).shape if hasattr(data, 'edge_attr') else None}, " \
           f"y={getattr(data, 'y', None)}"
    return info, data

def inspect_npy(npy_path):
    arr = np.load(npy_path)
    info = f"{npy_path}: shape={arr.shape}, min={arr.min():.3f}, max={arr.max():.3f}, mean={arr.mean():.3f}"
    return info, arr

for ds in sorted(os.listdir(DATA_ROOT)):
    ds_dir = os.path.join(DATA_ROOT, ds)
    if not os.path.isdir(ds_dir):
        continue
    graph_dir = os.path.join(ds_dir, 'graphs')
    fc_dir = os.path.join(ds_dir, 'fc')
    pt_files = [f for f in os.listdir(graph_dir)] if os.path.exists(graph_dir) else []
    npy_files = [f for f in os.listdir(fc_dir)] if os.path.exists(fc_dir) else []
    report_lines.append(f"=== {ds} ===\n.pt files: {len(pt_files)}\n.npy files: {len(npy_files)}")
    # 随机抽样一个.pt和一个.npy做详细可视化
    if pt_files:
        pt_path = os.path.join(graph_dir, pt_files[0])
        info, data = inspect_pt(pt_path)
        report_lines.append('Sample .pt: ' + info)
        # 可视化x
        plt.figure(figsize=(8,2))
        plt.title(f"{ds} x (feature)")
        plt.imshow(data.x.cpu().numpy(), aspect='auto', cmap='viridis')
        plt.colorbar()
        plt.savefig(os.path.join(IMG_DIR, f'{ds}_sample_x.png'))
        plt.close()
    if npy_files:
        npy_path = os.path.join(fc_dir, npy_files[0])
        info, arr = inspect_npy(npy_path)
        report_lines.append('Sample .npy: ' + info)
        # 可视化FC
        plt.figure(figsize=(5,4))
        plt.title(f"{ds} FC matrix")
        plt.imshow(arr, cmap='bwr', vmin=-1, vmax=1)
        plt.colorbar()
        plt.savefig(os.path.join(IMG_DIR, f'{ds}_sample_fc.png'))
        plt.close()

with open(REPORT_PATH, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"报告已保存到 {REPORT_PATH}，可视化图片在 {IMG_DIR}/") 