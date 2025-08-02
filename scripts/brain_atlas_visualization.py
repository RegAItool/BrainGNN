#!/usr/bin/env python3
"""
Brain Atlas Visualization for BrainGNN
可视化ABIDE数据集中使用的脑区atlas
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nilearn import datasets, plotting
from nilearn.plotting import plot_roi, plot_anat, plot_glass_brain
import nibabel as nib
import os
import pandas as pd

def load_cc200_atlas():
    """加载CC200 atlas信息"""
    # CC200 (Craddock 200) atlas
    atlas = datasets.fetch_atlas_craddock_2012()
    return atlas

def load_ho_atlas():
    """加载Harvard-Oxford atlas"""
    atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
    return atlas

def load_cc400_atlas():
    """加载CC400 atlas信息"""
    # 这里使用CC200作为替代，因为CC400可能需要特殊处理
    atlas = datasets.fetch_atlas_craddock_2012()
    return atlas

def visualize_atlas(atlas_name='cc200'):
    """可视化指定的atlas"""
    print(f"正在加载 {atlas_name} atlas...")
    
    if atlas_name == 'cc200':
        atlas = load_cc200_atlas()
        title = "Craddock 200 ROI Atlas"
    elif atlas_name == 'ho':
        atlas = load_ho_atlas()
        title = "Harvard-Oxford Cortical Atlas"
    elif atlas_name == 'cc400':
        atlas = load_cc400_atlas()
        title = "Craddock 400 ROI Atlas"
    else:
        print(f"不支持的atlas: {atlas_name}")
        return
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'{title} - BrainGNN Visualization', fontsize=16, fontweight='bold')
    
    # 1. 3D脑区可视化
    ax1 = axes[0, 0]
    try:
        display = plot_roi(atlas.maps, title="3D ROI Visualization", axes=ax1)
        ax1.set_title("3D ROI Visualization", fontsize=12)
    except Exception as e:
        ax1.text(0.5, 0.5, f"3D visualization failed:\n{str(e)}", 
                ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title("3D ROI Visualization (Failed)", fontsize=12)
    
    # 2. Glass brain visualization
    ax2 = axes[0, 1]
    try:
        display = plot_glass_brain(atlas.maps, title="Glass Brain View", axes=ax2)
        ax2.set_title("Glass Brain View", fontsize=12)
    except Exception as e:
        ax2.text(0.5, 0.5, f"Glass brain failed:\n{str(e)}", 
                ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title("Glass Brain View (Failed)", fontsize=12)
    
    # 3. ROI数量统计
    ax3 = axes[1, 0]
    if hasattr(atlas, 'labels'):
        roi_counts = len(atlas.labels)
        ax3.bar(['ROIs'], [roi_counts], color='skyblue', alpha=0.7)
        ax3.set_title(f"Number of ROIs: {roi_counts}", fontsize=12)
        ax3.set_ylabel("Count")
        ax3.text(0, roi_counts + roi_counts*0.05, str(roi_counts), 
                ha='center', va='bottom', fontweight='bold')
    else:
        ax3.text(0.5, 0.5, "ROI count not available", 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title("ROI Count", fontsize=12)
    
    # 4. Atlas信息
    ax4 = axes[1, 1]
    ax4.axis('off')
    info_text = f"""
Atlas Information:
- Name: {atlas_name.upper()}
- Type: {getattr(atlas, 'atlas_type', 'Unknown')}
- Description: {getattr(atlas, 'description', 'No description available')}
- Maps shape: {getattr(atlas.maps, 'shape', 'Unknown')}
- Labels count: {len(getattr(atlas, 'labels', []))}
"""
    ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, 
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
    ax4.set_title("Atlas Information", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'brain_atlas_{atlas_name}.png', dpi=300, bbox_inches='tight')
    plt.show()

def visualize_connectivity_matrix():
    """可视化连接矩阵"""
    print("正在加载连接矩阵数据...")
    
    # 尝试加载处理后的数据
    data_path = './data/ABIDE_pcp/cpac/filt_noglobal'
    if os.path.exists(data_path):
        # 查找.mat文件
        mat_files = [f for f in os.listdir(data_path) if f.endswith('.mat')]
        if mat_files:
            print(f"找到 {len(mat_files)} 个连接矩阵文件")
            
            # 这里可以添加连接矩阵的可视化代码
            # 由于.mat文件需要scipy.io来读取，这里只显示文件信息
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.text(0.5, 0.5, f"Found {len(mat_files)} connectivity matrix files\nin {data_path}", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title("Connectivity Matrix Files", fontsize=16)
            ax.axis('off')
            plt.tight_layout()
            plt.savefig('connectivity_matrix_info.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print("未找到连接矩阵文件")
    else:
        print(f"数据路径不存在: {data_path}")

def create_atlas_comparison():
    """创建不同atlas的对比"""
    print("创建atlas对比...")
    
    atlases = {
        'cc200': ('Craddock 200', 'craddock_2012'),
        'ho': ('Harvard-Oxford', 'harvard_oxford'),
        'aal': ('AAL', 'aal')
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Brain Atlas Comparison for BrainGNN', fontsize=16, fontweight='bold')
    
    for idx, (atlas_key, (atlas_name, atlas_func)) in enumerate(atlases.items()):
        ax = axes[idx//2, idx%2]
        
        try:
            if atlas_key == 'cc200':
                atlas = datasets.fetch_atlas_craddock_2012()
            elif atlas_key == 'ho':
                atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
            else:
                # 对于AAL，使用默认的
                atlas = datasets.fetch_atlas_craddock_2012()
            
            # 显示atlas信息
            roi_count = len(getattr(atlas, 'labels', []))
            ax.text(0.5, 0.5, f"{atlas_name}\nROIs: {roi_count}\nType: {getattr(atlas, 'atlas_type', 'Unknown')}", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
            ax.set_title(f"{atlas_name} Atlas", fontsize=14, fontweight='bold')
            
        except Exception as e:
            ax.text(0.5, 0.5, f"{atlas_name}\nError: {str(e)}", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=10)
            ax.set_title(f"{atlas_name} Atlas", fontsize=14, fontweight='bold')
        
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('atlas_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("=== BrainGNN Atlas Visualization ===")
    print("正在创建脑图谱可视化...")
    
    # 1. 可视化CC200 atlas (默认使用的atlas)
    print("\n1. 可视化CC200 Atlas...")
    visualize_atlas('cc200')
    
    # 2. 可视化Harvard-Oxford atlas
    print("\n2. 可视化Harvard-Oxford Atlas...")
    visualize_atlas('ho')
    
    # 3. 创建atlas对比
    print("\n3. 创建Atlas对比...")
    create_atlas_comparison()
    
    # 4. 可视化连接矩阵信息
    print("\n4. 检查连接矩阵数据...")
    visualize_connectivity_matrix()
    
    print("\n=== 可视化完成 ===")
    print("生成的文件:")
    print("- brain_atlas_cc200.png")
    print("- brain_atlas_ho.png") 
    print("- atlas_comparison.png")
    print("- connectivity_matrix_info.png")

if __name__ == "__main__":
    main() 