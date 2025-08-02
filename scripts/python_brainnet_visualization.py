#!/usr/bin/env python3
"""
Python版本的BrainNet Viewer可视化
直接生成专业的大脑网络可视化，无需MATLAB
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
import json
import os

def create_brain_outline(ax, scale=1.0):
    """创建大脑轮廓"""
    # 大脑轮廓参数
    brain_width = 15 * scale
    brain_height = 20 * scale
    brain_depth = 12 * scale
    
    # 创建大脑形状
    x = np.linspace(-brain_width/2, brain_width/2, 100)
    y = np.linspace(-brain_height/2, brain_height/2, 100)
    X, Y = np.meshgrid(x, y)
    
    # 大脑轮廓函数
    Z = brain_depth/2 * np.sqrt(1 - (X/(brain_width/2))**2 - (Y/(brain_height/2))**2)
    Z = np.where(Z < 0, 0, Z)
    
    # 绘制大脑轮廓
    ax.plot_surface(X, Y, Z, alpha=0.1, color='lightgray', linewidth=0)
    ax.plot_surface(X, Y, -Z, alpha=0.1, color='lightgray', linewidth=0)
    
    return X, Y, Z

def create_brain_network_visualization():
    """创建大脑网络可视化"""
    print("🧠 创建Python版本的BrainNet Viewer可视化...")
    
    # 加载数据
    try:
        nodes = np.loadtxt('bridge_nodes.node')
        edges = np.loadtxt('bridge_edges.edge')
        
        with open('brainnet_data_info.json', 'r') as f:
            data_info = json.load(f)
            
        print(f"✅ 加载数据成功: {nodes.shape[0]} 个节点, {edges.shape[0]} 条边")
        
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return
    
    # 创建图形
    fig = plt.figure(figsize=(20, 15))
    
    # 1. 3D大脑网络可视化
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    ax1.set_title('BrainGNN ROI Network - 3D View', fontsize=14, fontweight='bold')
    
    # 创建大脑轮廓
    create_brain_outline(ax1, scale=1.2)
    
    # 绘制节点
    scatter = ax1.scatter(nodes[:, 0], nodes[:, 1], nodes[:, 2], 
                          c=nodes[:, 4], s=nodes[:, 3]*50, 
                          cmap='hot', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    # 绘制边
    for edge in edges:
        if edge[2] > 0.1:  # 只显示强连接
            start_node = nodes[int(edge[0])]
            end_node = nodes[int(edge[1])]
            ax1.plot([start_node[0], end_node[0]], 
                    [start_node[1], end_node[1]], 
                    [start_node[2], end_node[2]], 
                    color='blue', alpha=edge[2], linewidth=edge[2]*3)
    
    ax1.set_xlabel('X (mm)')
    ax1.set_ylabel('Y (mm)')
    ax1.set_zlabel('Z (mm)')
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax1, shrink=0.8)
    cbar.set_label('ROI Importance', fontsize=12)
    
    # 2. 2D投影可视化
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_title('BrainGNN ROI Network - 2D Projection', fontsize=14, fontweight='bold')
    
    # 绘制大脑轮廓
    brain_circle = patches.Circle((0, 0), 10, fill=False, color='gray', linewidth=2)
    ax2.add_patch(brain_circle)
    
    # 绘制节点
    scatter2 = ax2.scatter(nodes[:, 0], nodes[:, 1], 
                           c=nodes[:, 4], s=nodes[:, 3]*30, 
                           cmap='hot', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    # 绘制边
    for edge in edges:
        if edge[2] > 0.1:
            start_node = nodes[int(edge[0])]
            end_node = nodes[int(edge[1])]
            ax2.plot([start_node[0], end_node[0]], 
                    [start_node[1], end_node[1]], 
                    color='blue', alpha=edge[2], linewidth=edge[2]*2)
    
    ax2.set_xlabel('X (mm)')
    ax2.set_ylabel('Y (mm)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # 3. ROI重要性热图
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_title('ROI Importance Heatmap', fontsize=14, fontweight='bold')
    
    # 创建重要性矩阵
    importance_matrix = nodes[:, 4].reshape(-1, 1)
    sns.heatmap(importance_matrix, cmap='hot', cbar=True, 
                xticklabels=False, yticklabels=False, ax=ax3)
    ax3.set_ylabel('ROI Index')
    ax3.set_xlabel('Importance Score')
    
    # 4. 重要性分布直方图
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.set_title('ROI Importance Distribution', fontsize=14, fontweight='bold')
    
    ax4.hist(nodes[:, 4], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
    ax4.axvline(np.mean(nodes[:, 4]), color='red', linestyle='--', 
                label=f'Mean: {np.mean(nodes[:, 4]):.3f}')
    ax4.axvline(np.max(nodes[:, 4]), color='orange', linestyle='--', 
                label=f'Max: {np.max(nodes[:, 4]):.3f}')
    ax4.set_xlabel('Importance Score')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. 连接强度分布
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.set_title('Connection Strength Distribution', fontsize=14, fontweight='bold')
    
    connection_strengths = edges[:, 2]
    ax5.hist(connection_strengths, bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
    ax5.axvline(np.mean(connection_strengths), color='red', linestyle='--', 
                label=f'Mean: {np.mean(connection_strengths):.3f}')
    ax5.set_xlabel('Connection Strength')
    ax5.set_ylabel('Frequency')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. 网络统计信息
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.set_title('Network Statistics', fontsize=14, fontweight='bold')
    ax6.axis('off')
    
    # 计算网络统计
    total_nodes = len(nodes)
    total_edges = len(edges)
    avg_importance = np.mean(nodes[:, 4])
    max_importance = np.max(nodes[:, 4])
    avg_connection = np.mean(edges[:, 2])
    max_connection = np.max(edges[:, 2])
    
    stats_text = f"""
    Network Statistics:
    
    Nodes: {total_nodes}
    Edges: {total_edges}
    
    ROI Importance:
    • Average: {avg_importance:.3f}
    • Maximum: {max_importance:.3f}
    
    Connection Strength:
    • Average: {avg_connection:.3f}
    • Maximum: {max_connection:.3f}
    
    Top 5 Important ROIs:
    """
    
    # 添加前5个重要ROI
    top_indices = np.argsort(nodes[:, 4])[-5:][::-1]
    for i, idx in enumerate(top_indices):
        stats_text += f"• ROI {idx}: {nodes[idx, 4]:.3f}\n"
    
    ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes, 
             fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图像
    output_file = 'python_brainnet_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ 可视化已保存: {output_file}")
    
    # 显示图像
    plt.show()
    
    return fig

def create_advanced_brain_visualization():
    """创建高级大脑可视化"""
    print("🎨 创建高级大脑可视化...")
    
    # 加载数据
    try:
        nodes = np.loadtxt('bridge_nodes.node')
        edges = np.loadtxt('bridge_edges.edge')
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Advanced BrainGNN Network Analysis', fontsize=16, fontweight='bold')
    
    # 1. 大脑网络图
    ax1 = axes[0, 0]
    ax1.set_title('Brain Network Graph', fontsize=12, fontweight='bold')
    
    # 创建网络图
    pos = nodes[:, :2]  # 使用前两个坐标作为位置
    
    # 绘制边
    for edge in edges:
        if edge[2] > 0.05:  # 过滤弱连接
            start_pos = pos[int(edge[0])]
            end_pos = pos[int(edge[1])]
            ax1.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 
                    color='blue', alpha=edge[2], linewidth=edge[2]*5)
    
    # 绘制节点
    scatter = ax1.scatter(pos[:, 0], pos[:, 1], 
                          c=nodes[:, 4], s=nodes[:, 3]*20, 
                          cmap='hot', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    ax1.set_xlabel('X (mm)')
    ax1.set_ylabel('Y (mm)')
    ax1.grid(True, alpha=0.3)
    
    # 2. 重要性排序
    ax2 = axes[0, 1]
    ax2.set_title('ROI Importance Ranking', fontsize=12, fontweight='bold')
    
    importance_scores = nodes[:, 4]
    sorted_indices = np.argsort(importance_scores)[::-1]
    sorted_scores = importance_scores[sorted_indices]
    
    bars = ax2.bar(range(len(sorted_scores)), sorted_scores, 
                   color=plt.cm.hot(sorted_scores/max(sorted_scores)))
    ax2.set_xlabel('ROI Rank')
    ax2.set_ylabel('Importance Score')
    ax2.set_xticks(range(0, len(sorted_scores), 10))
    ax2.grid(True, alpha=0.3)
    
    # 3. 连接强度矩阵
    ax3 = axes[1, 0]
    ax3.set_title('Connection Strength Matrix', fontsize=12, fontweight='bold')
    
    # 创建连接矩阵
    n_nodes = len(nodes)
    connection_matrix = np.zeros((n_nodes, n_nodes))
    
    for edge in edges:
        i, j, weight = int(edge[0]), int(edge[1]), edge[2]
        connection_matrix[i, j] = weight
        connection_matrix[j, i] = weight  # 对称矩阵
    
    im = ax3.imshow(connection_matrix, cmap='Blues', aspect='auto')
    plt.colorbar(im, ax=ax3)
    ax3.set_xlabel('ROI Index')
    ax3.set_ylabel('ROI Index')
    
    # 4. 3D散点图
    ax4 = axes[1, 1]
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    ax4.set_title('3D ROI Distribution', fontsize=12, fontweight='bold')
    
    scatter3d = ax4.scatter(nodes[:, 0], nodes[:, 1], nodes[:, 2], 
                            c=nodes[:, 4], s=nodes[:, 3]*30, 
                            cmap='hot', alpha=0.8)
    
    ax4.set_xlabel('X (mm)')
    ax4.set_ylabel('Y (mm)')
    ax4.set_zlabel('Z (mm)')
    
    plt.tight_layout()
    
    # 保存图像
    output_file = 'advanced_brain_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ 高级可视化已保存: {output_file}")
    
    plt.show()
    
    return fig

def main():
    """主函数"""
    print("🚀 Python BrainNet Viewer 可视化开始...")
    print("=" * 50)
    
    # 检查文件是否存在
    required_files = ['bridge_nodes.node', 'bridge_edges.edge', 'brainnet_data_info.json']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 文件不存在: {file}")
            print("请先运行 brainnet_visualization.py 生成数据文件")
            return
    
    print("✅ 所有必需文件都存在")
    
    # 创建基础可视化
    print("\n📊 创建基础大脑网络可视化...")
    fig1 = create_brain_network_visualization()
    
    # 创建高级可视化
    print("\n🎨 创建高级大脑可视化...")
    fig2 = create_advanced_brain_visualization()
    
    print("\n🎉 Python BrainNet Viewer 可视化完成！")
    print("📁 生成的文件:")
    print("   - python_brainnet_visualization.png (基础可视化)")
    print("   - advanced_brain_visualization.png (高级可视化)")
    
    print("\n🎯 特点:")
    print("   ✅ 无需MATLAB")
    print("   ✅ 专业的大脑网络可视化")
    print("   ✅ 多种分析视角")
    print("   ✅ 高质量输出")
    print("   ✅ 适合论文和报告")

if __name__ == "__main__":
    main() 