#!/usr/bin/env python3
"""
创建Top-30重要节点的BrainNet Viewer文件
基于节点重要性（第4列）选择最重要的30个节点
"""

import numpy as np

def create_top30_brainnet():
    """创建Top-30节点的BrainNet Viewer文件"""
    
    # 加载原始文件
    print("加载原始文件...")
    node = np.loadtxt('brainnet_nodes_100_6col.node')
    edge = np.loadtxt('brainnet_edges_100.edge')
    
    print(f"原始文件形状: Node {node.shape}, Edge {edge.shape}")
    
    # 根据节点重要性（第4列）排序，选择Top-30
    importance_scores = node[:, 3]  # 第4列是节点大小/重要性
    sorted_indices = np.argsort(importance_scores)[::-1]  # 降序排列
    top30_indices = sorted_indices[:30]
    
    print(f"Top-30节点的重要性分数范围: {importance_scores[top30_indices].min():.3f} 到 {importance_scores[top30_indices].max():.3f}")
    
    # 提取Top-30节点和对应的边
    top30_node = node[top30_indices, :]
    top30_edge = edge[np.ix_(top30_indices, top30_indices)]
    
    print(f"Top-30文件形状: Node {top30_node.shape}, Edge {top30_edge.shape}")
    
    # 保存文件
    print("保存Top-30文件...")
    np.savetxt('top30.node', top30_node, fmt='%.6f', delimiter='\t')
    np.savetxt('top30.edge', top30_edge, fmt='%.6f', delimiter='\t')
    
    # 显示Top-10最重要节点的信息
    print("\nTop-10最重要节点信息:")
    print("排名\t重要性\t模块\t坐标(x,y,z)")
    for i in range(min(10, len(top30_indices))):
        idx = top30_indices[i]
        importance = node[idx, 3]
        module = int(node[idx, 5])
        coords = node[idx, :3]
        print(f"{i+1}\t{importance:.3f}\t{module}\t({coords[0]:.1f}, {coords[1]:.1f}, {coords[2]:.1f})")
    
    # 统计边信息
    edge_strength = top30_edge[top30_edge > 0]
    print(f"\n边连接统计:")
    print(f"总边数: {top30_edge.size}")
    print(f"非零边数: {len(edge_strength)}")
    print(f"边强度范围: {edge_strength.min():.6f} 到 {edge_strength.max():.6f}")
    
    print("\n✅ Top-30文件创建完成!")
    print("文件: top30.node, top30.edge")
    print("可在BrainNet Viewer中使用这些文件进行可视化")

if __name__ == "__main__":
    create_top30_brainnet() 