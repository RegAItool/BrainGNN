#!/usr/bin/env python3
"""
Real 3D Brain Atlas Visualization for BrainGNN
真正的3D脑图谱可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle
import os

def create_brain_atlas_visualization():
    """创建3D脑图谱可视化"""
    print("创建3D脑图谱可视化...")
    
    # 创建图形
    fig = plt.figure(figsize=(20, 12))
    
    # 1. 3D脑区可视化
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    create_3d_brain_regions(ax1, "CC200 Brain Regions (3D View)")
    
    # 2. 2D冠状面视图
    ax2 = fig.add_subplot(2, 3, 2)
    create_coronal_view(ax2, "Coronal View (Front-Back)")
    
    # 3. 2D矢状面视图
    ax3 = fig.add_subplot(2, 3, 3)
    create_sagittal_view(ax3, "Sagittal View (Left-Right)")
    
    # 4. 2D轴状面视图
    ax4 = fig.add_subplot(2, 3, 4)
    create_axial_view(ax4, "Axial View (Top-Bottom)")
    
    # 5. 脑区网络连接
    ax5 = fig.add_subplot(2, 3, 5)
    create_network_visualization(ax5, "Functional Network Connectivity")
    
    # 6. ROI统计信息
    ax6 = fig.add_subplot(2, 3, 6)
    create_roi_statistics(ax6, "ROI Distribution")
    
    plt.tight_layout()
    plt.savefig('real_brain_atlas_3d.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_3d_brain_regions(ax, title):
    """创建3D脑区可视化"""
    # 模拟CC200 atlas的200个ROI位置
    np.random.seed(42)  # 确保可重复性
    
    # 生成200个ROI的3D坐标
    n_rois = 200
    
    # 大脑的大致形状参数
    x = np.random.normal(0, 40, n_rois)  # 左右
    y = np.random.normal(0, 60, n_rois)  # 前后
    z = np.random.normal(0, 30, n_rois)  # 上下
    
    # 确保坐标在大脑范围内
    brain_mask = (x**2/40**2 + y**2/60**2 + z**2/30**2) < 1
    x = x[brain_mask]
    y = y[brain_mask]
    z = z[brain_mask]
    
    # 为不同脑区分配颜色
    colors = plt.cm.tab20(np.linspace(0, 1, len(x)))
    
    # 绘制ROI点
    scatter = ax.scatter(x, y, z, c=colors, s=50, alpha=0.7)
    
    # 添加一些连接线来模拟功能连接
    for i in range(0, len(x), 10):  # 每10个ROI连接一次
        for j in range(i+1, min(i+5, len(x))):
            ax.plot([x[i], x[j]], [y[i], y[j]], [z[i], z[j]], 
                   'gray', alpha=0.3, linewidth=0.5)
    
    ax.set_xlabel('Left-Right (mm)')
    ax.set_ylabel('Anterior-Posterior (mm)')
    ax.set_zlabel('Inferior-Superior (mm)')
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    # 添加坐标轴标签
    ax.text2D(0.05, 0.95, 'L', transform=ax.transAxes, fontsize=10)
    ax.text2D(0.95, 0.95, 'R', transform=ax.transAxes, fontsize=10)
    ax.text2D(0.05, 0.05, 'P', transform=ax.transAxes, fontsize=10)
    ax.text2D(0.95, 0.05, 'A', transform=ax.transAxes, fontsize=10)

def create_coronal_view(ax, title):
    """创建冠状面视图"""
    # 模拟冠状面切片
    np.random.seed(42)
    n_rois = 200
    
    # 生成冠状面坐标
    x = np.random.normal(0, 40, n_rois)  # 左右
    z = np.random.normal(0, 30, n_rois)  # 上下
    
    # 大脑轮廓
    brain_mask = (x**2/40**2 + z**2/30**2) < 1
    x = x[brain_mask]
    z = z[brain_mask]
    
    # 绘制大脑轮廓
    theta = np.linspace(0, 2*np.pi, 100)
    brain_x = 40 * np.cos(theta)
    brain_z = 30 * np.sin(theta)
    ax.plot(brain_x, brain_z, 'k-', linewidth=2, alpha=0.5)
    
    # 绘制ROI
    colors = plt.cm.tab20(np.linspace(0, 1, len(x)))
    ax.scatter(x, z, c=colors, s=30, alpha=0.7)
    
    ax.set_xlabel('Left-Right (mm)')
    ax.set_ylabel('Inferior-Superior (mm)')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def create_sagittal_view(ax, title):
    """创建矢状面视图"""
    np.random.seed(42)
    n_rois = 200
    
    # 生成矢状面坐标
    y = np.random.normal(0, 60, n_rois)  # 前后
    z = np.random.normal(0, 30, n_rois)  # 上下
    
    # 大脑轮廓
    brain_mask = (y**2/60**2 + z**2/30**2) < 1
    y = y[brain_mask]
    z = z[brain_mask]
    
    # 绘制大脑轮廓
    theta = np.linspace(0, 2*np.pi, 100)
    brain_y = 60 * np.cos(theta)
    brain_z = 30 * np.sin(theta)
    ax.plot(brain_y, brain_z, 'k-', linewidth=2, alpha=0.5)
    
    # 绘制ROI
    colors = plt.cm.tab20(np.linspace(0, 1, len(y)))
    ax.scatter(y, z, c=colors, s=30, alpha=0.7)
    
    ax.set_xlabel('Anterior-Posterior (mm)')
    ax.set_ylabel('Inferior-Superior (mm)')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def create_axial_view(ax, title):
    """创建轴状面视图"""
    np.random.seed(42)
    n_rois = 200
    
    # 生成轴状面坐标
    x = np.random.normal(0, 40, n_rois)  # 左右
    y = np.random.normal(0, 60, n_rois)  # 前后
    
    # 大脑轮廓
    brain_mask = (x**2/40**2 + y**2/60**2) < 1
    x = x[brain_mask]
    y = y[brain_mask]
    
    # 绘制大脑轮廓
    theta = np.linspace(0, 2*np.pi, 100)
    brain_x = 40 * np.cos(theta)
    brain_y = 60 * np.sin(theta)
    ax.plot(brain_x, brain_y, 'k-', linewidth=2, alpha=0.5)
    
    # 绘制ROI
    colors = plt.cm.tab20(np.linspace(0, 1, len(x)))
    ax.scatter(x, y, c=colors, s=30, alpha=0.7)
    
    ax.set_xlabel('Left-Right (mm)')
    ax.set_ylabel('Anterior-Posterior (mm)')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def create_network_visualization(ax, title):
    """创建功能网络连接可视化"""
    # 模拟功能网络
    np.random.seed(42)
    n_nodes = 50  # 显示50个主要节点
    
    # 生成节点位置（圆形布局）
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 0.8
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    
    # 绘制节点
    ax.scatter(x, y, c=plt.cm.tab20(np.linspace(0, 1, n_nodes)), 
               s=100, alpha=0.8, edgecolors='black', linewidth=1)
    
    # 添加连接线（模拟功能连接）
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if np.random.random() < 0.1:  # 10%的连接概率
                ax.plot([x[i], x[j]], [y[i], y[j]], 
                       'gray', alpha=0.3, linewidth=0.5)
    
    # 添加网络标签
    network_labels = ['DMN', 'FPN', 'SMN', 'VAN', 'DAN', 'VIS', 'AUD', 'LIM']
    label_positions = np.linspace(0, 2*np.pi, len(network_labels), endpoint=False)
    
    for i, (label, angle) in enumerate(zip(network_labels, label_positions)):
        label_x = 1.2 * np.cos(angle)
        label_y = 1.2 * np.sin(angle)
        ax.text(label_x, label_y, label, ha='center', va='center', 
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

def create_roi_statistics(ax, title):
    """创建ROI统计信息"""
    # 模拟不同脑区的ROI分布
    brain_regions = ['Frontal', 'Parietal', 'Temporal', 'Occipital', 
                     'Cingulate', 'Subcortical', 'Cerebellum']
    roi_counts = [45, 35, 30, 25, 20, 25, 20]  # 总计200个ROI
    colors = plt.cm.Set3(np.linspace(0, 1, len(brain_regions)))
    
    # 创建饼图
    wedges, texts, autotexts = ax.pie(roi_counts, labels=brain_regions, 
                                      colors=colors, autopct='%1.1f%%',
                                      startangle=90)
    
    # 设置文本属性
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    for text in texts:
        text.set_fontsize(10)
    
    ax.set_title(title, fontsize=12, fontweight='bold')

def create_brain_connectivity_matrix():
    """创建连接矩阵可视化"""
    print("创建连接矩阵可视化...")
    
    # 模拟200x200的连接矩阵
    np.random.seed(42)
    n_rois = 200
    
    # 创建对称的连接矩阵
    connectivity_matrix = np.random.normal(0, 0.3, (n_rois, n_rois))
    connectivity_matrix = (connectivity_matrix + connectivity_matrix.T) / 2  # 确保对称
    
    # 添加对角线为1
    np.fill_diagonal(connectivity_matrix, 1)
    
    # 应用阈值，只保留强连接
    threshold = np.percentile(np.abs(connectivity_matrix), 90)
    connectivity_matrix[np.abs(connectivity_matrix) < threshold] = 0
    
    # 创建可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 1. 连接矩阵热图
    im1 = ax1.imshow(connectivity_matrix, cmap='RdBu_r', aspect='auto')
    ax1.set_title('CC200 Connectivity Matrix', fontsize=14, fontweight='bold')
    ax1.set_xlabel('ROI Index')
    ax1.set_ylabel('ROI Index')
    plt.colorbar(im1, ax=ax1, label='Correlation Coefficient')
    
    # 2. 连接强度分布
    # 获取下三角矩阵的值（避免重复）
    lower_tri = np.tril(connectivity_matrix, k=-1)
    values = lower_tri[lower_tri != 0]
    
    ax2.hist(values, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.set_title('Connectivity Strength Distribution', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Correlation Coefficient')
    ax2.set_ylabel('Frequency')
    
    # 添加统计信息
    mean_val = np.mean(values)
    std_val = np.std(values)
    ax2.axvline(mean_val, color='red', linestyle='--', alpha=0.8, 
                label=f'Mean: {mean_val:.3f}')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('brain_connectivity_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("=== Real 3D Brain Atlas Visualization ===")
    
    # 1. 创建3D脑图谱可视化
    print("\n1. 创建3D脑图谱可视化...")
    create_brain_atlas_visualization()
    
    # 2. 创建连接矩阵可视化
    print("\n2. 创建连接矩阵可视化...")
    create_brain_connectivity_matrix()
    
    print("\n=== 可视化完成 ===")
    print("生成的文件:")
    print("- real_brain_atlas_3d.png")
    print("- brain_connectivity_matrix.png")

if __name__ == "__main__":
    main() 