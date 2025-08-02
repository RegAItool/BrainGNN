import os
import torch
from tqdm import tqdm

def infer_task_type(data, fname):
    # 优先用dataset字段，否则用文件名判断
    dataset = getattr(data, 'dataset', None)
    if dataset is None or dataset == 'unknown':
        if 'ds000140' in fname:
            dataset = 'ds000140'
        elif 'ds003836' in fname:
            dataset = 'ds003836'
        elif 'ds005413' in fname:
            dataset = 'ds005413'
        else:
            return -1
    # 规则分配
    if dataset == 'ds000140':
        # 性别分类优先（假设y为0/1），否则年龄回归
        if hasattr(data, 'y') and data.y.numel() == 1 and int(data.y.item()) in [0, 1]:
            return 0
        else:
            return 2
    elif dataset == 'ds003836':
        return 3
    elif dataset == 'ds005413':
        return 1
    else:
        return -1

def main():
    root = 'data/pain_data/all_graphs'
    files = [f for f in os.listdir(root) if f.endswith('.pt')]
    for fname in tqdm(files):
        fpath = os.path.join(root, fname)
        try:
            data = torch.load(fpath)
            ttype = infer_task_type(data, fname)
            data.task_type = torch.tensor([ttype])
            torch.save(data, fpath)
        except Exception as e:
            print(f"Failed to process {fname}: {e}")

if __name__ == '__main__':
    main() 