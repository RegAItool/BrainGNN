import torch, os

root = 'data/pain_data/all_graphs'
files = [f for f in os.listdir(root) if f.endswith('.pt')]
files.sort()
for f in files:
    try:
        data = torch.load(os.path.join(root, f))
        if data.x.shape[1] == 200:
            print(f"{f}: x.shape = {data.x.shape}")
    except Exception as e:
        print(f"Skipping {f}: {e}") 