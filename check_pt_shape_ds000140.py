import torch, os

root = 'data/pain_data/ds000140/graphs'
files = [f for f in os.listdir(root) if f.endswith('.pt')]
files.sort()
for i, f in enumerate(files[:10]):  # 只看前10个
    data = torch.load(os.path.join(root, f))
    print(f"{f}: x.shape = {data.x.shape}") 