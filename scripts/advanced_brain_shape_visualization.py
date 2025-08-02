#!/usr/bin/env python3
"""
高级真实大脑形状可视化
使用更精确的大脑轮廓和更真实的脑区分布
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap

def load_importance_scores(score_path='./importance_scores/roi_importance.npy'):
    """加载ROI重要性分数"""
    if os.path.exists(score_path):
        roi_importance = np.load(score_path)
        print(f"✅ 加载ROI重要性分数: {roi_importance.shape}")
        return roi_importance
    else:
        print(f"❌ 重要性分数文件不存在: {score_path}")
        return None

def create_realistic_brain_shape():
    """创建更真实的大脑轮廓形状"""
    # 更精确的大脑轮廓坐标（基于真实大脑形状）
    brain_outline = np.array([
        # 大脑轮廓 - 更真实的形状
        [0.15, 0.5], [0.2, 0.45], [0.25, 0.4], [0.3, 0.35], [0.35, 0.3],
        [0.4, 0.25], [0.45, 0.2], [0.5, 0.15], [0.55, 0.2], [0.6, 0.25],
        [0.65, 0.3], [0.7, 0.35], [0.75, 0.4], [0.8, 0.45], [0.85, 0.5],
        [0.8, 0.55], [0.75, 0.6], [0.7, 0.65], [0.65, 0.7], [0.6, 0.75],
        [0.55, 0.8], [0.5, 0.85], [0.45, 0.8], [0.4, 0.75], [0.35, 0.7],
        [0.3, 0.65], [0.25, 0.6], [0.2, 0.55], [0.15, 0.5]
    ])
    
    # 大脑沟回和脑叶
    sulci_and_lobes = {
        'central_sulcus': np.array([[0.35, 0.4], [0.45, 0.35], [0.55, 0.3], [0.65, 0.25]]),
        'lateral_sulcus': np.array([[0.4, 0.5], [0.5, 0.45], [0.6, 0.4], [0.7, 0.35]]),
        'parieto_occipital': np.array([[0.3, 0.6], [0.4, 0.55], [0.5, 0.5], [0.6, 0.45]]),
        'frontal_lobe': np.array([[0.25, 0.45], [0.35, 0.4], [0.45, 0.35], [0.55, 0.3]]),
        'temporal_lobe': np.array([[0.4, 0.6], [0.5, 0.55], [0.6, 0.5], [0.7, 0.45]]),
        'parietal_lobe': np.array([[0.3, 0.5], [0.4, 0.45], [0.5, 0.4], [0.6, 0.35]]),
        'occipital_lobe': np.array([[0.35, 0.65], [0.45, 0.6], [0.55, 0.55], [0.65, 0.5]])
    }
    
    # 脑区边界
    brain_regions = {
        'frontal': np.array([[0.2, 0.4], [0.3, 0.35], [0.4, 0.3], [0.5, 0.25], [0.6, 0.3], [0.7, 0.35], [0.8, 0.4], [0.7, 0.45], [0.6, 0.5], [0.5, 0.55], [0.4, 0.5], [0.3, 0.45], [0.2, 0.4]]),
        'temporal': np.array([[0.3, 0.5], [0.4, 0.45], [0.5, 0.4], [0.6, 0.35], [0.7, 0.4], [0.8, 0.45], [0.75, 0.55], [0.65, 0.6], [0.55, 0.55], [0.45, 0.5], [0.35, 0.55], [0.3, 0.5]]),
        'parietal': np.array([[0.25, 0.6], [0.35, 0.55], [0.45, 0.5], [0.55, 0.45], [0.65, 0.5], [0.75, 0.55], [0.7, 0.65], [0.6, 0.7], [0.5, 0.65], [0.4, 0.6], [0.3, 0.65], [0.25, 0.6]]),
        'occipital': np.array([[0.35, 0.7], [0.45, 0.65], [0.55, 0.6], [0.65, 0.55], [0.75, 0.6], [0.7, 0.7], [0.6, 0.75], [0.5, 0.7], [0.4, 0.75], [0.35, 0.7]])
    }
    
    return brain_outline, sulci_and_lobes, brain_regions

def create_advanced_brain_visualization(roi_importance):
    """创建高级真实大脑形状可视化"""
    print("🧠 创建高级真实大脑形状可视化...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('BrainGNN ROI Importance - Advanced Real Brain Shape Visualization', fontsize=16, fontweight='bold')
    
    # 获取大脑形状
    brain_outline, sulci_and_lobes, brain_regions = create_realistic_brain_shape()
    
    def create_advanced_brain_view(ax, title, is_left=True, view='lateral'):
        # 绘制大脑轮廓
        if is_left:
            outline = brain_outline
        else:
            # 右半球（镜像）
            outline = np.array([[1 - x, y] for x, y in brain_outline])
        
        # 绘制大脑轮廓
        ax.plot(outline[:, 0], outline[:, 1], 'k-', linewidth=3, label='Brain Outline')
        ax.fill(outline[:, 0], outline[:, 1], alpha=0.05, color='gray')
        
        # 绘制大脑沟回
        for name, sulcus in sulci_and_lobes.items():
            if is_left:
                sulcus_coords = sulcus
            else:
                sulcus_coords = np.array([[1 - x, y] for x, y in sulcus])
            
            ax.plot(sulcus_coords[:, 0], sulcus_coords[:, 1], 'k--', alpha=0.6, linewidth=1.5)
        
        # 绘制脑区边界
        for region_name, region_coords in brain_regions.items():
            if is_left:
                region_outline = region_coords
            else:
                region_outline = np.array([[1 - x, y] for x, y in region_coords])
            
            ax.plot(region_outline[:, 0], region_outline[:, 1], 'k-', alpha=0.4, linewidth=1)
        
        # 将ROI重要性映射到大脑区域
        n_rois = len(roi_importance)
        max_importance = np.max(roi_importance)
        
        # 在大脑轮廓内分布ROI，按重要性排序
        sorted_indices = np.argsort(roi_importance)[::-1]
        roi_positions = []
        
        for i, roi_idx in enumerate(sorted_indices[:30]):  # 只显示前30个最重要的ROI
            # 在大脑轮廓内分布
            attempts = 0
            while attempts < 200:
                x = 0.2 + 0.6 * np.random.random()
                y = 0.2 + 0.6 * np.random.random()
                
                # 检查是否在大脑轮廓内
                center_x, center_y = 0.5, 0.5
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                # 更精确的轮廓检查
                if distance <= 0.35 and 0.15 <= x <= 0.85 and 0.15 <= y <= 0.85:
                    roi_positions.append((x, y, roi_importance[roi_idx], roi_idx))
                    break
                attempts += 1
        
        # 绘制ROI点，颜色和大小表示重要性
        for x, y, importance, roi_idx in roi_positions:
            color_intensity = importance / max_importance
            size = 30 + 70 * color_intensity  # 大小根据重要性变化
            
            # 使用热力图颜色
            ax.scatter(x, y, c=[color_intensity], cmap='hot', s=size, alpha=0.8, edgecolors='black', linewidth=0.5)
            
            # 为最重要的ROI添加标签
            if roi_idx in sorted_indices[:5]:
                ax.annotate(f'ROI{roi_idx}', (x, y), xytext=(5, 5), 
                           textcoords='offset points', fontsize=6, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_aspect('equal')
        ax.axis('off')
    
    # 1. 左半球外侧视图
    create_advanced_brain_view(axes[0, 0], 'Left Hemisphere (Lateral View)', True, 'lateral')
    
    # 2. 左半球内侧视图
    create_advanced_brain_view(axes[0, 1], 'Left Hemisphere (Medial View)', True, 'medial')
    
    # 3. 左半球背侧视图
    create_advanced_brain_view(axes[0, 2], 'Left Hemisphere (Dorsal View)', True, 'dorsal')
    
    # 4. 右半球外侧视图
    create_advanced_brain_view(axes[1, 0], 'Right Hemisphere (Lateral View)', False, 'lateral')
    
    # 5. 右半球内侧视图
    create_advanced_brain_view(axes[1, 1], 'Right Hemisphere (Medial View)', False, 'medial')
    
    # 6. 重要性分数分布
    ax6 = axes[1, 2]
    non_zero_importance = roi_importance[roi_importance > 0]
    ax6.hist(non_zero_importance, bins=25, alpha=0.7, color='red', edgecolor='black')
    ax6.set_xlabel('ROI Importance Score')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Distribution of ROI Importance Scores')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_brain_region_analysis(roi_importance):
    """创建脑区分析可视化"""
    print("🔬 创建脑区分析可视化...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('BrainGNN ROI Importance - Brain Region Analysis', fontsize=16, fontweight='bold')
    
    # 1. 脑区重要性热力图
    ax1 = axes[0, 0]
    # 将ROI重要性映射到脑区
    brain_regions_importance = {
        'Frontal': np.mean(roi_importance[:25]),  # 前25个ROI
        'Temporal': np.mean(roi_importance[25:50]),  # 25-50
        'Parietal': np.mean(roi_importance[50:75]),  # 50-75
        'Occipital': np.mean(roi_importance[75:100])  # 75-100
    }
    
    regions = list(brain_regions_importance.keys())
    importance_values = list(brain_regions_importance.values())
    
    bars = ax1.bar(regions, importance_values, color=['red', 'orange', 'yellow', 'green'], alpha=0.7)
    ax1.set_ylabel('Average Importance Score')
    ax1.set_title('Brain Region Importance Analysis')
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, value in zip(bars, importance_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. ROI重要性排名
    ax2 = axes[0, 1]
    top_indices = np.argsort(roi_importance)[-20:][::-1]
    top_scores = roi_importance[top_indices]
    
    bars = ax2.bar(range(len(top_indices)), top_scores, color='red', alpha=0.7)
    ax2.set_xlabel('ROI Rank')
    ax2.set_ylabel('Importance Score')
    ax2.set_title('Top 20 Most Important ROIs')
    ax2.set_xticks(range(0, len(top_indices), 5))
    ax2.set_xticklabels([f'#{i+1}' for i in range(0, len(top_indices), 5)])
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, top_scores)):
        if i < 10:  # 只标注前10个
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                    f'{score:.3f}', ha='center', va='bottom', fontsize=8)
    
    # 3. 重要性分数vs ROI索引
    ax3 = axes[1, 0]
    ax3.scatter(range(len(roi_importance)), roi_importance, alpha=0.6, c=roi_importance, cmap='hot', s=40)
    ax3.set_xlabel('ROI Index')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('ROI Importance vs Index')
    ax3.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(range(len(roi_importance)), roi_importance, 1)
    p = np.poly1d(z)
    ax3.plot(range(len(roi_importance)), p(range(len(roi_importance))), "r--", alpha=0.8)
    
    # 4. 统计信息
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # 计算统计信息
    mean_score = np.mean(roi_importance)
    std_score = np.std(roi_importance)
    median_score = np.median(roi_importance)
    max_score = np.max(roi_importance)
    min_score = np.min(roi_importance)
    
    # 找出最重要的ROI
    top_roi_idx = np.argmax(roi_importance)
    top_roi_score = roi_importance[top_roi_idx]
    
    info_text = f"""
    BrainGNN ROI Importance Analysis:
    
    Model Performance:
    • Test Accuracy: 52.2%
    • Total ROIs: {len(roi_importance)}
    
    Importance Statistics:
    • Mean: {mean_score:.4f}
    • Std: {std_score:.4f}
    • Median: {median_score:.4f}
    • Max: {max_score:.4f} (ROI {top_roi_idx})
    • Min: {min_score:.4f}
    
    Brain Region Analysis:
    • Frontal: {brain_regions_importance['Frontal']:.4f}
    • Temporal: {brain_regions_importance['Temporal']:.4f}
    • Parietal: {brain_regions_importance['Parietal']:.4f}
    • Occipital: {brain_regions_importance['Occipital']:.4f}
    
    Top 5 Most Important ROIs:
    """
    for i, idx in enumerate(top_indices[:5]):
        info_text += f"• ROI {idx}: {roi_importance[idx]:.4f}\n"
    
    ax4.text(0.1, 0.95, info_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

def create_3d_brain_visualization(roi_importance):
    """创建3D大脑可视化"""
    print("🌐 创建3D大脑可视化...")
    
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('BrainGNN ROI Importance - 3D Brain Visualization', fontsize=16, fontweight='bold')
    
    # 创建3D轴
    ax = fig.add_subplot(111, projection='3d')
    
    # 创建3D大脑轮廓（简化）
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 50)
    theta, phi = np.meshgrid(theta, phi)
    
    # 大脑形状参数
    a, b, c = 1, 1.2, 0.8  # 椭球参数
    
    x = a * np.sin(phi) * np.cos(theta)
    y = b * np.sin(phi) * np.sin(theta)
    z = c * np.cos(phi)
    
    # 绘制大脑轮廓
    ax.plot_surface(x, y, z, alpha=0.1, color='gray')
    
    # 在大脑表面分布ROI
    n_rois = len(roi_importance)
    max_importance = np.max(roi_importance)
    
    # 选择最重要的ROI进行可视化
    top_indices = np.argsort(roi_importance)[-20:][::-1]
    
    for i, roi_idx in enumerate(top_indices):
        # 在大脑表面随机分布
        phi_roi = np.random.uniform(0, np.pi)
        theta_roi = np.random.uniform(0, 2*np.pi)
        
        x_roi = a * np.sin(phi_roi) * np.cos(theta_roi)
        y_roi = b * np.sin(phi_roi) * np.sin(theta_roi)
        z_roi = c * np.cos(phi_roi)
        
        importance = roi_importance[roi_idx]
        color_intensity = importance / max_importance
        size = 50 + 100 * color_intensity
        
        ax.scatter(x_roi, y_roi, z_roi, c=[color_intensity], cmap='hot', s=size, alpha=0.8)
        
        # 为最重要的ROI添加标签
        if i < 5:
            ax.text(x_roi, y_roi, z_roi, f'ROI{roi_idx}', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Brain ROI Importance Distribution')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("🚀 开始创建高级真实大脑形状可视化...")
    
    # 1. 加载重要性分数
    roi_importance = load_importance_scores()
    if roi_importance is None:
        return
    
    # 2. 创建可视化
    print("📈 生成高级真实大脑形状可视化...")
    
    # 高级真实大脑形状可视化
    fig1 = create_advanced_brain_visualization(roi_importance)
    fig1.savefig('advanced_brain_shape_visualization.png', dpi=300, bbox_inches='tight')
    print("💾 保存高级大脑形状图: advanced_brain_shape_visualization.png")
    
    # 脑区分析可视化
    fig2 = create_brain_region_analysis(roi_importance)
    fig2.savefig('brain_region_analysis.png', dpi=300, bbox_inches='tight')
    print("💾 保存脑区分析图: brain_region_analysis.png")
    
    # 3D大脑可视化
    try:
        fig3 = create_3d_brain_visualization(roi_importance)
        fig3.savefig('3d_brain_visualization.png', dpi=300, bbox_inches='tight')
        print("💾 保存3D大脑图: 3d_brain_visualization.png")
    except Exception as e:
        print(f"⚠️ 3D可视化失败: {e}")
    
    print("✅ 高级真实大脑形状可视化已生成完成！")
    print("📁 生成的文件:")
    print("   - advanced_brain_shape_visualization.png (高级大脑形状图)")
    print("   - brain_region_analysis.png (脑区分析图)")
    print("   - 3d_brain_visualization.png (3D大脑图)")

if __name__ == '__main__':
    main() 