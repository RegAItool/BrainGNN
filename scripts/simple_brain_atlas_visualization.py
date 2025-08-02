#!/usr/bin/env python3
"""
简单但有效的大脑atlas可视化
使用matplotlib绘制大脑轮廓并高亮重要区域
"""

import numpy as np
import matplotlib.pyplot as plt
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

def create_brain_outline_visualization(roi_importance):
    """创建大脑轮廓可视化"""
    print("🧠 创建大脑轮廓可视化...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('BrainGNN ROI Importance - Brain Atlas Visualization', fontsize=16, fontweight='bold')
    
    # 定义大脑轮廓的坐标（简化版）
    def create_brain_outline(ax, title, is_left=True):
        # 创建大脑轮廓
        brain_outline = plt.Circle((0.5, 0.5), 0.4, fill=False, color='black', linewidth=2)
        ax.add_patch(brain_outline)
        
        # 添加大脑沟回
        sulci = [
            plt.Circle((0.3, 0.6), 0.05, fill=False, color='gray', alpha=0.5),
            plt.Circle((0.7, 0.6), 0.05, fill=False, color='gray', alpha=0.5),
            plt.Circle((0.5, 0.3), 0.05, fill=False, color='gray', alpha=0.5),
            plt.Circle((0.5, 0.7), 0.05, fill=False, color='gray', alpha=0.5),
        ]
        for sulcus in sulci:
            ax.add_patch(sulcus)
        
        # 将ROI重要性映射到大脑区域
        n_rois = len(roi_importance)
        max_importance = np.max(roi_importance)
        
        # 创建ROI区域
        roi_positions = []
        for i in range(min(n_rois, 50)):  # 只显示前50个ROI
            # 在大脑轮廓内随机分布ROI
            angle = 2 * np.pi * i / n_rois
            radius = 0.2 + 0.15 * np.random.random()
            x = 0.5 + radius * np.cos(angle)
            y = 0.5 + radius * np.sin(angle)
            
            # 确保在轮廓内
            if (x - 0.5)**2 + (y - 0.5)**2 <= 0.16:
                roi_positions.append((x, y, roi_importance[i]))
        
        # 绘制ROI点，颜色表示重要性
        for x, y, importance in roi_positions:
            color_intensity = importance / max_importance
            ax.scatter(x, y, c=[color_intensity], cmap='hot', s=50, alpha=0.7)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_aspect('equal')
        ax.axis('off')
    
    # 1. 左半球外侧视图
    create_brain_outline(axes[0, 0], 'Left Hemisphere (Lateral)', True)
    
    # 2. 左半球内侧视图
    create_brain_outline(axes[0, 1], 'Left Hemisphere (Medial)', True)
    
    # 3. 左半球背侧视图
    create_brain_outline(axes[0, 2], 'Left Hemisphere (Dorsal)', True)
    
    # 4. 右半球外侧视图
    create_brain_outline(axes[1, 0], 'Right Hemisphere (Lateral)', False)
    
    # 5. 右半球内侧视图
    create_brain_outline(axes[1, 1], 'Right Hemisphere (Medial)', False)
    
    # 6. 重要性分数分布
    ax6 = axes[1, 2]
    non_zero_importance = roi_importance[roi_importance > 0]
    ax6.hist(non_zero_importance, bins=20, alpha=0.7, color='red', edgecolor='black')
    ax6.set_xlabel('ROI Importance Score')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Distribution of ROI Importance Scores')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_brain_region_visualization(roi_importance):
    """创建大脑区域可视化"""
    print("🗺️ 创建大脑区域可视化...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('BrainGNN ROI Importance - Brain Region Analysis', fontsize=16, fontweight='bold')
    
    # 1. 大脑区域重要性热力图
    ax1 = axes[0, 0]
    # 将ROI重要性重塑为2D矩阵
    n_rois = len(roi_importance)
    side_length = int(np.ceil(np.sqrt(n_rois)))
    
    heatmap_matrix = np.zeros((side_length, side_length))
    for i in range(n_rois):
        row = i // side_length
        col = i % side_length
        if row < side_length and col < side_length:
            heatmap_matrix[row, col] = roi_importance[i]
    
    im1 = ax1.imshow(heatmap_matrix, cmap='hot', aspect='auto')
    ax1.set_title('Brain ROI Importance Heatmap')
    ax1.set_xlabel('ROI Column')
    ax1.set_ylabel('ROI Row')
    plt.colorbar(im1, ax=ax1, label='Importance Score')
    
    # 2. 前15个最重要ROI
    ax2 = axes[0, 1]
    top_indices = np.argsort(roi_importance)[-15:][::-1]
    top_scores = roi_importance[top_indices]
    
    bars = ax2.bar(range(len(top_indices)), top_scores, color='red', alpha=0.7)
    ax2.set_xlabel('ROI Index')
    ax2.set_ylabel('Importance Score')
    ax2.set_title('Top 15 Most Important ROIs')
    ax2.set_xticks(range(len(top_indices)))
    ax2.set_xticklabels([f'ROI {idx}' for idx in top_indices], rotation=45, fontsize=8)
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, top_scores)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{score:.4f}', ha='center', va='bottom', fontsize=6)
    
    # 3. 重要性分数vs ROI索引
    ax3 = axes[1, 0]
    ax3.scatter(range(len(roi_importance)), roi_importance, alpha=0.6, c=roi_importance, cmap='hot', s=30)
    ax3.set_xlabel('ROI Index')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('ROI Importance vs Index')
    ax3.grid(True, alpha=0.3)
    
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
    • Median: {np.median(roi_importance):.4f}
    
    Top 5 Most Important ROIs:
    """
    for i, idx in enumerate(top_indices[:5]):
        info_text += f"• ROI {idx}: {roi_importance[idx]:.4f}\n"
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

def create_brain_atlas_mapping(roi_importance):
    """创建大脑atlas映射"""
    print("📊 创建大脑atlas映射...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('BrainGNN ROI Importance - Atlas Mapping', fontsize=16, fontweight='bold')
    
    # 1. CC200 Atlas ROI重要性映射
    ax1 = axes[0, 0]
    # 将重要性分数映射到CC200 atlas ROI
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
    
    # 添加统计线
    mean_score = np.mean(roi_importance)
    std_score = np.std(roi_importance)
    ax2.axvline(mean_score, color='red', linestyle='--', label=f'Mean: {mean_score:.4f}')
    ax2.axvline(mean_score + std_score, color='orange', linestyle=':', label=f'+1 STD: {mean_score + std_score:.4f}')
    ax2.axvline(mean_score - std_score, color='orange', linestyle=':', label=f'-1 STD: {mean_score - std_score:.4f}')
    ax2.legend()
    
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
    
    # 添加80%和90%标记线
    ax3.axhline(80, color='red', linestyle='--', alpha=0.7, label='80%')
    ax3.axhline(90, color='orange', linestyle='--', alpha=0.7, label='90%')
    ax3.legend()
    
    # 4. 重要性分数箱线图
    ax4 = axes[1, 1]
    ax4.boxplot(roi_importance, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    ax4.set_ylabel('Importance Score')
    ax4.set_title('ROI Importance Score Distribution')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("🚀 开始创建简单但有效的大脑可视化...")
    
    # 1. 加载重要性分数
    roi_importance = load_importance_scores()
    if roi_importance is None:
        return
    
    # 2. 创建可视化
    print("📈 生成大脑可视化...")
    
    # 大脑轮廓可视化
    fig1 = create_brain_outline_visualization(roi_importance)
    fig1.savefig('brain_outline_visualization.png', dpi=300, bbox_inches='tight')
    print("💾 保存大脑轮廓图: brain_outline_visualization.png")
    
    # 大脑区域可视化
    fig2 = create_brain_region_visualization(roi_importance)
    fig2.savefig('brain_region_visualization.png', dpi=300, bbox_inches='tight')
    print("💾 保存大脑区域图: brain_region_visualization.png")
    
    # Atlas映射可视化
    fig3 = create_brain_atlas_mapping(roi_importance)
    fig3.savefig('brain_atlas_mapping.png', dpi=300, bbox_inches='tight')
    print("💾 保存Atlas映射图: brain_atlas_mapping.png")
    
    print("✅ 大脑可视化已生成完成！")
    print("📁 生成的文件:")
    print("   - brain_outline_visualization.png (大脑轮廓图)")
    print("   - brain_region_visualization.png (大脑区域图)")
    print("   - brain_atlas_mapping.png (Atlas映射图)")

if __name__ == '__main__':
    main() 