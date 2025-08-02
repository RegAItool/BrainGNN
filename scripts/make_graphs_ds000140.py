import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.maskers import NiftiLabelsMasker
from torch_geometric.data import Data
import torch

# 配置参数
AAL_PATH = 'imports/BrainNetViewer_20191031/Data/ExampleFiles/AAL90/aal.nii'
DATASET_DIR = 'data/pain_data/ds000140'
GRAPH_DIR = os.path.join(DATASET_DIR, 'graphs')
FC_DIR = os.path.join(DATASET_DIR, 'fc')
LABEL_FILE = os.path.join(DATASET_DIR, 'participants.tsv')

os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(FC_DIR, exist_ok=True)

# 读取标签
participants = pd.read_csv(LABEL_FILE, sep='\t')
sub2label = {}
for _, row in participants.iterrows():
    sub_id = row['participant_id']
    # 选择性别分类（M=0, F=1），如需年龄回归可改为 row['age']
    label = 0 if row['sex'] == 'M' else 1
    sub2label[sub_id] = label

# 遍历所有被试
for sub in sorted(os.listdir(DATASET_DIR)):
    if not sub.startswith('sub-'):
        continue
    sub_dir = os.path.join(DATASET_DIR, sub, 'func')
    if not os.path.isdir(sub_dir):
        continue
    for fname in os.listdir(sub_dir):
        if fname.endswith('_bold.nii.gz'):
            fmri_path = os.path.join(sub_dir, fname)
            print(f'Processing {fmri_path}')
            # 1. 提取ROI时序
            masker = NiftiLabelsMasker(labels_img=AAL_PATH, standardize=True)
            # 跳过空文件
            if os.path.getsize(fmri_path) == 0:
                print(f"⚠️ Skip empty file: {fmri_path}")
                continue
            try:
                time_series = masker.fit_transform(fmri_path)
            except Exception as e:
                print(f"❌ Error processing {fmri_path}: {e}")
                continue
            # 2. 计算FC矩阵
            fc = np.corrcoef(time_series.T)
            fc = np.nan_to_num(fc)
            # 3. 保存FC
            fc_save_path = os.path.join(FC_DIR, f'{sub}_fc.npy')
            np.save(fc_save_path, fc)
            # 4. 构建图结构
            n_roi = fc.shape[0]
            edge_index = np.array(np.nonzero(np.ones((n_roi, n_roi))))
            edge_attr = fc[edge_index[0], edge_index[1]]
            x = time_series.mean(axis=0, keepdims=True).T  # [n_roi, 1]，可自定义特征
            y = torch.tensor([sub2label[sub]], dtype=torch.long)
            data = Data(x=torch.tensor(x, dtype=torch.float),
                        edge_index=torch.tensor(edge_index, dtype=torch.long),
                        edge_attr=torch.tensor(edge_attr, dtype=torch.float),
                        y=y)
            # 自动补全task_type字段
            data.task_type = torch.tensor([0])  # ds000140: 性别任务
            # 5. 保存图结构
            graph_save_path = os.path.join(GRAPH_DIR, f'{sub}_graph.pt')
            torch.save(data, graph_save_path)
            print(f'Saved: {graph_save_path} and {fc_save_path}') 