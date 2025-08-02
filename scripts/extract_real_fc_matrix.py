#!/usr/bin/env python3
"""
从ABIDE数据中提取真实的FC矩阵
生成正确的BrainNet Viewer node和edge文件
"""

import numpy as np
import torch
import os
from sklearn.cluster import KMeans

def extract_real_fc_matrix():
    """从ABIDE数据中提取真实的FC矩阵"""
    print("🔍 从ABIDE数据中提取真实FC矩阵...")
    
    # 加载数据
    data_path = './data/ABIDE_pcp/cpac/filt_noglobal/processed/data.pt'
    data = torch.load(data_path)
    
    # 获取第一个样本的FC矩阵
    sample = data[0]
    print(f"样本特征形状: {sample.x.shape}")
    print(f"边索引形状: {sample.edge_index.shape}")
    print(f"边属性形状: {sample.edge_attr.shape}")
    
    # 从边索引和边属性重建FC矩阵
    num_nodes = sample.x.shape[1]  # 应该是200
    print(f"节点数: {num_nodes}")
    
    # 创建空的FC矩阵
    fc_matrix = np.zeros((num_nodes, num_nodes))
    
    # 从边索引和边属性填充FC矩阵
    edge_index = sample.edge_index.numpy()
    edge_attr = sample.edge_attr.numpy().flatten()
    
    for i in range(edge_index.shape[1]):
        row = edge_index[0, i]
        col = edge_index[1, i]
        weight = edge_attr[i]
        fc_matrix[row, col] = weight
    
    print(f"FC矩阵形状: {fc_matrix.shape}")
    print(f"FC矩阵非零元素: {np.count_nonzero(fc_matrix)}")
    print(f"FC矩阵范围: [{np.min(fc_matrix):.4f}, {np.max(fc_matrix):.4f}]")
    
    return fc_matrix

def create_brainnet_files(fc_matrix, importance_scores):
    """创建BrainNet Viewer文件 - 6列标准格式"""
    print("📝 创建BrainNet Viewer文件...")
    
    # 确保FC矩阵是100x100
    if fc_matrix.shape[0] > 100:
        print(f"截取前100x100的FC矩阵...")
        fc_matrix = fc_matrix[:100, :100]
    
    # 确保重要性分数是100个
    if len(importance_scores) > 100:
        print(f"截取前100个重要性分数...")
        importance_scores = importance_scores[:100]
    
    # 生成100个节点的3D坐标（仿真大脑空间，MNI坐标范围）
    np.random.seed(42)
    # MNI坐标范围：X[-90,90], Y[-126,90], Z[-72,108]
    coords = np.random.uniform([-90, -126, -72], [90, 90, 108], size=(100, 3))
    
    # 节点大小（基于重要性，5-20的范围）
    node_sizes = importance_scores * 15 + 5
    
    # 颜色值（基于重要性，0-1范围）
    # 归一化重要性分数到0-1范围
    color_values = (importance_scores - np.min(importance_scores)) / (np.max(importance_scores) - np.min(importance_scores))
    
    # 模块分组（使用K-means聚类，基于FC矩阵的相似性）
    print("🔍 计算模块分组...")
    # 使用FC矩阵的相似性进行聚类
    similarity_matrix = np.corrcoef(fc_matrix)
    similarity_matrix = np.nan_to_num(similarity_matrix, nan=0)
    
    # K-means聚类，分为6个模块
    n_modules = 6
    kmeans = KMeans(n_clusters=n_modules, random_state=42, n_init=10)
    modules = kmeans.fit_predict(similarity_matrix)
    
    # 创建6列的.node文件
    node_data = np.column_stack([
        coords[:, 0],      # X坐标
        coords[:, 1],      # Y坐标  
        coords[:, 2],      # Z坐标
        node_sizes,        # 节点大小
        color_values,      # 颜色值（0-1）
        modules + 1        # 模块编号（1-6）
    ])
    
    # 保存.node文件（6列格式）
    np.savetxt('brainnet_nodes_100_6col.node', node_data, 
               fmt='%.3f\t%.3f\t%.3f\t%.3f\t%.6f\t%d', 
               delimiter='\t')
    print("✅ 已生成 brainnet_nodes_100_6col.node (100行, 6列)")
    
    # 创建.edge文件（纯数字方阵，Tab分隔）
    np.savetxt('brainnet_edges_100.edge', fc_matrix, fmt='%.6f', delimiter='\t')
    print("✅ 已生成 brainnet_edges_100.edge (100x100矩阵)")
    
    # 验证文件
    print(f"\n📊 验证文件:")
    print(f"Node文件行数: {len(node_data)}")
    print(f"Node文件列数: {node_data.shape[1]}")
    print(f"Edge文件形状: {fc_matrix.shape}")
    print(f"Edge矩阵非零元素: {np.count_nonzero(fc_matrix)}")
    print(f"Edge矩阵范围: [{np.min(fc_matrix):.6f}, {np.max(fc_matrix):.6f}]")
    print(f"模块分布: {np.bincount(modules + 1)}")
    print(f"颜色值范围: [{np.min(color_values):.6f}, {np.max(color_values):.6f}]")
    print(f"节点大小范围: [{np.min(node_sizes):.3f}, {np.max(node_sizes):.3f}]")
    
    return 'brainnet_nodes_100_6col.node', 'brainnet_edges_100.edge'

def main():
    """主函数"""
    print("🧠 从ABIDE数据提取真实FC矩阵并生成BrainNet Viewer文件")
    print("=" * 60)
    
    # 1. 提取真实FC矩阵
    fc_matrix = extract_real_fc_matrix()
    
    # 2. 加载重要性分数
    importance_scores = np.load('importance_scores/roi_importance.npy')
    print(f"重要性分数形状: {importance_scores.shape}")
    
    # 3. 创建BrainNet Viewer文件
    node_file, edge_file = create_brainnet_files(fc_matrix, importance_scores)
    
    print(f"\n🎉 完成！")
    print(f"Node文件: {node_file} (6列标准格式)")
    print(f"Edge文件: {edge_file}")
    print(f"现在可以在MATLAB/BrainNet Viewer中使用这些文件了！")
    
    # 显示文件格式说明
    print(f"\n📋 文件格式说明:")
    print(f"Node文件格式: x\ty\tz\tsize\tcolor\tmodule")
    print(f"  - x, y, z: MNI坐标 (mm)")
    print(f"  - size: 节点大小 (5-20)")
    print(f"  - color: 颜色值 (0-1, 基于重要性)")
    print(f"  - module: 模块编号 (1-6, 基于FC相似性聚类)")

if __name__ == "__main__":
    main() 