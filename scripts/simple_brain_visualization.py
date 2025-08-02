#!/usr/bin/env python3
"""
简化的脑区重要性可视化
使用BrainGNN导出的ROI重要性分数生成论文风格的可视化
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

def load_stats(stats_path='./importance_scores/stats.pkl'):
    """加载统计信息"""
    if os.path.exists(stats_path):
        with open(stats_path, 'rb') as f:
            stats = pickle.load(f)
        print(f"📊 模型性能: 准确率 {stats['accuracy']:.3f}")
        return stats
    return None

def create_brain_heatmap(roi_importance, stats=None):
    """创建大脑ROI热力图"""
    print("🎨 创建大脑ROI热力图...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # 1. ROI重要性热力图
    ax1 = axes[0, 0]
    # 将ROI重要性重塑为2D矩阵（假设是方形布局）
    n_rois = len(roi_importance)
    side_length = int(np.ceil(np.sqrt(n_rois)))
    
    # 创建2D矩阵
    heatmap_matrix = np.zeros((side_length, side_length))
    for i in range(n_rois):
        row = i // side_length
        col = i % side_length
        if row < side_length and col < side_length:
            heatmap_matrix[row, col] = roi_importance[i]
    
    # 绘制热力图
    im1 = ax1.imshow(heatmap_matrix, cmap='hot', aspect='auto')
    ax1.set_title('Brain ROI Importance Heatmap', fontsize=14, fontweight='bold')
    ax1.set_xlabel('ROI Column')
    ax1.set_ylabel('ROI Row')
    plt.colorbar(im1, ax=ax1, label='Importance Score')
    
    # 2. 前20个最重要ROI的条形图
    ax2 = axes[0, 1]
    top_indices = np.argsort(roi_importance)[-20:][::-1]
    top_scores = roi_importance[top_indices]
    
    bars = ax2.bar(range(len(top_indices)), top_scores, color='red', alpha=0.7)
    ax2.set_xlabel('ROI Index')
    ax2.set_ylabel('Importance Score')
    ax2.set_title('Top 20 Most Important ROIs', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(top_indices)))
    ax2.set_xticklabels([f'ROI {idx}' for idx in top_indices], rotation=45)
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, top_scores)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{score:.4f}', ha='center', va='bottom', fontsize=8)
    
    # 3. 重要性分数分布
    ax3 = axes[1, 0]
    ax3.hist(roi_importance, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax3.set_xlabel('Importance Score')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of ROI Importance Scores', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 添加统计信息
    mean_score = np.mean(roi_importance)
    std_score = np.std(roi_importance)
    ax3.axvline(mean_score, color='red', linestyle='--', label=f'Mean: {mean_score:.4f}')
    ax3.axvline(mean_score + std_score, color='orange', linestyle=':', label=f'+1 STD: {mean_score + std_score:.4f}')
    ax3.axvline(mean_score - std_score, color='orange', linestyle=':', label=f'-1 STD: {mean_score - std_score:.4f}')
    ax3.legend()
    
    # 4. 累积重要性分数
    ax4 = axes[1, 1]
    sorted_scores = np.sort(roi_importance)[::-1]
    cumulative_importance = np.cumsum(sorted_scores)
    cumulative_percentage = cumulative_importance / cumulative_importance[-1] * 100
    
    ax4.plot(range(1, len(sorted_scores) + 1), cumulative_percentage, 'g-', linewidth=2)
    ax4.set_xlabel('Number of ROIs')
    ax4.set_ylabel('Cumulative Importance (%)')
    ax4.set_title('Cumulative Importance by ROI Count', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 添加80%和90%标记线
    ax4.axhline(80, color='red', linestyle='--', alpha=0.7, label='80%')
    ax4.axhline(90, color='orange', linestyle='--', alpha=0.7, label='90%')
    ax4.legend()
    
    # 添加统计信息
    if stats:
        fig.suptitle(
            f'BrainGNN ROI Importance Analysis\n'
            f'ABIDE Dataset | Test Accuracy: {stats["accuracy"]:.3f} | '
            f'Correct Predictions: {stats["n_correct"]}/{stats["n_samples"]}',
            fontsize=16, fontweight='bold'
        )
    else:
        fig.suptitle('BrainGNN ROI Importance Analysis', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_importance_summary(roi_importance, stats=None):
    """创建重要性分数总结图"""
    print("📊 创建重要性分数总结...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 重要性分数排序图
    ax1 = axes[0, 0]
    sorted_scores = np.sort(roi_importance)[::-1]
    ax1.plot(range(1, len(sorted_scores) + 1), sorted_scores, 'b-', linewidth=2)
    ax1.set_xlabel('ROI Rank')
    ax1.set_ylabel('Importance Score')
    ax1.set_title('ROI Importance Scores (Ranked)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. 重要性分数箱线图
    ax2 = axes[0, 1]
    ax2.boxplot(roi_importance, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    ax2.set_ylabel('Importance Score')
    ax2.set_title('ROI Importance Score Distribution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. 重要性分数密度图
    ax3 = axes[1, 0]
    ax3.hist(roi_importance, bins=30, density=True, alpha=0.7, color='green', edgecolor='black')
    ax3.set_xlabel('Importance Score')
    ax3.set_ylabel('Density')
    ax3.set_title('ROI Importance Score Density', fontsize=14, fontweight='bold')
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
        • Median Importance: {np.median(roi_importance):.4f}
        
        Top 5 Most Important ROIs:
        """
        top_indices = np.argsort(roi_importance)[-5:][::-1]
        for i, idx in enumerate(top_indices):
            info_text += f"• ROI {idx}: {roi_importance[idx]:.4f}\n"
    else:
        info_text = f"""
        ROI Importance Statistics:
        • Total ROIs: {len(roi_importance)}
        • Mean Importance: {np.mean(roi_importance):.4f}
        • Std Importance: {np.std(roi_importance):.4f}
        • Max Importance: {np.max(roi_importance):.4f}
        • Min Importance: {np.min(roi_importance):.4f}
        • Median Importance: {np.median(roi_importance):.4f}
        """
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

