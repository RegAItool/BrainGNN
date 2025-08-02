import os
import torch

# 任务定义（可根据需要修改）
TASK_MAP = {
    'ds000140': {'gender': 0, 'age': 2},
    'ds005413': {'pain_level': 1},
    'ds003836': {'stimulus_class': 3},
}

# 你可以根据文件名或目录结构判断属于哪个任务
# 这里假设文件名包含数据集名和任务关键词

def infer_task_type_and_dataset(filename):
    fname = filename.lower()
    if 'ds000140' in fname:
        if 'gender' in fname:
            return 0, 'ds000140'
        if 'age' in fname:
            return 2, 'ds000140'
        # 默认性别
        return 0, 'ds000140'
    if 'ds005413' in fname:
        return 1, 'ds005413'
    if 'ds003836' in fname:
        return 3, 'ds003836'
    # fallback
    return -1, 'unknown'


def upgrade_all_pt_files(root_dir):
    for fname in os.listdir(root_dir):
        if not fname.endswith('.pt'):
            continue
        fpath = os.path.join(root_dir, fname)
        try:
            data = torch.load(fpath)
            # 已有task_type则跳过
            if hasattr(data, 'task_type') and hasattr(data, 'dataset'):
                continue
            task_type, dataset = infer_task_type_and_dataset(fname)
            data.task_type = torch.tensor([task_type])
            data.dataset = dataset
            torch.save(data, fpath)
            print(f'Upgraded {fname}: task_type={task_type}, dataset={dataset}')
        except Exception as e:
            print(f'Error processing {fname}: {e}')

if __name__ == '__main__':
    upgrade_all_pt_files('/workspace/data/pain_data/all_graphs') 