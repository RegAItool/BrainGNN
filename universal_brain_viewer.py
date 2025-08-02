#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用大脑可视化查看器 - 不依赖特定软件
Universal Brain Viewer - No specific software required
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import os

class UniversalBrainViewer:
    """通用大脑查看器"""
    
    def __init__(self):
        self.setup_brain_data()
        
    def setup_brain_data(self):
        """设置脑区数据"""
        
        # BrainGNN疼痛分类结果
        self.regions = {
            # 疼痛激活区域 (红色)
            'Cerebelum_Crus1_R': {'coords': [28, -77, -33], 'value': 0.601, 'type': 'enhanced'},
            'Cerebelum_Crus1_L': {'coords': [-28, -77, -33], 'value': 0.438, 'type': 'enhanced'},
            'Occipital_Mid_R': {'coords': [31, -87, 11], 'value': 0.528, 'type': 'enhanced'},
            'Occipital_Sup_R': {'coords': [20, -93, 15], 'value': 0.528, 'type': 'enhanced'},
            'Occipital_Mid_L': {'coords': [-31, -87, 11], 'value': 0.385, 'type': 'enhanced'},
            'ParaHippocampal_L': {'coords': [-24, -7, -21], 'value': 0.120, 'type': 'enhanced'},
            'Amygdala_R': {'coords': [25, -1, -20], 'value': 0.080, 'type': 'enhanced'},
            
            # 疼痛抑制区域 (蓝色)
            'Frontal_Sup_L': {'coords': [-15, 26, 56], 'value': 0.512, 'type': 'suppressed'},
            'Frontal_Mid_L': {'coords': [-30, 47, 28], 'value': 0.498, 'type': 'suppressed'},
            'Precentral_L': {'coords': [-39, -6, 52], 'value': 0.433, 'type': 'suppressed'},
            'Postcentral_L': {'coords': [-43, -25, 49], 'value': 0.431, 'type': 'suppressed'},
            'Rolandic_Oper_L': {'coords': [-50, 0, 9], 'value': 0.401, 'type': 'suppressed'},
            'Frontal_Sup_R': {'coords': [15, 26, 56], 'value': 0.394, 'type': 'suppressed'},
            'Putamen_R': {'coords': [26, 6, 0], 'value': 0.386, 'type': 'suppressed'}
        }

    def create_interactive_html_viewer(self):
        """创建交互式HTML查看器"""
        
        print("🌐 Creating interactive HTML brain viewer...")
        
        # 创建大脑表面
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0.1, np.pi - 0.1, 40)
        
        # 大脑椭球参数
        a, b, c = 75, 90, 65
        
        x = np.outer(np.sin(v), np.cos(u)) * a
        y = np.outer(np.sin(v), np.sin(u)) * b
        z = np.outer(np.cos(v), np.ones(np.size(u))) * c
        
        # 大脑形状修正
        for i in range(len(v)):
            for j in range(len(u)):
                # 前额叶突出
                if y[i,j] > 50:
                    y[i,j] *= 1.2
                    z[i,j] *= 0.85
                # 颞叶下垂
                if abs(x[i,j]) > 55 and z[i,j] < 25:
                    z[i,j] -= 25
                    x[i,j] *= 1.15
                # 枕叶后突
                if y[i,j] < -70:
                    y[i,j] *= 1.1
        
        # 计算表面激活
        activation_surface = np.zeros_like(x)
        
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                point = np.array([x[i,j], y[i,j], z[i,j]])
                
                total_activation = 0.0
                for region_name, region_data in self.regions.items():
                    region_coords = np.array(region_data['coords'])
                    distance = np.linalg.norm(point - region_coords)
                    
                    # 高斯衰减
                    sigma = 25.0
                    weight = np.exp(-(distance**2) / (2 * sigma**2))
                    
                    # 根据类型设置符号
                    value = region_data['value']
                    if region_data['type'] == 'suppressed':
                        value = -value
                    
                    total_activation += value * weight
                
                activation_surface[i,j] = total_activation
        
        # 创建Plotly图形
        fig = go.Figure()
        
        # 添加大脑表面
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=activation_surface,
            colorscale='RdBu_r',
            cmin=-0.4, cmax=0.4,
            opacity=0.8,
            name='Brain Surface',
            colorbar=dict(
                title="Pain Response<br>(Red: Enhanced<br>Blue: Suppressed)",
                x=1.02
            ),
            hovertemplate="Brain Surface<br>X: %{x}<br>Y: %{y}<br>Z: %{z}<br>Activation: %{surfacecolor:.3f}<extra></extra>"
        ))
        
        # 添加脑区标记点
        for region_name, region_data in self.regions.items():
            coords = region_data['coords']
            value = region_data['value']
            region_type = region_data['type']
            
            color = 'red' if region_type == 'enhanced' else 'blue'
            size = value * 25 + 10
            
            fig.add_trace(go.Scatter3d(
                x=[coords[0]], y=[coords[1]], z=[coords[2]],
                mode='markers+text',
                marker=dict(
                    size=size, color=color, opacity=0.9,
                    line=dict(width=3, color='white')
                ),
                text=region_name.split('_')[0],
                textposition="top center",
                name=region_name,
                showlegend=False,
                hovertemplate=f"<b>{region_name}</b><br>" +
                             f"Type: {region_type.title()}<br>" +
                             f"Strength: {value:.3f}<br>" +
                             f"Coordinates: {coords}<extra></extra>"
            ))
        
        # 设置布局
        fig.update_layout(
            title=dict(
                text="🧠 BrainGNN Pain Classification - Universal 3D Viewer<br>" +
                     "<sup>98.7% Accuracy | Interactive Brain Visualization | No Special Software Required</sup>",
                x=0.5,
                font=dict(size=16)
            ),
            scene=dict(
                xaxis_title="Left ← X (mm) → Right",
                yaxis_title="Posterior ← Y (mm) → Anterior", 
                zaxis_title="Inferior ← Z (mm) → Superior",
                camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2)),
                aspectmode='cube'
            ),
            height=700,
            font=dict(size=12)
        )
        
        # 保存HTML文件
        html_file = './figures/universal_brain_viewer.html'
        fig.write_html(html_file)
        
        print(f"✅ Interactive viewer created: {html_file}")
        
        # 自动打开
        fig.show()
        
        return html_file

    def create_static_views(self):
        """创建静态多视图"""
        
        print("📸 Creating static multi-view visualization...")
        
        fig = plt.figure(figsize=(16, 12))
        
        # 准备数据
        enhanced_regions = [(name, data) for name, data in self.regions.items() if data['type'] == 'enhanced']
        suppressed_regions = [(name, data) for name, data in self.regions.items() if data['type'] == 'suppressed']
        
        # 视图1: 左侧视图 (Y-Z平面)
        ax1 = fig.add_subplot(2, 3, 1)
        for name, data in enhanced_regions:
            y, z = data['coords'][1], data['coords'][2]
            ax1.scatter(y, z, c='red', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax1.annotate(name.split('_')[0], (y, z), fontsize=8, ha='center')
        
        for name, data in suppressed_regions:
            y, z = data['coords'][1], data['coords'][2]
            ax1.scatter(y, z, c='blue', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax1.annotate(name.split('_')[0], (y, z), fontsize=8, ha='center')
        
        ax1.set_xlabel('Y: Posterior ← → Anterior (mm)')
        ax1.set_ylabel('Z: Inferior ← → Superior (mm)')
        ax1.set_title('Left Side View')
        ax1.grid(True, alpha=0.3)
        
        # 视图2: 顶部视图 (X-Y平面)
        ax2 = fig.add_subplot(2, 3, 2)
        for name, data in enhanced_regions:
            x, y = data['coords'][0], data['coords'][1]
            ax2.scatter(x, y, c='red', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax2.annotate(name.split('_')[0], (x, y), fontsize=8, ha='center')
        
        for name, data in suppressed_regions:
            x, y = data['coords'][0], data['coords'][1]
            ax2.scatter(x, y, c='blue', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax2.annotate(name.split('_')[0], (x, y), fontsize=8, ha='center')
        
        ax2.set_xlabel('X: Left ← → Right (mm)')
        ax2.set_ylabel('Y: Posterior ← → Anterior (mm)')
        ax2.set_title('Top View')
        ax2.grid(True, alpha=0.3)
        
        # 视图3: 前部视图 (X-Z平面)
        ax3 = fig.add_subplot(2, 3, 3)
        for name, data in enhanced_regions:
            x, z = data['coords'][0], data['coords'][2]
            ax3.scatter(x, z, c='red', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax3.annotate(name.split('_')[0], (x, z), fontsize=8, ha='center')
        
        for name, data in suppressed_regions:
            x, z = data['coords'][0], data['coords'][2]
            ax3.scatter(x, z, c='blue', s=data['value']*200+50, alpha=0.7, edgecolors='white')
            ax3.annotate(name.split('_')[0], (x, z), fontsize=8, ha='center')
        
        ax3.set_xlabel('X: Left ← → Right (mm)')
        ax3.set_ylabel('Z: Inferior ← → Superior (mm)')
        ax3.set_title('Front View')
        ax3.grid(True, alpha=0.3)
        
        # 视图4: 3D散点图
        ax4 = fig.add_subplot(2, 3, 4, projection='3d')
        
        for name, data in enhanced_regions:
            x, y, z = data['coords']
            ax4.scatter(x, y, z, c='red', s=data['value']*200+50, alpha=0.7)
        
        for name, data in suppressed_regions:
            x, y, z = data['coords']
            ax4.scatter(x, y, z, c='blue', s=data['value']*200+50, alpha=0.7)
        
        ax4.set_xlabel('X: L ← → R')
        ax4.set_ylabel('Y: P ← → A')
        ax4.set_zlabel('Z: I ← → S')
        ax4.set_title('3D View')
        
        # 视图5: 激活强度柱状图
        ax5 = fig.add_subplot(2, 3, 5)
        
        all_regions = list(self.regions.keys())
        all_values = [self.regions[r]['value'] for r in all_regions]
        all_colors = ['red' if self.regions[r]['type'] == 'enhanced' else 'blue' for r in all_regions]
        
        bars = ax5.barh(range(len(all_regions)), all_values, color=all_colors, alpha=0.7)
        ax5.set_yticks(range(len(all_regions)))
        ax5.set_yticklabels([r.replace('_', ' ') for r in all_regions], fontsize=9)
        ax5.set_xlabel('Activation Strength')
        ax5.set_title('Region Activation')
        ax5.grid(True, axis='x', alpha=0.3)
        
        # 视图6: 统计信息
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.axis('off')
        
        # 统计文本
        stats_text = f"""
BrainGNN Pain Classification Results

🎯 Classification Accuracy: 98.7%
📊 Total Brain Regions: {len(self.regions)}

🔴 Pain Enhanced Regions: {len(enhanced_regions)}
• Cerebellum (bilateral)
• Occipital cortex (bilateral)  
• Parahippocampal gyrus
• Amygdala

🔵 Pain Suppressed Regions: {len(suppressed_regions)}
• Frontal cortex (bilateral)
• Motor/sensory cortex
• Putamen

🧠 Neural Networks:
• Sensorimotor
• Visual processing
• Limbic system
• Executive control

📍 Coordinate System: MNI
📏 Units: millimeters (mm)
        """
        
        ax6.text(0.05, 0.95, stats_text, transform=ax6.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.suptitle('BrainGNN Pain State Classification - Multi-View Analysis\n98.7% Accuracy | 14 Key Brain Regions', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        # 保存图像
        static_file = './figures/universal_brain_multiview.png'
        plt.savefig(static_file, dpi=200, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Static views created: {static_file}")
        
        return static_file

    def create_simple_text_summary(self):
        """创建简单文本总结"""
        
        print("📝 Creating text summary...")
        
        summary = """
# 🧠 BrainGNN Pain Classification Results Summary

## 📊 Overview
- **Task**: Pain vs No-Pain State Classification
- **Accuracy**: 98.7%
- **Method**: Graph Neural Network (BrainGNN)
- **Data**: fMRI brain connectivity
- **Regions**: 14 key brain areas identified

## 🔴 Pain-Enhanced Regions (7 regions)
Regions showing INCREASED activation during pain:

1. **Cerebellum Crus1 (Right)**: [28, -77, -33] - Activation: 0.601
   • Primary sensorimotor integration

2. **Cerebellum Crus1 (Left)**: [-28, -77, -33] - Activation: 0.438
   • Bilateral cerebellar coordination

3. **Occipital Middle (Right)**: [31, -87, 11] - Activation: 0.528
   • Visual-spatial pain processing

4. **Occipital Superior (Right)**: [20, -93, 15] - Activation: 0.528
   • Enhanced visual attention

5. **Occipital Middle (Left)**: [-31, -87, 11] - Activation: 0.385
   • Bilateral visual processing

6. **Parahippocampal (Left)**: [-24, -7, -21] - Activation: 0.120
   • Pain memory encoding

7. **Amygdala (Right)**: [25, -1, -20] - Activation: 0.080
   • Emotional pain response

## 🔵 Pain-Suppressed Regions (7 regions)  
Regions showing DECREASED activation during pain:

1. **Frontal Superior (Left)**: [-15, 26, 56] - Suppression: 0.512
   • Top-down cognitive control

2. **Frontal Middle (Left)**: [-30, 47, 28] - Suppression: 0.498
   • Executive function regulation

3. **Precentral (Left)**: [-39, -6, 52] - Suppression: 0.433
   • Motor cortex inhibition

4. **Postcentral (Left)**: [-43, -25, 49] - Suppression: 0.431
   • Sensory cortex regulation

5. **Rolandic Operculum (Left)**: [-50, 0, 9] - Suppression: 0.401
   • Sensorimotor integration

6. **Frontal Superior (Right)**: [15, 26, 56] - Suppression: 0.394
   • Bilateral cognitive control

7. **Putamen (Right)**: [26, 6, 0] - Suppression: 0.386
   • Motor regulation suppression

## 🧭 Neural Networks Involved
- **Sensorimotor Network**: Pain sensing and motor response
- **Visual Network**: Visual-spatial pain processing  
- **Limbic Network**: Emotional and memory aspects
- **Executive Network**: Cognitive control and regulation

## 📍 Technical Details
- **Coordinate System**: MNI (Montreal Neurological Institute)
- **Units**: Millimeters (mm)
- **Hemispheres**: L = Left, R = Right
- **Classification**: Binary (Pain vs No-Pain)

---
Generated by BrainGNN Pain Classification System
🎯 Professional Neuroscience Analysis
        """
        
        summary_file = './figures/braingnn_pain_summary.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ Text summary created: {summary_file}")
        
        return summary_file

    def run_all_visualizations(self):
        """运行所有可视化"""
        
        print("🚀 Creating Universal Brain Visualization Suite...")
        print("🧠 No special software required - works on any computer!")
        
        # 创建各种格式的可视化
        html_file = self.create_interactive_html_viewer()
        static_file = self.create_static_views()  
        summary_file = self.create_simple_text_summary()
        
        print("\n✅ Universal Brain Visualization Suite Complete!")
        print("\n📂 Generated Files:")
        print(f"  🌐 Interactive 3D: {html_file}")
        print(f"  📸 Static views: {static_file}")  
        print(f"  📝 Text summary: {summary_file}")
        
        print("\n🎯 How to View:")
        print("  • Double-click the HTML file for 3D interaction")
        print("  • Open the PNG file for static views")
        print("  • Read the TXT file for detailed results")
        
        print("\n💡 These work on ANY computer:")
        print("  ✅ No SurfIce needed")
        print("  ✅ No special software needed") 
        print("  ✅ Just web browser and image viewer")
        
        return {
            'html': html_file,
            'static': static_file,
            'summary': summary_file
        }

def main():
    """主函数"""
    print("=" * 60)
    print("🧠 Universal Brain Viewer")
    print("🎯 Works without SurfIce or any special software!")
    print("=" * 60)
    
    # 创建通用查看器
    viewer = UniversalBrainViewer()
    
    # 运行所有可视化
    files = viewer.run_all_visualizations()
    
    print("\n" + "=" * 60)
    print("🎉 Success! Your brain visualization is ready!")
    print("🌐 Open the HTML file in any web browser!")
    print("=" * 60)

if __name__ == "__main__":
    main()