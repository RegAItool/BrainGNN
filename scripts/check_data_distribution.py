import os
import numpy as np
import torch
from imports.read_abide_stats_parall import read_sigle_data
from torch_geometric.data import Data

raw_dir = './data/ABIDE_pcp/cpac/filt_noglobal/raw'
all_files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.h5')])
np.random.seed(42)
np.random.shuffle(all_files)
n_subjects = len(all_files)
n_test = n_subjects // 5
n_val = n_subjects // 5
n_train = n_subjects - n_test - n_val
test_files = all_files[:n_test]
val_files = all_files[n_test:n_test+n_val]
train_files = all_files[n_test+n_val:]

def load_labels_and_feats(file_list):
    labels = []
    feats = []
    for fname in file_list:
        edge_att, edge_index, att, label, num_nodes = read_sigle_data(raw_dir, fname)
        labels.append(label)
        feats.append(att)
    return np.array(labels), feats

train_labels, train_feats = load_labels_and_feats(train_files)
val_labels, val_feats = load_labels_and_feats(val_files)
test_labels, test_feats = load_labels_and_feats(test_files)

print('Train set:')
print('  样本数:', len(train_labels))
print('  类别分布:', np.unique(train_labels, return_counts=True))
print('  第一个样本特征均值/方差:', np.mean(train_feats[0]), np.std(train_feats[0]))
print('  第一个样本前5节点特征:', train_feats[0][:5])

print('Val set:')
print('  样本数:', len(val_labels))
print('  类别分布:', np.unique(val_labels, return_counts=True))

print('Test set:')
print('  样本数:', len(test_labels))
print('  类别分布:', np.unique(test_labels, return_counts=True)) 