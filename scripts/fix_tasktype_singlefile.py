import sys
import torch

def infer_task_type(data, fname):
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
    if dataset == 'ds000140':
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
    if len(sys.argv) != 2:
        print('Usage: python fix_tasktype_singlefile.py <pt_file>')
        sys.exit(1)
    fpath = sys.argv[1]
    try:
        data = torch.load(fpath)
        ttype = infer_task_type(data, fpath)
        data.task_type = torch.tensor([ttype])
        torch.save(data, fpath)
        print(f"[OK] {fpath} -> task_type={ttype}")
    except Exception as e:
        print(f"[FAIL] {fpath}: {e}")

if __name__ == '__main__':
    main() 