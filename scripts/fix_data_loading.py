import os
import numpy as np
import torch
import deepdish as dd
from imports.read_abide_stats_parall import read_sigle_data
from networkx.convert_matrix import from_numpy_array as from_numpy_matrix
import networkx as nx
from torch_geometric.utils import remove_self_loops
from torch_sparse import coalesce
from imports.gdc import GDC
from torch_geometric.data import Data

def fix_inf_nan_matrix(matrix, diagonal_value=1.0):
    """修复矩阵中的inf/nan值"""
    # 复制矩阵避免修改原始数据
    fixed_matrix = matrix.copy()
    
    # 替换inf为有限值
    fixed_matrix = np.nan_to_num(fixed_matrix, nan=0.0, posinf=1.0, neginf=-1.0)
    
    # 将对角线设为指定值（通常是1.0，表示自相关）
    np.fill_diagonal(fixed_matrix, diagonal_value)
    
    return fixed_matrix

def read_sigle_data_fixed(data_dir, filename, use_gdc=False):
    """修复版本的read_sigle_data函数"""
    temp = dd.io.load(os.path.join(data_dir, filename))
    
    # 修复pcorr矩阵
    pcorr = np.abs(temp['pcorr'][()])
    pcorr_fixed = fix_inf_nan_matrix(pcorr, diagonal_value=1.0)
    
    # 修复corr矩阵
    corr = temp['corr'][()]
    corr_fixed = fix_inf_nan_matrix(corr, diagonal_value=1.0)
    
    # 使用修复后的数据
    num_nodes = pcorr_fixed.shape[0]
    G = from_numpy_matrix(pcorr_fixed)
    A = nx.to_scipy_sparse_array(G)
    adj = A.tocoo()
    edge_att = np.zeros(len(adj.row))
    for i in range(len(adj.row)):
        edge_att[i] = pcorr_fixed[adj.row[i], adj.col[i]]
    
    edge_index = np.stack([adj.row, adj.col])
    edge_index, edge_att = remove_self_loops(torch.from_numpy(edge_index), torch.from_numpy(edge_att))
    edge_index = edge_index.long()
    edge_index, edge_att = coalesce(edge_index, edge_att, num_nodes, num_nodes)
    
    label = temp['label'][()]
    
    if use_gdc:
        # GDC处理逻辑保持不变
        att_torch = torch.from_numpy(corr_fixed).float()
        y_torch = torch.from_numpy(np.array(label)).long()
        data = Data(x=att_torch, edge_index=edge_index.long(), y=y_torch, edge_attr=edge_att)
        data.edge_attr = data.edge_attr.squeeze()
        gdc = GDC(self_loop_weight=1, normalization_in='sym',
                  normalization_out='col',
                  diffusion_kwargs=dict(method='ppr', alpha=0.2),
                  sparsification_kwargs=dict(method='topk', k=20, dim=0), exact=True)
        data = gdc(data)
        return data.edge_attr.data.numpy(), data.edge_index.data.numpy(), data.x.data.numpy(), data.y.data.item(), num_nodes
    else:
        return edge_att.data.numpy(), edge_index.data.numpy(), corr_fixed, label, num_nodes

# 测试修复效果
raw_dir = './data/ABIDE_pcp/cpac/filt_noglobal/raw'
test_file = sorted([f for f in os.listdir(raw_dir) if f.endswith('.h5')])[0]

print("测试修复效果:")
edge_att, edge_index, att, label, num_nodes = read_sigle_data_fixed(raw_dir, test_file)
print(f"修复后att形状: {att.shape}")
print(f"修复后att是否有inf: {np.any(np.isinf(att))}")
print(f"修复后att是否有nan: {np.any(np.isnan(att))}")
print(f"修复后att均值: {np.mean(att):.6f}")
print(f"修复后att方差: {np.var(att):.6f}")
print(f"修复后att对角线前5个值: {np.diag(att)[:5]}") 