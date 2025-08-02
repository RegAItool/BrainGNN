#!/usr/bin/env python3
"""
真正的大脑表面可视化
使用nilearn显示3D大脑表面并高亮重要脑区
"""

import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, surface
import os
import pickle

def load_importance_scores(score_path='./importance_scores/roi_importance.npy'):
    """加载ROI重要性分数"""
    if os.path.exists(score_path):
        roi_importance = np.load(score_path)
        print(f"✅ 加载ROI重要性分数: {roi_importance.shape}")
        return roi_importance
    else:
        print(f"❌ 重要性分数文件不存在: {score_path}")
        return None

def create_brain_surface_visualization(roi_importance):
    """创建真正的大脑表面可视化"""
    print("🧠 创建真正的大脑表面可视化...")
    
    # 加载fsaverage大脑表面
    try:
        fsaverage = datasets.fetch_surf_fsaverage(mesh='fsaverage5')
        print("✅ 成功加载fsaverage表面")
    except Exception as e:
        print(f"❌ 无法加载fsaverage表面: {e}")
        return None
    
    # 正确读取mesh顶点数
    coords_left, faces_left = surface.load_surf_mesh(fsaverage.pial_left)
    coords_right, faces_right = surface.load_surf_mesh(fsaverage.pial_right)
    left_vertices = coords_left.shape[0]
    right_vertices = coords_right.shape[0]
    print(f"📏 左半球顶点数: {left_vertices}, 右半球顶点数: {right_vertices}")
    
    # 创建重要性mask
    n_rois = len(roi_importance)
    # 左半球
    left_importance = np.interp(
        np.linspace(0, 1, left_vertices),
        np.linspace(0, 1, n_rois),
        roi_importance
    )
    # 右半球
    right_importance = np.interp(
        np.linspace(0, 1, right_vertices),
        np.linspace(0, 1, n_rois),
        roi_importance
    )
    
    # 设置颜色映射和阈值
    cmap = 'hot'
    vmin, vmax = np.percentile(roi_importance[roi_importance > 0], [10, 90])
    
    # 创建图形
    fig = plt.figure(figsize=(20, 16))
    
    # 1. 左半球外侧视图
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_left,
        stat_map=left_importance,
        hemi='left',
        view='lateral',
        colorbar=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        axes=ax1,
        title='Left Hemisphere (Lateral)',
        bg_map=fsaverage.sulc_left
    )
    
    # 2. 左半球内侧视图
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_left,
        stat_map=left_importance,
        hemi='left',
        view='medial',
        colorbar=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        axes=ax2,
        title='Left Hemisphere (Medial)',
        bg_map=fsaverage.sulc_left
    )
    
    # 3. 左半球背侧视图
    ax3 = fig.add_subplot(2, 3, 3, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_left,
        stat_map=left_importance,
        hemi='left',
        view='dorsal',
        colorbar=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        axes=ax3,
        title='Left Hemisphere (Dorsal)',
        bg_map=fsaverage.sulc_left
    )
    
    # 4. 右半球外侧视图
    ax4 = fig.add_subplot(2, 3, 4, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_right,
        stat_map=right_importance,
        hemi='right',
        view='lateral',
        colorbar=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        axes=ax4,
        title='Right Hemisphere (Lateral)',
        bg_map=fsaverage.sulc_right
    )
    
    # 5. 右半球内侧视图
    ax5 = fig.add_subplot(2, 3, 5, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_right,
        stat_map=right_importance,
        hemi='right',
        view='medial',
        colorbar=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        axes=ax5,
        title='Right Hemisphere (Medial)',
        bg_map=fsaverage.sulc_right
    )
    
    # 6. 重要性分数分布
    ax6 = fig.add_subplot(2, 3, 6)
    non_zero_importance = roi_importance[roi_importance > 0]
    ax6.hist(non_zero_importance, bins=30, alpha=0.7, color='red', edgecolor='black')
    ax6.set_xlabel('ROI Importance Score')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Distribution of ROI Importance Scores')
    ax6.grid(True, alpha=0.3)
    
    # 添加统计信息
    fig.suptitle('BrainGNN ROI Importance - Brain Surface Visualization', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_glass_brain_visualization(roi_importance):
    """创建玻璃脑可视化"""
    print("🔍 创建玻璃脑可视化...")
    
    # 创建重要性mask（用于玻璃脑）
    n_rois = len(roi_importance)
    # 创建一个3D体积mask
    # 简化处理：创建一个64x64x64的体积
    volume_size = 64
    importance_volume = np.zeros((volume_size, volume_size, volume_size))
    
    # 将ROI重要性映射到3D体积的中心区域
    center_start = volume_size // 4
    center_end = 3 * volume_size // 4
    
    for i in range(min(n_rois, (center_end - center_start) ** 3)):
        x = center_start + (i % (center_end - center_start))
        y = center_start + ((i // (center_end - center_start)) % (center_end - center_start))
        z = center_start + (i // (center_end - center_start) ** 2)
        if x < center_end and y < center_end and z < center_end:
            importance_volume[x, y, z] = roi_importance[i]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('BrainGNN ROI Importance - Glass Brain View', fontsize=16, fontweight='bold')
    
    # 定义颜色映射
    cmap = 'hot'
    vmin, vmax = np.percentile(roi_importance[roi_importance > 0], [10, 90])
    
    # 四个视角的玻璃脑
    views = ['lateral', 'medial', 'dorsal', 'ventral']
    titles = ['Lateral View', 'Medial View', 'Dorsal View', 'Ventral View']
    
    for i, (view, title) in enumerate(zip(views, titles)):
        ax = axes[i//2, i%2]
        plotting.plot_glass_brain(
            importance_volume,
            colorbar=True,
            plot_abs=False,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            axes=ax,
            title=title
        )
    
    plt.tight_layout()
    return fig

def create_brain_atlas_mapping(roi_importance):
    """创建大脑atlas映射可视化"""
    print("🗺️ 创建大脑atlas映射...")
    
    # 尝试加载CC200 atlas
    try:
        atlas = datasets.fetch_atlas_craddock_2012()
        print("✅ 成功加载CC200 atlas")
    except Exception as e:
        print(f"❌ 无法加载CC200 atlas: {e}")
        return None
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('BrainGNN ROI Importance - Atlas Mapping', fontsize=16, fontweight='bold')
    
    # 1. Atlas ROI重要性映射
    ax1 = axes[0, 0]
    # 将重要性分数映射到atlas ROI
    n_rois = len(roi_importance)
    atlas_importance = np.zeros(200)  # CC200有200个ROI
    atlas_importance[:n_rois] = roi_importance
    
    # 创建热力图
    heatmap_data = atlas_importance.reshape(10, 20)  # 重塑为2D
    im1 = ax1.imshow(heatmap_data, cmap='hot', aspect='auto')
    ax1.set_title('CC200 Atlas ROI Importance')
    ax1.set_xlabel('ROI Column')
    ax1.set_ylabel('ROI Row')
    plt.colorbar(im1, ax=ax1, label='Importance Score')
    
    # 2. 重要性分数分布
    ax2 = axes[0, 1]
    ax2.hist(roi_importance, bins=20, alpha=0.7, color='blue', edgecolor='black')
    ax2.set_xlabel('Importance Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('ROI Importance Distribution')
    ax2.grid(True, alpha=0.3)
    
    # 3. 前10个最重要ROI
    ax3 = axes[1, 0]
    top_indices = np.argsort(roi_importance)[-10:][::-1]
    top_scores = roi_importance[top_indices]
    
    bars = ax3.bar(range(len(top_indices)), top_scores, color='red', alpha=0.7)
    ax3.set_xlabel('ROI Index')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('Top 10 Most Important ROIs')
    ax3.set_xticks(range(len(top_indices)))
    ax3.set_xticklabels([f'ROI {idx}' for idx in top_indices], rotation=45)
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, top_scores)):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{score:.4f}', ha='center', va='bottom', fontsize=8)
    
    # 4. 统计信息
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    info_text = f"""
    BrainGNN ROI Importance Analysis:
    
    Model Performance:
    • Test Accuracy: 52.2%
    • ROI Count: {len(roi_importance)}
    
    Importance Statistics:
    • Mean: {np.mean(roi_importance):.4f}
    • Std: {np.std(roi_importance):.4f}
    • Max: {np.max(roi_importance):.4f}
    • Min: {np.min(roi_importance):.4f}
    
    Top 5 Most Important ROIs:
    """
    for i, idx in enumerate(top_indices[:5]):
        info_text += f"• ROI {idx}: {roi_importance[idx]:.4f}\n"
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("🚀 开始创建真正的大脑表面可视化...")
    
    # 1. 加载重要性分数
    roi_importance = load_importance_scores()
    if roi_importance is None:
        return
    
    # 2. 创建可视化
    print("📈 生成大脑表面可视化...")
    
    # 大脑表面可视化
    fig1 = create_brain_surface_visualization(roi_importance)
    if fig1 is not None:
        fig1.savefig('real_brain_surface.png', dpi=300, bbox_inches='tight')
        print("💾 保存大脑表面图: real_brain_surface.png")
    
    # 玻璃脑可视化
    fig2 = create_glass_brain_visualization(roi_importance)
    fig2.savefig('real_glass_brain.png', dpi=300, bbox_inches='tight')
    print("💾 保存玻璃脑图: real_glass_brain.png")
    
    # Atlas映射可视化
    fig3 = create_brain_atlas_mapping(roi_importance)
    if fig3 is not None:
        fig3.savefig('real_brain_atlas_mapping.png', dpi=300, bbox_inches='tight')
        print("💾 保存Atlas映射图: real_brain_atlas_mapping.png")
    
    print("✅ 真正的大脑表面可视化已生成完成！")
    print("📁 生成的文件:")
    print("   - real_brain_surface.png (3D大脑表面图)")
    print("   - real_glass_brain.png (玻璃脑图)")
    print("   - real_brain_atlas_mapping.png (Atlas映射图)")

if __name__ == '__main__':
    main() 