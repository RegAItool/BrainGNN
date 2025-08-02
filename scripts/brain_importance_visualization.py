#!/usr/bin/env python3
"""
论文风格的脑区重要性可视化
使用BrainGNN导出的ROI重要性分数生成大脑表面高亮图
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nilearn import datasets, plotting, surface
import nibabel as nib
import os
import pickle
import argparse

def load_importance_scores(score_path='./importance_scores/roi_importance.npy'):
    """加载ROI重要性分数"""
    if os.path.exists(score_path):
        roi_importance = np.load(score_path)
        print(f"✅ 加载ROI重要性分数: {roi_importance.shape}")
        return roi_importance
    else:
        print(f"❌ 重要性分数文件不存在: {score_path}")
        return None

def load_stats(stats_path='./importance_scores/stats.pkl'):
    """加载统计信息"""
    if os.path.exists(stats_path):
        with open(stats_path, 'rb') as f:
            stats = pickle.load(f)
        print(f"📊 模型性能: 准确率 {stats['accuracy']:.3f}")
        return stats
    return None

def create_roi_mask(roi_importance, atlas_name='cc200'):
    """将ROI重要性分数转换为大脑表面mask"""
    print("🔄 创建ROI重要性mask...")
    
    # 加载fsaverage大脑表面
    try:
        fsaverage = datasets.fetch_surf_fsaverage(mesh='fsaverage5')
        print("✅ 成功加载fsaverage表面")
    except Exception as e:
        print(f"❌ 无法加载fsaverage表面: {e}")
        return None, None
    
    # 正确读取mesh顶点数
    coords_left, faces_left = surface.load_surf_mesh(fsaverage.pial_left)
    left_vertices = coords_left.shape[0]
    print(f"📏 左半球顶点数: {left_vertices}")
    
    # 创建重要性mask (插值到mesh顶点)
    n_rois = len(roi_importance)
    importance_mask = np.interp(
        np.linspace(0, 1, left_vertices),
        np.linspace(0, 1, n_rois),
        roi_importance
    )
    
    return importance_mask, fsaverage

def create_paper_style_visualization(importance_mask, fsaverage, stats=None):
    """创建论文风格的大脑可视化"""
    print("🎨 创建论文风格的大脑可视化...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形
    fig = plt.figure(figsize=(20, 12))
    
    # 定义颜色映射
    cmap = 'hot'  # 论文常用热力图
    vmin, vmax = np.percentile(importance_mask[importance_mask > 0], [10, 90])
    
    # 1. 左半球外侧视图
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    plotting.plot_surf_stat_map(
        fsaverage.infl_left,
        stat_map=importance_mask,
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
        stat_map=importance_mask,
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
        stat_map=importance_mask,
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
        stat_map=importance_mask,
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
        stat_map=importance_mask,
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
    
    # 6. 重要性分数分布直方图
    ax6 = fig.add_subplot(2, 3, 6)
    non_zero_mask = importance_mask[importance_mask > 0]
    ax6.hist(non_zero_mask, bins=30, alpha=0.7, color='red', edgecolor='black')
    ax6.set_xlabel('ROI Importance Score')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Distribution of ROI Importance Scores')
    ax6.grid(True, alpha=0.3)
    
    # 添加统计信息
    if stats:
        fig.suptitle(
            f'BrainGNN ROI Importance Visualization\n'
            f'ABIDE Dataset | Test Accuracy: {stats["accuracy"]}:.3f | '
            f'Correct Predictions: {stats["n_correct"]}/{stats["n_samples"]}',
            fontsize=16, fontweight='bold'
        )
    else:
        fig.suptitle('BrainGNN ROI Importance Visualization', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_glass_brain_visualization(roi_importance, fsaverage):
    """创建玻璃脑可视化"""
    print("🔍 创建玻璃脑可视化...")
    import nibabel as nib
    from nilearn import image
    
    # 创建一个3D体积（64x64x64）
    volume_size = 64
    importance_volume = np.zeros((volume_size, volume_size, volume_size))
    n_rois = len(roi_importance)
    center_start = volume_size // 4
    center_end = 3 * volume_size // 4
    # 将ROI重要性分数填入中心区域
    for i in range(min(n_rois, (center_end - center_start) ** 3)):
        x = center_start + (i % (center_end - center_start))
        y = center_start + ((i // (center_end - center_start)) % (center_end - center_start))
        z = center_start + (i // (center_end - center_start) ** 2)
        if x < center_end and y < center_end and z < center_end:
            importance_volume[x, y, z] = roi_importance[i]
    # 创建Nifti1Image
    affine = np.eye(4)
    importance_img = nib.Nifti1Image(importance_volume, affine)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('BrainGNN ROI Importance - Glass Brain View', fontsize=16, fontweight='bold')
    cmap = 'hot'
    non_zero = roi_importance[roi_importance > 0]
    vmin, vmax = np.percentile(non_zero, [10, 90])
    views = ['lateral', 'medial', 'dorsal', 'ventral']
    titles = ['Lateral View', 'Medial View', 'Dorsal View', 'Ventral View']
    for i, (view, title) in enumerate(zip(views, titles)):
        ax = axes[i//2, i%2]
        plotting.plot_glass_brain(
            importance_img,
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

def create_importance_summary(roi_importance, stats=None):
    """创建重要性分数总结图"""
    print("📊 创建重要性分数总结...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 前20个最重要ROI的条形图
    top_indices = np.argsort(roi_importance)[-20:][::-1]
    top_scores = roi_importance[top_indices]
    
    ax1 = axes[0, 0]
    bars = ax1.bar(range(len(top_indices)), top_scores, color='red', alpha=0.7)
    ax1.set_xlabel('ROI Index')
    ax1.set_ylabel('Importance Score')
    ax1.set_title('Top 20 Most Important ROIs')
    ax1.set_xticks(range(len(top_indices)))
    ax1.set_xticklabels([f'ROI {idx}' for idx in top_indices], rotation=45)
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, top_scores)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{score:.4f}', ha='center', va='bottom', fontsize=8)
    
    # 2. 重要性分数分布
    ax2 = axes[0, 1]
    ax2.hist(roi_importance, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax2.set_xlabel('Importance Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of ROI Importance Scores')
    ax2.grid(True, alpha=0.3)
    
    # 3. 累积重要性分数
    ax3 = axes[1, 0]
    sorted_scores = np.sort(roi_importance)[::-1]
    cumulative_importance = np.cumsum(sorted_scores)
    cumulative_percentage = cumulative_importance / cumulative_importance[-1] * 100
    
    ax3.plot(range(1, len(sorted_scores) + 1), cumulative_percentage, 'g-', linewidth=2)
    ax3.set_xlabel('Number of ROIs')
    ax3.set_ylabel('Cumulative Importance (%)')
    ax3.set_title('Cumulative Importance by ROI Count')
    ax3.grid(True, alpha=0.3)
    
    # 4. 统计信息表格
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    if stats:
        info_text = f"""
        Model Performance:
        • Test Accuracy: {stats['accuracy']:.3f}
        • Correct Predictions: {stats['n_correct']}/{stats['n_samples']}
        
        ROI Importance Statistics:
        • Total ROIs: {len(roi_importance)}
        • Mean Importance: {np.mean(roi_importance):.4f}
        • Std Importance: {np.std(roi_importance):.4f}
        • Max Importance: {np.max(roi_importance):.4f}
        • Min Importance: {np.min(roi_importance):.4f}
        
        Top 5 Most Important ROIs:
        """
        for i, idx in enumerate(top_indices[:5]):
            info_text += f"• ROI {idx}: {roi_importance[idx]:.4f}\n"
    else:
        info_text = f"""
        ROI Importance Statistics:
        • Total ROIs: {len(roi_importance)}
        • Mean Importance: {np.mean(roi_importance):.4f}
        • Std Importance: {np.std(roi_importance):.4f}
        • Max Importance: {np.max(roi_importance):.4f}
        • Min Importance: {np.min(roi_importance):.4f}
        """
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("🚀 开始创建论文风格的脑区重要性可视化...")
    
    # ==== 支持命令行参数 ====
    parser = argparse.ArgumentParser(description='脑区重要性可视化')
    parser.add_argument('--score_path', type=str, default='./importance_scores/roi_importance.npy', help='重要性分数文件路径')
    parser.add_argument('--roi_csv', type=str, default=None, help='带脑区名称的csv（自动高亮TOP-10）')
    parser.add_argument('--atlas_path', type=str, default='atlas_116.nii.gz', help='AAL116 label图（每voxel=ROI编号+1）')
    args = parser.parse_args()
    score_path = args.score_path
    roi_csv = args.roi_csv or score_path.replace('ensemble_importance.npy', 'roi_importance_with_name.csv')
    atlas_path = args.atlas_path

    # 1. 加载重要性分数
    roi_importance = load_importance_scores(score_path)
    if roi_importance is None:
        return
    
    # 2. 加载统计信息
    stats = load_stats()
    
    # 3. 创建ROI mask
    importance_mask, fsaverage = create_roi_mask(roi_importance)
    if importance_mask is None:
        return
    
    # 4. 创建可视化
    print("📈 生成可视化图表...")
    
    # 论文风格的大脑表面图
    fig1 = create_paper_style_visualization(importance_mask, fsaverage, stats)
    fig1.savefig('brain_importance_surface.png', dpi=300, bbox_inches='tight')
    print("💾 保存大脑表面图: brain_importance_surface.png")
    
    # 玻璃脑可视化
    fig2 = create_glass_brain_visualization(roi_importance, fsaverage)
    fig2.savefig('brain_importance_glass.png', dpi=300, bbox_inches='tight')
    print("💾 保存玻璃脑图: brain_importance_glass.png")
    
    # 重要性分数总结
    fig3 = create_importance_summary(roi_importance, stats)
    fig3.savefig('roi_importance_summary.png', dpi=300, bbox_inches='tight')
    print("💾 保存重要性总结: roi_importance_summary.png")

    # === 自动高亮TOP-10 ROI（plot_glass_brain）及分组统计 ===
    import pandas as pd
    import numpy as np
    import nibabel as nib
    from nilearn import plotting
    import os
    if os.path.exists(roi_csv) and os.path.exists(atlas_path):
        df = pd.read_csv(roi_csv)
        top10 = df.head(10)
        print("\nTOP-10 ROI:")
        print(top10[['BrainRegion', 'Importance']])
        # 生成stat_map
        atlas_img = nib.load(atlas_path)
        atlas_data = atlas_img.get_fdata()
        stat_map = np.zeros_like(atlas_data)
        for idx, row in top10.iterrows():
            roi_id = int(row['ROI'])
            stat_map[atlas_data == roi_id + 1] = row['Importance']
        out_path = 'top10_importance_map.nii.gz'
        nib.save(nib.Nifti1Image(stat_map, affine=atlas_img.affine), out_path)
        print(f"已保存TOP-10高亮stat_map: {out_path}")
        plotting.plot_glass_brain(out_path, threshold=np.percentile(top10['Importance'], 90), colorbar=True, title='Top-10 ROI')
        plotting.show()
        # 分组统计
        def region_group(name):
            if 'Frontal' in name: return 'Frontal'
            if 'Temporal' in name: return 'Temporal'
            if 'Parietal' in name: return 'Parietal'
            if 'Occipital' in name: return 'Occipital'
            if 'Insula' in name: return 'Insula'
            if 'Cingulum' in name: return 'Cingulate'
            if 'Hippocampus' in name or 'Amygdala' in name: return 'Limbic'
            if 'Caudate' in name or 'Putamen' in name or 'Pallidum' in name or 'Thalamus' in name: return 'Subcortical'
            if 'Cerebelum' in name or 'Vermis' in name: return 'Cerebellum'
            return 'Other'
        top10['Group'] = top10['BrainRegion'].apply(region_group)
        # 左右半球统计
        top10['Hemisphere'] = top10['BrainRegion'].apply(lambda x: 'L' if x.endswith('_L') else ('R' if x.endswith('_R') else 'Mid'))
        print("\nTOP-10分组统计:")
        print(top10.groupby('Group').size())
        print("左右半球分布:")
        print(top10.groupby('Hemisphere').size())
        print("\n解释建议:")
        print("- 疼痛任务: Insula, Cingulate, Thalamus, Somatosensory等高亮，提示模型关注疼痛感知/调控相关脑区。")
        print("- 调控任务: Prefrontal, Cingulate高亮，提示模型关注认知调控、情绪调节相关脑区。")
        print("- 预期任务: Prefrontal, Striatum, Amygdala高亮，提示模型关注奖赏、动机、情绪相关脑区。\n")
    else:
        print("未找到roi_importance_with_name.csv或atlas_116.nii.gz，跳过TOP-10高亮和分组统计。")

    print("✅ 所有可视化图表已生成完成！")
    print("📁 生成的文件:")
    print("   - brain_importance_surface.png (大脑表面图)")
    print("   - brain_importance_glass.png (玻璃脑图)")
    print("   - roi_importance_summary.png (重要性总结)")
    print("   - top10_importance_map.nii.gz (TOP-10高亮stat_map, 如有atlas)")

if __name__ == '__main__':
    main() 