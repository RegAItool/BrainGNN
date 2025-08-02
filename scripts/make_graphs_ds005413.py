import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.maskers import NiftiLabelsMasker
from torch_geometric.data import Data
import torch

AAL_PATH = 'imports/BrainNetViewer_20191031/Data/ExampleFiles/AAL90/aal.nii'
DATASET_DIR = 'data/pain_data/ds005413'
GRAPH_DIR = os.path.join(DATASET_DIR, 'graphs')
FC_DIR = os.path.join(DATASET_DIR, 'fc')
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(FC_DIR, exist_ok=True)

min_required_length = 3  # 最小帧数门槛，可根据需要调整

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
            base = fname.replace('_bold.nii.gz', '')
            events_path = os.path.join(sub_dir, base + '_events.tsv')
            if not os.path.exists(events_path):
                print(f'No events file for {fmri_path}')
                continue
            events = pd.read_csv(events_path, sep='\t')
            # 以每个trial为单位，标签为pain_rating（如有）或trial_type
            total_trials = 0
            kept_trials = 0
            for idx, row in events.iterrows():
                total_trials += 1
                # 优先用pain_rating，否则用trial_type
                if 'pain_rating' in row:
                    try:
                        label = float(row['pain_rating'])
                    except:
                        continue
                elif 'trial_type' in row:
                    label = 1 if row['trial_type'] == 'high' else 0
                else:
                    print(f'No valid label for trial {idx} in {events_path}')
                    continue
                onset = float(row['onset'])
                duration = float(row['duration'])
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
                # 自动读取TR
                img = nib.load(fmri_path)
                TR = img.header.get_zooms()[-1]
                start_vol = int(onset // TR)
                end_vol = int((onset + duration) // TR)
                if end_vol <= start_vol or end_vol > time_series.shape[0]:
                    print(f'Skip trial {idx} in {fmri_path} due to invalid time window')
                    continue
                trial_ts = time_series[start_vol:end_vol]
                if trial_ts.shape[0] < min_required_length:
                    print(f'Skip trial {idx} in {fmri_path} due to too short segment (length={trial_ts.shape[0]}, min_required_length={min_required_length})')
                    continue
                kept_trials += 1
                fc = np.corrcoef(trial_ts.T)
                fc = np.nan_to_num(fc)
                fc_save_path = os.path.join(FC_DIR, f'{sub}_{base}_trial{idx}_fc.npy')
                np.save(fc_save_path, fc)
                n_roi = fc.shape[0]
                edge_index = np.array(np.nonzero(np.ones((n_roi, n_roi))))
                edge_attr = fc[edge_index[0], edge_index[1]]
                x = trial_ts.mean(axis=0, keepdims=True).T  # [n_roi, 1]
                y = torch.tensor([label], dtype=torch.float)
                data = Data(x=torch.tensor(x, dtype=torch.float),
                            edge_index=torch.tensor(edge_index, dtype=torch.long),
                            edge_attr=torch.tensor(edge_attr, dtype=torch.float),
                            y=y)
                # 自动补全task_type字段
                data.task_type = torch.tensor([3])  # ds005413: stimulus_class任务
                graph_save_path = os.path.join(GRAPH_DIR, f'{sub}_{base}_trial{idx}_graph.pt')
                torch.save(data, graph_save_path)
                print(f'Saved: {graph_save_path} and {fc_save_path}') 

# 统计trial保留率
print("\n=== Trial 保留统计 ===")
print(f"总trial数: {total_trials}")
print(f"保留trial数: {kept_trials}")
print(f"保留率: {kept_trials/total_trials:.2%}" if total_trials > 0 else "无有效trial") 