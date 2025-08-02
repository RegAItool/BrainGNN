import torch

checkpoint = torch.load('./model/best_pain_model.pth', map_location='cpu')
for k, v in checkpoint.items():
    if '.weight' in k and len(v.shape) == 2:
        print(f"{k}: {v.shape}")
        break 