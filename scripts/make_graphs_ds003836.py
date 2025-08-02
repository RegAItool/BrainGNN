import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.maskers import NiftiLabelsMasker
from torch_geometric.data import Data
import torch

AAL_PATH = 'imports/BrainNetViewer_20191031/Data/ExampleFiles/AAL90/aal.nii'
DATASET_DIR = 'data/pain_data/ds003836'
GRAPH_DIR = os.path.join(DATASET_DIR, 'graphs')
FC_DIR = os.path.join(DATASET_DIR, 'fc')
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(FC_DIR, exist_ok=True)

# 遍历所有被试
for sub in sorted(os.listdir(DATASET_DIR)):
    print(f"Checking subject: {sub}")
    if not sub.startswith('sub-'):
        continue
    sub_dir = os.path.join(DATASET_DIR, sub, 'func')
    if not os.path.isdir(sub_dir):
        print(f"  No func dir for {sub}")
        continue
    for fname in os.listdir(sub_dir):
        print(f"  Found file: {fname}")
        if fname.endswith('_bold.nii') or fname.endswith('_bold.nii.gz'):
            fmri_path = os.path.join(sub_dir, fname)
            base = fname.replace('_bold.nii', '').replace('_bold.nii.gz', '')
            events_path = os.path.join(sub_dir, base + '_events.tsv')
            print(f"    Processing fMRI: {fmri_path}")
            if not os.path.exists(events_path):
                print(f'    No events file for {fmri_path}')
                continue
            events = pd.read_csv(events_path, sep='\t')
            # 只处理high/low trial
            for idx, row in events.iterrows():
                trial_type = row['trial_type']
                if trial_type not in ['high', 'low']:
                    continue
                onset = float(row['onset'])
                duration = float(row['duration'])
                if duration == 0:
                    duration = 6.0  # 默认窗口长度6秒
                # 1. 提取该trial的fMRI片段
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
                tr = 2.0  # 默认TR=2s，如需自动读取可扩展
                start_vol = int(onset // tr)
                end_vol = int((onset + duration) // tr)
                if end_vol <= start_vol or end_vol > time_series.shape[0]:
                    print(f'Skip trial {idx} in {fmri_path} due to invalid time window')
                    continue
                trial_ts = time_series[start_vol:end_vol]
                if trial_ts.shape[0] < 2:
                    print(f'Skip trial {idx} in {fmri_path} due to too short segment')
                    continue
                # 2. 计算FC
                fc = np.corrcoef(trial_ts.T)
                fc = np.nan_to_num(fc)
                # 3. 保存FC
                fc_save_path = os.path.join(FC_DIR, f'{sub}_{base}_trial{idx}_fc.npy')
                np.save(fc_save_path, fc)
                # 4. 构建图结构
                n_roi = fc.shape[0]
                edge_index = np.array(np.nonzero(np.ones((n_roi, n_roi))))
                edge_attr = fc[edge_index[0], edge_index[1]]
                x = trial_ts.mean(axis=0, keepdims=True).T  # [n_roi, 1]
                y = torch.tensor([1 if trial_type == 'high' else 0], dtype=torch.long)
                data = Data(x=torch.tensor(x, dtype=torch.float),
                            edge_index=torch.tensor(edge_index, dtype=torch.long),
                            edge_attr=torch.tensor(edge_attr, dtype=torch.float),
                            y=y)
                # 自动补全task_type字段
                data.task_type = torch.tensor([1])  # ds003836: pain_level任务
                # 5. 保存图结构
                graph_save_path = os.path.join(GRAPH_DIR, f'{sub}_{base}_trial{idx}_graph.pt')
                if os.path.exists(graph_save_path):
                    print(f"Skip existing: {graph_save_path}")
                    continue
                torch.save(data, graph_save_path)
                print(f'Saved: {graph_save_path} and {fc_save_path}') 