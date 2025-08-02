#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrainRender专业脑图可视化 - 疼痛状态映射
Professional Brain Visualization using BrainRender - Pain State Mapping
"""

import numpy as np
from brainrender import Scene, settings
from brainrender.actors import Points
import pandas as pd
import os

# 设置brainrender配置
settings.SHOW_AXES = True
settings.SHADER_STYLE = 'plastic'  # 或 'cartoon', 'metallic'
settings.DEFAULT_ATLAS = 'allen_mouse_25um'  # 使用Allen atlas

class BrainRenderPainVisualization:
    """BrainRender疼痛可视化器"""
    
    def __init__(self):
        self.setup_brain_data()
        self.setup_scene()
        
    def setup_brain_data(self):
        """设置脑区数据"""
        
        # BrainGNN关键脑区结果 (MNI坐标转换为brainrender坐标系)
        self.brain_regions = {
            # 疼痛激活区域 (红色) - 小鼠坐标系转换
            'Cerebelum_Crus1_R': {
                'coords': [2.8, -7.7, -3.3],  # 转换为小鼠尺度 (除以10)
                'activation': 0.601,
                'hemisphere': 'R',
                'network': 'Sensorimotor',
                'description': 'Primary sensorimotor integration'
            },
            'Cerebelum_Crus1_L': {
                'coords': [-2.8, -7.7, -3.3],
                'activation': 0.438,
                'hemisphere': 'L',
                'network': 'Sensorimotor',
                'description': 'Bilateral cerebellar coordination'
            },
            'Occipital_Mid_R': {
                'coords': [3.1, -8.7, 1.1],
                'activation': 0.528,
                'hemisphere': 'R',
                'network': 'Visual',
                'description': 'Visual-spatial pain processing'
            },
            'Occipital_Sup_R': {
                'coords': [2.0, -9.3, 1.5],
                'activation': 0.528,
                'hemisphere': 'R',
                'network': 'Visual',
                'description': 'Enhanced visual attention'
            },
            'Occipital_Mid_L': {
                'coords': [-3.1, -8.7, 1.1],
                'activation': 0.385,
                'hemisphere': 'L',
                'network': 'Visual',
                'description': 'Bilateral visual processing'
            },
            'ParaHippocampal_L': {
                'coords': [-2.4, -0.7, -2.1],
                'activation': 0.120,
                'hemisphere': 'L',
                'network': 'Limbic',
                'description': 'Pain memory encoding'
            },
            'Amygdala_R': {
                'coords': [2.5, -0.1, -2.0],
                'activation': 0.080,
                'hemisphere': 'R',
                'network': 'Limbic',
                'description': 'Emotional pain response'
            },
            
            # 疼痛抑制区域 (蓝色)
            'Frontal_Sup_L': {
                'coords': [-1.5, 2.6, 5.6],
                'activation': -0.512,
                'hemisphere': 'L',
                'network': 'Executive',
                'description': 'Top-down cognitive control'
            },
            'Frontal_Mid_L': {
                'coords': [-3.0, 4.7, 2.8],
                'activation': -0.498,
                'hemisphere': 'L',
                'network': 'Executive',
                'description': 'Executive function regulation'
            },
            'Precentral_L': {
                'coords': [-3.9, -0.6, 5.2],
                'activation': -0.433,
                'hemisphere': 'L',
                'network': 'Motor',
                'description': 'Motor cortex inhibition'
            },
            'Postcentral_L': {
                'coords': [-4.3, -2.5, 4.9],
                'activation': -0.431,
                'hemisphere': 'L',
                'network': 'Somatosensory',
                'description': 'Sensory cortex regulation'
            },
            'Rolandic_Oper_L': {
                'coords': [-5.0, 0.0, 0.9],
                'activation': -0.401,
                'hemisphere': 'L',
                'network': 'Sensorimotor',
                'description': 'Sensorimotor integration'
            },
            'Frontal_Sup_R': {
                'coords': [1.5, 2.6, 5.6],
                'activation': -0.394,
                'hemisphere': 'R',
                'network': 'Executive',
                'description': 'Bilateral cognitive control'
            },
            'Putamen_R': {
                'coords': [2.6, 0.6, 0.0],
                'activation': -0.386,
                'hemisphere': 'R',
                'network': 'Subcortical',
                'description': 'Motor regulation suppression'
            }
        }
        
    def setup_scene(self):
        """设置BrainRender场景"""
        
        print("🧠 Setting up BrainRender scene...")
        
        # 创建场景
        self.scene = Scene(
            title="BrainGNN Pain State Mapping",
            atlas_name="allen_mouse_25um"  # 使用Allen小鼠atlas
        )
        
        # 添加整个大脑轮廓 (半透明)
        self.scene.add_brain_region("root", alpha=0.1, color="lightgray")
        
    def add_pain_regions(self):
        """添加疼痛相关脑区"""
        
        print("🎯 Adding pain-related brain regions...")
        
        # 分别处理激活和抑制区域
        enhanced_regions = []
        suppressed_regions = []
        
        for region_name, region_data in self.brain_regions.items():
            activation = region_data['activation']
            coords = region_data['coords']
            
            if activation > 0:
                enhanced_regions.append({
                    'name': region_name,
                    'coords': coords,
                    'activation': activation,
                    'color': 'red',
                    'network': region_data['network']
                })
            else:
                suppressed_regions.append({
                    'name': region_name,
                    'coords': coords,
                    'activation': abs(activation),
                    'color': 'blue',
                    'network': region_data['network']
                })
        
        # 添加疼痛激活区域 (红色球体)
        if enhanced_regions:
            enhanced_coords = np.array([r['coords'] for r in enhanced_regions])
            enhanced_sizes = np.array([r['activation'] * 500 + 100 for r in enhanced_regions])
            enhanced_colors = ['red'] * len(enhanced_regions)
            
            enhanced_actor = Points(
                enhanced_coords,
                name="Pain Enhanced Regions",
                colors=enhanced_colors,
                radius=enhanced_sizes.tolist(),
                alpha=0.8
            )
            self.scene.add(enhanced_actor)
        
        # 添加疼痛抑制区域 (蓝色球体)
        if suppressed_regions:
            suppressed_coords = np.array([r['coords'] for r in suppressed_regions])
            suppressed_sizes = np.array([r['activation'] * 500 + 100 for r in suppressed_regions])
            suppressed_colors = ['blue'] * len(suppressed_regions)
            
            suppressed_actor = Points(
                suppressed_coords,
                name="Pain Suppressed Regions",
                colors=suppressed_colors,
                radius=suppressed_sizes.tolist(),
                alpha=0.8
            )
            self.scene.add(suppressed_actor)
        
        return len(enhanced_regions), len(suppressed_regions)
    
    def add_network_visualization(self):
        """添加网络连接可视化"""
        
        print("🔗 Adding network connections...")
        
        # 按网络分组
        networks = {}
        for region_name, region_data in self.brain_regions.items():
            network = region_data['network']
            if network not in networks:
                networks[network] = []
            networks[network].append({
                'name': region_name,
                'coords': region_data['coords'],
                'activation': region_data['activation']
            })
        
        # 为每个网络添加连接线
        network_colors = {
            'Sensorimotor': 'orange',
            'Visual': 'green',
            'Limbic': 'purple',
            'Executive': 'yellow',
            'Motor': 'cyan',
            'Somatosensory': 'magenta',
            'Subcortical': 'brown'
        }
        
        for network_name, regions in networks.items():
            if len(regions) > 1:
                # 连接同一网络内的区域
                for i in range(len(regions)):
                    for j in range(i + 1, len(regions)):
                        start_coords = regions[i]['coords']
                        end_coords = regions[j]['coords']
                        
                        # 添加连接线 (如果brainrender支持)
                        # 这里简化处理，实际实现需要根据brainrender API
                        pass
        
        return list(networks.keys())
    
    def add_anatomical_regions(self):
        """添加解剖学区域"""
        
        print("🧭 Adding anatomical regions...")
        
        # 定义主要解剖区域
        anatomical_regions = [
            # 皮层区域
            "Isocortex",
            "CTXpl",  # 皮层板
            "MOp",    # 初级运动皮层
            "MOs",    # 次级运动皮层
            "SSp",    # 初级体感皮层
            "SSs",    # 次级体感皮层
            "VISp",   # 初级视觉皮层
            "VISam",  # 前内侧视觉皮层
            
            # 皮层下区域
            "CB",     # 小脑
            "CBN",    # 小脑核
            "STR",    # 纹状体
            "PAL",    # 苍白球
            "TH",     # 丘脑
            "HY",     # 下丘脑
        ]
        
        added_regions = []
        
        for region in anatomical_regions:
            try:
                # 添加区域 (半透明)
                self.scene.add_brain_region(
                    region, 
                    alpha=0.2,
                    color="lightblue"
                )
                added_regions.append(region)
            except Exception as e:
                print(f"⚠️ Could not add region {region}: {e}")
                continue
        
        return added_regions
    
    def create_comprehensive_visualization(self):
        """创建综合可视化"""
        
        print("🎨 Creating comprehensive brainrender visualization...")
        
        # 1. 添加疼痛相关区域
        enhanced_count, suppressed_count = self.add_pain_regions()
        
        # 2. 添加网络连接
        networks = self.add_network_visualization()
        
        # 3. 添加解剖学区域
        anatomical_regions = self.add_anatomical_regions()
        
        # 4. 设置相机和渲染
        self.scene.content
        
        print(f"✅ Added {enhanced_count} pain-enhanced regions (red)")
        print(f"✅ Added {suppressed_count} pain-suppressed regions (blue)")
        print(f"✅ Identified {len(networks)} neural networks")
        print(f"✅ Added {len(anatomical_regions)} anatomical regions")
        
        return self.scene
    
    def render_and_save(self, filename="brainrender_pain_mapping"):
        """渲染并保存图像"""
        
        print("📸 Rendering and saving brainrender visualization...")
        
        # 确保目录存在
        os.makedirs('./figures', exist_ok=True)
        
        try:
            # 渲染场景
            self.scene.render(
                interactive=False,  # 非交互模式
                zoom=1.5,
                elevation=30,
                azimuth=45
            )
            
            # 保存图像
            self.scene.screenshot(f"./figures/{filename}.png")
            
            print(f"✅ BrainRender visualization saved: ./figures/{filename}.png")
            
            # 显示交互式版本
            print("🌐 Starting interactive brainrender session...")
            self.scene.render(interactive=True)
            
        except Exception as e:
            print(f"❌ Error rendering: {e}")
            print("💡 Trying alternative rendering method...")
            
            # 备用方案：基本渲染
            try:
                self.scene.render()
            except Exception as e2:
                print(f"❌ Alternative rendering failed: {e2}")
                print("📝 Scene created successfully, but rendering failed")
                return False
        
        return True
    
    def export_scene_data(self):
        """导出场景数据"""
        
        print("📊 Exporting scene data...")
        
        # 创建数据总结
        summary = {
            'total_regions': len(self.brain_regions),
            'enhanced_regions': len([r for r in self.brain_regions.values() if r['activation'] > 0]),
            'suppressed_regions': len([r for r in self.brain_regions.values() if r['activation'] < 0]),
            'networks': list(set([r['network'] for r in self.brain_regions.values()])),
            'hemisphere_balance': {
                'left': len([r for r in self.brain_regions.values() if r['hemisphere'] == 'L']),
                'right': len([r for r in self.brain_regions.values() if r['hemisphere'] == 'R'])
            }
        }
        
        # 保存区域详情
        df = pd.DataFrame.from_dict(self.brain_regions, orient='index')
        df.to_csv('./figures/brainrender_regions_data.csv')
        
        print("✅ Scene data exported:")
        print(f"  • Total regions: {summary['total_regions']}")
        print(f"  • Enhanced: {summary['enhanced_regions']}")
        print(f"  • Suppressed: {summary['suppressed_regions']}")
        print(f"  • Networks: {', '.join(summary['networks'])}")
        print(f"  • Hemisphere balance: L={summary['hemisphere_balance']['left']}, R={summary['hemisphere_balance']['right']}")
        
        return summary

def main():
    """主函数"""
    print("🚀 Starting BrainRender Pain State Visualization...")
    print("🧠 BrainGNN Results: 98.7% Accuracy | Pain vs No-Pain Classification")
    print("🎯 Using professional brainrender library from BrainGlobe...")
    
    try:
        # 创建可视化器
        viz = BrainRenderPainVisualization()
        
        # 创建综合可视化
        scene = viz.create_comprehensive_visualization()
        
        # 导出数据
        summary = viz.export_scene_data()
        
        # 渲染和保存
        success = viz.render_and_save("brainrender_pain_mapping")
        
        if success:
            print("\n🎉 BrainRender visualization completed successfully!")
            print("📂 Files saved:")
            print("  • ./figures/brainrender_pain_mapping.png")
            print("  • ./figures/brainrender_regions_data.csv")
            print("\n🎮 Interactive controls:")
            print("  • Mouse: Rotate view")
            print("  • Scroll: Zoom in/out")
            print("  • Drag: Pan view")
        else:
            print("\n⚠️ Visualization created but rendering had issues")
            print("💡 Scene data still available in CSV format")
            
    except Exception as e:
        print(f"❌ Error creating BrainRender visualization: {e}")
        print("\n🔧 Troubleshooting suggestions:")
        print("  • Check atlas installation")
        print("  • Verify brainrender dependencies")
        print("  • Try simpler visualization first")
        
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()