def create_brain_atlas_visualization(roi_importance):
    """创建大脑atlas可视化"""
    print("🧠 创建大脑atlas可视化...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 大脑区域重要性映射（简化版）
    ax1 = axes[0, 0]
    # 创建大脑轮廓的简化表示
    brain_outline = plt.Circle((0.5, 0.5), 0.4, fill=False, color='black', linewidth=2)
    ax1.add_patch(brain_outline)
    
    # 将ROI重要性映射到大脑区域
    n_rois = len(roi_importance)
    for i in range(min(n_rois, 50)):  # 只显示前50个ROI
        angle = 2 * np.pi * i / n_rois
        radius = 0.3 + 0.1 * (roi_importance[i] / np.max(roi_importance))
        x = 0.5 + radius * np.cos(angle)
        y = 0.5 + radius * np.sin(angle)
        
        # 根据重要性设置颜色
        color_intensity = roi_importance[i] / np.max(roi_importance)
        ax1.scatter(x, y, c=[color_intensity], cmap='hot', s=50, alpha=0.7)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('Brain ROI Importance Mapping', fontsize=14, fontweight='bold')
    ax1.set_aspect('equal')
    
    # 2. 重要性分数分布
    ax2 = axes[0, 1]
    ax2.hist(roi_importance, bins=20, alpha=0.7, color='red', edgecolor='black')
    ax2.set_xlabel('Importance Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('ROI Importance Distribution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. 重要性分数vs ROI索引
    ax3 = axes[1, 0]
    ax3.scatter(range(len(roi_importance)), roi_importance, alpha=0.6, c=roi_importance, cmap='hot')
    ax3.set_xlabel('ROI Index')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('ROI Importance vs Index', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. 重要性分数统计
    ax4 = axes[1, 1]
    stats_data = [np.mean(roi_importance), np.std(roi_importance), 
                  np.max(roi_importance), np.min(roi_importance)]
    stats_labels = ['Mean', 'Std', 'Max', 'Min']
    bars = ax4.bar(stats_labels, stats_data, color=['blue', 'green', 'red', 'orange'])
    ax4.set_ylabel('Value')
    ax4.set_title('ROI Importance Statistics', fontsize=14, fontweight='bold')
    
    # 添加数值标签
    for bar, value in zip(bars, stats_data):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{value:.4f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("🚀 开始创建简化的脑区重要性可视化...")
    
    # 1. 加载重要性分数
    roi_importance = load_importance_scores()
    if roi_importance is None:
        return
    
    # 2. 加载统计信息
    stats = load_stats()
    
    # 3. 创建可视化
    print("📈 生成可视化图表...")
    
    # 大脑热力图
    fig1 = create_brain_heatmap(roi_importance, stats)
    fig1.savefig('brain_importance_heatmap.png', dpi=300, bbox_inches='tight')
    print("💾 保存大脑热力图: brain_importance_heatmap.png")
    
    # 重要性总结
    fig2 = create_importance_summary(roi_importance, stats)
    fig2.savefig('roi_importance_summary.png', dpi=300, bbox_inches='tight')
    print("💾 保存重要性总结: roi_importance_summary.png")
    
    # 大脑atlas可视化
    fig3 = create_brain_atlas_visualization(roi_importance)
    fig3.savefig('brain_atlas_visualization.png', dpi=300, bbox_inches='tight')
    print("💾 保存大脑atlas可视化: brain_atlas_visualization.png")
    
    print("✅ 所有可视化图表已生成完成！")
    print("📁 生成的文件:")
    print("   - brain_importance_heatmap.png (大脑热力图)")
    print("   - roi_importance_summary.png (重要性总结)")
    print("   - brain_atlas_visualization.png (大脑atlas可视化)")

if __name__ == '__main__':
    main() 