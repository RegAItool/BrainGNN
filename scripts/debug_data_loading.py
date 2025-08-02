import os
import numpy as np
import torch
import deepdish as dd
from imports.read_abide_stats_parall import read_sigle_data

raw_dir = './data/ABIDE_pcp/cpac/filt_noglobal/raw'
all_files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.h5')])

# 检查第一个文件
test_file = all_files[0]
print(f"检查文件: {test_file}")

# 直接加载h5文件
temp = dd.io.load(os.path.join(raw_dir, test_file))
print("H5文件内容:")
for key in temp.keys():
    print(f"  {key}: {type(temp[key])}")

# 检查pcorr矩阵
pcorr = np.abs(temp['pcorr'][()])
print(f"\npcorr矩阵:")
print(f"  形状: {pcorr.shape}")
print(f"  数据类型: {pcorr.dtype}")
print(f"  最小值: {np.min(pcorr)}")
print(f"  最大值: {np.max(pcorr)}")
print(f"  均值: {np.mean(pcorr)}")
print(f"  是否有inf: {np.any(np.isinf(pcorr))}")
print(f"  是否有nan: {np.any(np.isnan(pcorr))}")
if np.any(np.isinf(pcorr)) or np.any(np.isnan(pcorr)):
    print(f"  inf位置: {np.where(np.isinf(pcorr))}")
    print(f"  nan位置: {np.where(np.isnan(pcorr))}")

# 检查corr特征
corr = temp['corr'][()]
print(f"\ncorr特征:")
print(f"  形状: {corr.shape}")
print(f"  数据类型: {corr.dtype}")
print(f"  最小值: {np.min(corr)}")
print(f"  最大值: {np.max(corr)}")
print(f"  均值: {np.mean(corr)}")
print(f"  是否有inf: {np.any(np.isinf(corr))}")
print(f"  是否有nan: {np.any(np.isnan(corr))}")
if np.any(np.isinf(corr)) or np.any(np.isnan(corr)):
    print(f"  inf位置: {np.where(np.isinf(corr))}")
    print(f"  nan位置: {np.where(np.isnan(corr))}")

# 检查label
label = temp['label'][()]
print(f"\nlabel:")
print(f"  值: {label}")
print(f"  类型: {type(label)}")

# 使用read_sigle_data函数
print(f"\n使用read_sigle_data函数:")
edge_att, edge_index, att, label, num_nodes = read_sigle_data(raw_dir, test_file)
print(f"  返回的att形状: {att.shape}")
print(f"  返回的att是否有inf: {np.any(np.isinf(att))}")
print(f"  返回的att是否有nan: {np.any(np.isnan(att))}")
print(f"  返回的att均值: {np.mean(att)}")
print(f"  返回的att方差: {np.var(att)}")

# 检查多个文件
print(f"\n检查前5个文件:")
for i in range(min(5, len(all_files))):
    fname = all_files[i]
    temp = dd.io.load(os.path.join(raw_dir, fname))
    pcorr = np.abs(temp['pcorr'][()])
    corr = temp['corr'][()]
    
    print(f"  文件{i+1}: {fname}")
    print(f"    pcorr有inf: {np.any(np.isinf(pcorr))}, 有nan: {np.any(np.isnan(pcorr))}")
    print(f"    corr有inf: {np.any(np.isinf(corr))}, 有nan: {np.any(np.isnan(corr))}")
    print(f"    corr均值: {np.mean(corr):.6f}, 方差: {np.var(corr):.6f}") 