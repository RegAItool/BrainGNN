#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotly 3D 脑图可视化 - 浏览器查看
替代ParaView的简单可靠方案
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class Plotly3DBrainViewer:
    """Plotly 3D脑图查看器"""
    
    def __init__(self):
        self.setup_brain_data()
        
    def setup_brain_data(self):
        """设置脑区数据"""
        
        # BrainGNN关键脑区结果
        self.brain_regions = {
            # 疼痛激活区域 (红色)
            'Cerebelum_Crus1_R': {
                'coords': [28, -77, -33], 'activation': 0.601,
                'network': 'Sensorimotor', 'hemisphere': 'R',
                'description': 'Primary sensorimotor integration'
            },
            'Cerebelum_Crus1_L': {
                'coords': [-28, -77, -33], 'activation': 0.438,
                'network': 'Sensorimotor', 'hemisphere': 'L',
                'description': 'Bilateral cerebellar coordination'
            },
            'Occipital_Mid_R': {
                'coords': [31, -87, 11], 'activation': 0.528,
                'network': 'Visual', 'hemisphere': 'R',
                'description': 'Visual-spatial pain processing'
            },
            'Occipital_Sup_R': {
                'coords': [20, -93, 15], 'activation': 0.528,
                'network': 'Visual', 'hemisphere': 'R',
                'description': 'Enhanced visual attention'
            },
            'Occipital_Mid_L': {
                'coords': [-31, -87, 11], 'activation': 0.385,
                'network': 'Visual', 'hemisphere': 'L',
                'description': 'Bilateral visual processing'
            },
            'ParaHippocampal_L': {
                'coords': [-24, -7, -21], 'activation': 0.120,
                'network': 'Limbic', 'hemisphere': 'L',
                'description': 'Pain memory encoding'
            },
            'Amygdala_R': {
                'coords': [25, -1, -20], 'activation': 0.080,
                'network': 'Limbic', 'hemisphere': 'R',
                'description': 'Emotional pain response'
            },
            
            # 疼痛抑制区域 (蓝色)
            'Frontal_Sup_L': {
                'coords': [-15, 26, 56], 'activation': -0.512,
                'network': 'Executive', 'hemisphere': 'L',
                'description': 'Top-down cognitive control'
            },
            'Frontal_Mid_L': {
                'coords': [-30, 47, 28], 'activation': -0.498,
                'network': 'Executive', 'hemisphere': 'L',
                'description': 'Executive function regulation'
            },
            'Precentral_L': {
                'coords': [-39, -6, 52], 'activation': -0.433,
                'network': 'Motor', 'hemisphere': 'L',
                'description': 'Motor cortex inhibition'
            },
            'Postcentral_L': {
                'coords': [-43, -25, 49], 'activation': -0.431,
                'network': 'Somatosensory', 'hemisphere': 'L',
                'description': 'Sensory cortex regulation'
            },
            'Rolandic_Oper_L': {
                'coords': [-50, 0, 9], 'activation': -0.401,
                'network': 'Sensorimotor', 'hemisphere': 'L',
                'description': 'Sensorimotor integration'
            },
            'Frontal_Sup_R': {
                'coords': [15, 26, 56], 'activation': -0.394,
                'network': 'Executive', 'hemisphere': 'R',
                'description': 'Bilateral cognitive control'
            },
            'Putamen_R': {
                'coords': [26, 6, 0], 'activation': -0.386,
                'network': 'Subcortical', 'hemisphere': 'R',
                'description': 'Motor regulation suppression'
            }
        }
    
    def create_brain_surface(self):
        """创建大脑表面网格"""
        
        # 创建大脑椭球表面
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 30)
        
        # 大脑椭球参数 (基于真实解剖尺寸)
        a, b, c = 75, 85, 65  # 左右、前后、上下半径
        
        x = a * np.outer(np.sin(v), np.cos(u))
        y = b * np.outer(np.sin(v), np.sin(u))
        z = c * np.outer(np.cos(v), np.ones(np.size(u)))
        
        # 大脑形状调整
        for i in range(len(v)):
            for j in range(len(u)):
                # 前额叶突出
                if y[i,j] > 40:
                    y[i,j] *= 1.1
                    z[i,j] *= 0.9
                
                # 颞叶下垂
                if abs(x[i,j]) > 50 and z[i,j] < 0:
                    z[i,j] -= 15
                
                # 枕叶后突
                if y[i,j] < -60:
                    y[i,j] *= 1.05
        
        return x, y, z
    
    def calculate_surface_activation(self, x, y, z):
        """计算表面激活值"""
        
        activation_surface = np.zeros_like(x)
        
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                point = [x[i,j], y[i,j], z[i,j]]
                
                # 找最近的脑区并计算激活
                min_distance = float('inf')
                activation = 0.0
                
                for region_name, region_data in self.brain_regions.items():
                    region_coords = region_data['coords']
                    distance = np.sqrt(sum((point[k] - region_coords[k])**2 for k in range(3)))
                    
                    if distance < min_distance:
                        min_distance = distance
                        # 距离衰减
                        decay = np.exp(-distance / 25.0)
                        activation = region_data['activation'] * decay
                
                activation_surface[i,j] = activation
        
        return activation_surface
    
    def create_interactive_3d_plot(self):
        """创建交互式3D图"""
        
        print("🎨 Creating interactive 3D brain visualization...")
        
        # 创建子图布局
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "scene", "colspan": 2}, None],
                   [{"type": "xy"}, {"type": "xy"}]],
            subplot_titles=('3D Brain Pain State Mapping', 
                          'Activation by Network', 'Activation by Hemisphere'),
            vertical_spacing=0.1
        )
        
        # 1. 创建大脑表面
        x, y, z = self.create_brain_surface()
        activation_surface = self.calculate_surface_activation(x, y, z)
        
        # 大脑表面mesh
        fig.add_trace(
            go.Surface(
                x=x, y=y, z=z,
                surfacecolor=activation_surface,
                colorscale='RdBu_r',  # 红-白-蓝
                cmin=-0.6, cmax=0.6,
                opacity=0.7,
                name='Brain Surface',
                colorbar=dict(
                    title="Pain Activation<br>(Pain - No Pain)",
                    titleside="right",
                    x=1.02
                )
            ),
            row=1, col=1
        )
        
        # 2. 添加脑区球体
        for region_name, region_data in self.brain_regions.items():
            coords = region_data['coords']
            activation = region_data['activation']
            network = region_data['network']
            hemisphere = region_data['hemisphere']
            description = region_data['description']
            
            # 颜色和大小
            color = 'red' if activation > 0 else 'blue'
            size = abs(activation) * 30 + 5
            
            fig.add_trace(
                go.Scatter3d(
                    x=[coords[0]], y=[coords[1]], z=[coords[2]],
                    mode='markers',
                    marker=dict(
                        size=size,
                        color=color,
                        opacity=0.8,
                        line=dict(width=2, color='white')
                    ),
                    name=region_name.replace('_', ' '),
                    text=f"<b>{region_name.replace('_', ' ')}</b><br>" +
                         f"Activation: {activation:+.3f}<br>" +
                         f"Network: {network}<br>" +
                         f"Hemisphere: {hemisphere}<br>" +
                         f"Function: {description}",
                    hovertemplate="%{text}<extra></extra>"
                ),
                row=1, col=1
            )
        
        # 3. 网络激活分析
        network_data = {}
        for region_name, region_data in self.brain_regions.items():
            network = region_data['network']
            activation = region_data['activation']
            
            if network not in network_data:
                network_data[network] = []
            network_data[network].append(activation)
        
        networks = list(network_data.keys())
        avg_activations = [np.mean(network_data[net]) for net in networks]
        colors = ['red' if x > 0 else 'blue' for x in avg_activations]
        
        fig.add_trace(
            go.Bar(
                x=networks,
                y=avg_activations,
                marker_color=colors,
                name='Network Activation',
                text=[f'{x:+.3f}' for x in avg_activations],
                textposition='outside'
            ),
            row=2, col=1
        )
        
        # 4. 半球激活分析
        left_activations = [data['activation'] for data in self.brain_regions.values() 
                           if data['hemisphere'] == 'L']
        right_activations = [data['activation'] for data in self.brain_regions.values() 
                            if data['hemisphere'] == 'R']
        
        fig.add_trace(
            go.Bar(
                x=['Left Hemisphere', 'Right Hemisphere'],
                y=[np.mean(left_activations), np.mean(right_activations)],
                marker_color=['lightblue', 'lightcoral'],
                name='Hemisphere Activation',
                text=[f'{np.mean(left_activations):+.3f}', 
                      f'{np.mean(right_activations):+.3f}'],
                textposition='outside'
            ),
            row=2, col=2
        )
        
        # 布局设置
        fig.update_scenes(
            xaxis_title="X (mm)",
            yaxis_title="Y (mm)", 
            zaxis_title="Z (mm)",
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1.0)
            )
        )
        
        fig.update_layout(
            title=dict(
                text="🧠 BrainGNN Pain State Classification: Interactive 3D Visualization<br>" +
                     "<sup>Binary Classification (Pain vs No-Pain) | Accuracy: 98.7% | 14 Key Brain Regions</sup>",
                x=0.5,
                font=dict(size=16)
            ),
            height=900,
            showlegend=False,
            font=dict(size=12)
        )
        
        # 更新子图标题
        fig.update_xaxes(title_text="Brain Networks", row=2, col=1)
        fig.update_yaxes(title_text="Avg Activation", row=2, col=1)
        fig.update_xaxes(title_text="Brain Hemisphere", row=2, col=2)
        fig.update_yaxes(title_text="Avg Activation", row=2, col=2)
        
        return fig
    
    def create_simple_3d_plot(self):
        """创建简化版3D图 (如果复杂版本有问题)"""
        
        print("🎨 Creating simple 3D brain plot...")
        
        fig = go.Figure()
        
        # 只显示脑区球体
        for region_name, region_data in self.brain_regions.items():
            coords = region_data['coords']
            activation = region_data['activation']
            
            color = 'red' if activation > 0 else 'blue'
            size = abs(activation) * 40 + 10
            
            fig.add_trace(
                go.Scatter3d(
                    x=[coords[0]], y=[coords[1]], z=[coords[2]],
                    mode='markers+text',
                    marker=dict(
                        size=size,
                        color=color,
                        opacity=0.8,
                        line=dict(width=2, color='white')
                    ),
                    text=region_name.split('_')[0],
                    textposition="middle center",
                    name=f"{region_name}: {activation:+.3f}",
                    hovertemplate=f"<b>{region_name}</b><br>" +
                                 f"Activation: {activation:+.3f}<br>" +
                                 f"Coordinates: {coords}<extra></extra>"
                )
            )
        
        # 添加大脑轮廓 (简化椭球)
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 15)
        
        a, b, c = 75, 85, 65
        x = a * np.outer(np.sin(v), np.cos(u))
        y = b * np.outer(np.sin(v), np.sin(u))
        z = c * np.outer(np.cos(v), np.ones(np.size(u)))
        
        fig.add_trace(
            go.Surface(
                x=x, y=y, z=z,
                opacity=0.2,
                showscale=False,
                colorscale=[[0, 'lightgray'], [1, 'lightgray']],
                name='Brain Outline'
            )
        )
        
        fig.update_layout(
            title="🧠 BrainGNN Pain Classification: 3D Brain Regions<br>" +
                  "<sup>Red: Pain Enhanced | Blue: Pain Suppressed</sup>",
            scene=dict(
                xaxis_title="X (mm)",
                yaxis_title="Y (mm)",
                zaxis_title="Z (mm)",
                camera=dict(eye=dict(x=1.5, y=-1.5, z=1.0))
            ),
            height=700,
            font=dict(size=12)
        )
        
        return fig
    
    def save_and_show(self, fig, filename="brain_3d_plotly.html"):
        """保存并显示图表"""
        
        # 保存为HTML文件
        fig.write_html(f"./figures/{filename}")
        print(f"✅ 3D visualization saved: ./figures/{filename}")
        
        # 自动在浏览器中打开
        fig.show()
        
        print("🌐 3D brain visualization opened in your web browser!")
        print("🎮 You can:")
        print("  • Rotate: Click and drag")
        print("  • Zoom: Mouse wheel")
        print("  • Pan: Shift + click and drag") 
        print("  • Hover: Mouse over regions for details")

def main():
    """主函数"""
    print("🚀 Starting Plotly 3D Brain Visualization...")
    print("📊 BrainGNN Results: 98.7% Accuracy | Pain vs No-Pain Classification")
    
    # 创建3D查看器
    viewer = Plotly3DBrainViewer()
    
    try:
        # 尝试创建完整版
        print("\n🎨 Creating comprehensive 3D visualization...")
        fig = viewer.create_interactive_3d_plot()
        viewer.save_and_show(fig, "brain_3d_comprehensive.html")
        
    except Exception as e:
        print(f"⚠️ Comprehensive version failed: {e}")
        print("🔄 Creating simplified version...")
        
        # 创建简化版
        fig = viewer.create_simple_3d_plot()
        viewer.save_and_show(fig, "brain_3d_simple.html")
    
    print("\n🎉 3D Brain visualization completed!")
    print("📂 Open in browser: ./figures/brain_3d_*.html")

if __name__ == "__main__":
    main()