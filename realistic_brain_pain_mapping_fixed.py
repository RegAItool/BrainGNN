#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realistic Brain Shape Pain Mapping (Fixed Version)
BrainGNN 2-Class Pain State Visualization: Pain vs No Pain
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

class RealisticBrainPainMapper:
    """真实脑子形状疼痛映射器"""
    
    def __init__(self):
        self.setup_brain_anatomy()
        self.setup_pain_regions()
        self.setup_colors()
    
    def setup_brain_anatomy(self):
        """设置大脑解剖结构"""
        
        # 真实大脑轮廓坐标 (简化的解剖形状)
        self.brain_outline = {
            # 主要大脑皮层轮廓
            'cortex': np.array([
                [-75, 65], [-70, 75], [-60, 85], [-45, 90], [-25, 92], [0, 93], 
                [25, 92], [45, 90], [60, 85], [70, 75], [75, 65], [78, 50],
                [80, 30], [78, 10], [75, -10], [70, -30], [65, -45], [55, -60],
                [45, -70], [30, -75], [15, -78], [0, -80], [-15, -78], [-30, -75],
                [-45, -70], [-55, -60], [-65, -45], [-70, -30], [-75, -10], 
                [-78, 10], [-80, 30], [-78, 50], [-75, 65]
            ]),
            
            # 小脑轮廓
            'cerebellum': np.array([
                [-55, -75], [-45, -85], [-35, -90], [-20, -92], [0, -93],
                [20, -92], [35, -90], [45, -85], [55, -75], [50, -65],
                [40, -55], [25, -50], [0, -48], [-25, -50], [-40, -55],
                [-50, -65], [-55, -75]
            ]),
            
            # 脑干
            'brainstem': np.array([
                [-8, -45], [-6, -55], [-4, -65], [-2, -70], [0, -72],
                [2, -70], [4, -65], [6, -55], [8, -45], [6, -35],
                [4, -30], [2, -28], [0, -27], [-2, -28], [-4, -30],
                [-6, -35], [-8, -45]
            ])
        }
        
        # 主要脑叶分界线
        self.lobe_boundaries = {
            'frontal_parietal': [[-40, 25], [40, 25], [45, 20], [40, 15], [-40, 15], [-45, 20]],
            'parietal_occipital': [[-35, -20], [35, -20], [40, -25], [35, -30], [-35, -30], [-40, -25]],
            'temporal_boundary': [[-70, 10], [-50, -40], [-30, -45], [-25, -35], [-35, 0], [-55, 15]]
        }
    
    def setup_pain_regions(self):
        """设置疼痛相关脑区"""
        
        # 基于BrainGNN分析结果的关键脑区
        self.pain_regions = {
            # === 疼痛激活增强区域 (Pain State Activation) ===
            'enhanced_regions': {
                'Cerebelum_Crus1_R': {
                    'pos': (45, -75), 'size': 12, 'activation': 0.601,
                    'anatomical_area': 'cerebellum', 'hemisphere': 'right',
                    'description': 'Primary sensorimotor integration during pain'
                },
                'Cerebelum_Crus1_L': {
                    'pos': (-45, -75), 'size': 10, 'activation': 0.438,
                    'anatomical_area': 'cerebellum', 'hemisphere': 'left',
                    'description': 'Bilateral cerebellar coordination'
                },
                'Occipital_Mid_R': {
                    'pos': (35, -85), 'size': 11, 'activation': 0.528,
                    'anatomical_area': 'occipital', 'hemisphere': 'right',
                    'description': 'Visual-spatial pain localization'
                },
                'Occipital_Sup_R': {
                    'pos': (25, -95), 'size': 10, 'activation': 0.528,
                    'anatomical_area': 'occipital', 'hemisphere': 'right',
                    'description': 'Enhanced visual attention to pain'
                },
                'Occipital_Mid_L': {
                    'pos': (-35, -85), 'size': 9, 'activation': 0.385,
                    'anatomical_area': 'occipital', 'hemisphere': 'left',
                    'description': 'Bilateral visual processing'
                },
                'ParaHippocampal_L': {
                    'pos': (-30, -35), 'size': 8, 'activation': 0.120,
                    'anatomical_area': 'temporal', 'hemisphere': 'left',
                    'description': 'Pain memory encoding'
                },
                'Amygdala_R': {
                    'pos': (25, -10), 'size': 7, 'activation': 0.080,
                    'anatomical_area': 'temporal', 'hemisphere': 'right',
                    'description': 'Emotional response to pain'
                }
            },
            
            # === 疼痛抑制区域 (Pain State Suppression) ===
            'suppressed_regions': {
                'Frontal_Sup_L': {
                    'pos': (-35, 70), 'size': 11, 'activation': -0.512,
                    'anatomical_area': 'frontal', 'hemisphere': 'left',
                    'description': 'Top-down cognitive control'
                },
                'Frontal_Mid_L': {
                    'pos': (-50, 45), 'size': 10, 'activation': -0.498,
                    'anatomical_area': 'frontal', 'hemisphere': 'left',
                    'description': 'Executive function regulation'
                },
                'Precentral_L': {
                    'pos': (-40, 25), 'size': 10, 'activation': -0.433,
                    'anatomical_area': 'frontal', 'hemisphere': 'left',
                    'description': 'Motor cortex inhibition'
                },
                'Postcentral_L': {
                    'pos': (-40, -20), 'size': 9, 'activation': -0.431,
                    'anatomical_area': 'parietal', 'hemisphere': 'left',
                    'description': 'Sensory cortex regulation'
                },
                'Rolandic_Oper_L': {
                    'pos': (-55, 5), 'size': 9, 'activation': -0.401,
                    'anatomical_area': 'frontal', 'hemisphere': 'left',
                    'description': 'Sensorimotor integration'
                },
                'Frontal_Sup_R': {
                    'pos': (35, 70), 'size': 8, 'activation': -0.394,
                    'anatomical_area': 'frontal', 'hemisphere': 'right',
                    'description': 'Bilateral cognitive control'
                },
                'Putamen_R': {
                    'pos': (25, 5), 'size': 7, 'activation': -0.386,
                    'anatomical_area': 'subcortical', 'hemisphere': 'right',
                    'description': 'Motor regulation suppression'
                }
            }
        }
        
        # 疼痛状态定义
        self.pain_states = {
            'pain_state': {
                'name': 'Pain State (疼痛状态)',
                'description': 'Brain regions activated during pain perception',
                'regions': self.pain_regions['enhanced_regions'],
                'color': '#FF3333',
                'mechanism': 'Enhanced activation for pain processing'
            },
            'no_pain_state': {
                'name': 'No Pain State (非疼痛状态)', 
                'description': 'Brain regions suppressed during pain (active in no-pain)',
                'regions': self.pain_regions['suppressed_regions'],
                'color': '#3333FF',
                'mechanism': 'Suppressed during pain / Active during no-pain'
            }
        }
    
    def setup_colors(self):
        """设置颜色方案"""
        
        # 疼痛状态颜色映射
        self.pain_cmap = LinearSegmentedColormap.from_list(
            'pain_states',
            ['#0066CC', '#FFFFFF', '#CC0000'],  # Blue-White-Red
            N=256
        )
        
        # 解剖区域颜色
        self.anatomy_colors = {
            'frontal': '#FFE6E6',
            'parietal': '#E6F2FF', 
            'temporal': '#E6FFE6',
            'occipital': '#FFFFE6',
            'cerebellum': '#F0E6FF',
            'subcortical': '#FFE6F2'
        }
    
    def create_realistic_brain_pain_mapping(self):
        """创建真实脑形状疼痛映射图"""
        
        # 创建大画布
        fig = plt.figure(figsize=(20, 16))
        
        # 主要大脑图 - 疼痛状态对比
        ax_main = plt.subplot2grid((3, 4), (0, 0), rowspan=2, colspan=2)
        
        # 疼痛状态脑图
        ax_pain = plt.subplot2grid((3, 4), (0, 2), rowspan=1, colspan=1)
        
        # 非疼痛状态脑图
        ax_no_pain = plt.subplot2grid((3, 4), (1, 2), rowspan=1, colspan=1)
        
        # 激活强度对比
        ax_comparison = plt.subplot2grid((3, 4), (0, 3), rowspan=2, colspan=1)
        
        # 疼痛机制说明
        ax_mechanism = plt.subplot2grid((3, 4), (2, 0), rowspan=1, colspan=4)
        
        # === 绘制主要大脑图 ===
        self.draw_realistic_brain_comparison(ax_main)
        
        # === 绘制疼痛状态脑图 ===
        self.draw_single_state_brain(ax_pain, 'pain_state')
        
        # === 绘制非疼痛状态脑图 ===
        self.draw_single_state_brain(ax_no_pain, 'no_pain_state')
        
        # === 绘制激活对比 ===
        self.draw_activation_comparison(ax_comparison)
        
        # === 绘制机制说明 ===
        self.draw_pain_mechanism_explanation(ax_mechanism)
        
        # 设置总标题
        title_text = ('🧠 BrainGNN Realistic Brain Pain State Mapping\n'
                     'Binary Classification: Pain vs No-Pain States (98.7% Accuracy)\n'
                     f'Analysis of {len(self.pain_regions["enhanced_regions"]) + len(self.pain_regions["suppressed_regions"])} Key Brain Regions')
        
        fig.suptitle(title_text, fontsize=18, fontweight='bold', y=0.96)
        
        plt.tight_layout()
        
        # 保存图片
        plt.savefig('./figures/realistic_brain_pain_mapping.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.savefig('./figures/realistic_brain_pain_mapping.pdf', 
                   bbox_inches='tight', facecolor='white')
        
        print("✅ Realistic brain pain mapping saved:")
        print("  • ./figures/realistic_brain_pain_mapping.png")
        print("  • ./figures/realistic_brain_pain_mapping.pdf")
        
        return fig
    
    def draw_realistic_brain_comparison(self, ax):
        """绘制真实大脑形状对比图"""
        
        # 绘制大脑解剖轮廓
        self.draw_brain_anatomy(ax)
        
        # 绘制疼痛激活区域 (红色)
        for region_name, region_info in self.pain_regions['enhanced_regions'].items():
            pos = region_info['pos']
            size = region_info['size']
            activation = region_info['activation']
            
            # 激活强度决定颜色深度
            color_intensity = 0.4 + 0.6 * abs(activation)
            color = plt.cm.Reds(color_intensity)
            
            # 绘制激活区域
            circle = Circle(pos, size, color=color, alpha=0.9, 
                          edgecolor='darkred', linewidth=2)
            ax.add_patch(circle)
            
            # 添加激活数值
            ax.text(pos[0], pos[1], f'+{activation:.2f}', 
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   color='white')
            
            # 添加区域标签
            label = region_name.split('_')[0]
            ax.annotate(label, pos, xytext=(0, size + 6), 
                       textcoords='offset points',
                       ha='center', va='bottom', fontsize=7, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='red', alpha=0.7, edgecolor='white'))
        
        # 绘制疼痛抑制区域 (蓝色)
        for region_name, region_info in self.pain_regions['suppressed_regions'].items():
            pos = region_info['pos']
            size = region_info['size']
            activation = region_info['activation']
            
            # 抑制强度决定颜色深度
            color_intensity = 0.4 + 0.6 * abs(activation)
            color = plt.cm.Blues(color_intensity)
            
            # 绘制抑制区域
            circle = Circle(pos, size, color=color, alpha=0.9, 
                          edgecolor='darkblue', linewidth=2)
            ax.add_patch(circle)
            
            # 添加抑制数值
            ax.text(pos[0], pos[1], f'{activation:.2f}', 
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   color='white')
            
            # 添加区域标签
            label = region_name.split('_')[0]
            ax.annotate(label, pos, xytext=(0, size + 6), 
                       textcoords='offset points',
                       ha='center', va='bottom', fontsize=7, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='blue', alpha=0.7, edgecolor='white'))
        
        ax.set_xlim(-100, 100)
        ax.set_ylim(-110, 110)
        ax.set_aspect('equal')
        ax.set_title('Pain vs No-Pain Brain State Comparison\n(Red=Pain Active, Blue=No-Pain Active)', 
                    fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # 添加方向标识
        ax.text(-90, 95, 'L', fontsize=16, fontweight='bold', 
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightblue', alpha=0.8))
        ax.text(85, 95, 'R', fontsize=16, fontweight='bold',
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightcoral', alpha=0.8))
        
        # 添加图例
        pain_patch = mpatches.Patch(color='#FF3333', label='Pain State (Enhanced Activation)')
        no_pain_patch = mpatches.Patch(color='#3333FF', label='No-Pain State (Active when no pain)')
        ax.legend(handles=[pain_patch, no_pain_patch], loc='upper right', fontsize=10)
    
    def draw_brain_anatomy(self, ax):
        """绘制大脑解剖结构"""
        
        # 绘制主要大脑皮层
        cortex_polygon = Polygon(self.brain_outline['cortex'], 
                               fill=True, facecolor='lightgray', 
                               edgecolor='black', linewidth=2, alpha=0.3)
        ax.add_patch(cortex_polygon)
        
        # 绘制小脑
        cerebellum_polygon = Polygon(self.brain_outline['cerebellum'], 
                                   fill=True, facecolor='lightsteelblue', 
                                   edgecolor='black', linewidth=1.5, alpha=0.4)
        ax.add_patch(cerebellum_polygon)
        
        # 绘制脑干
        brainstem_polygon = Polygon(self.brain_outline['brainstem'], 
                                  fill=True, facecolor='lightyellow', 
                                  edgecolor='black', linewidth=1.5, alpha=0.5)
        ax.add_patch(brainstem_polygon)
        
        # 添加解剖标签
        ax.text(0, 50, 'Cerebral Cortex', ha='center', va='center', 
               fontsize=12, fontweight='bold', alpha=0.6)
        ax.text(0, -75, 'Cerebellum', ha='center', va='center', 
               fontsize=10, fontweight='bold', alpha=0.7)
        ax.text(0, -45, 'Brainstem', ha='center', va='center', 
               fontsize=8, fontweight='bold', alpha=0.7)
    
    def draw_single_state_brain(self, ax, state_key):
        """绘制单一疼痛状态的脑图"""
        
        state_info = self.pain_states[state_key]
        
        # 简化的大脑轮廓
        brain_circle = Circle((0, 0), 45, fill=True, facecolor='lightgray', 
                            edgecolor='black', linewidth=2, alpha=0.3)
        ax.add_patch(brain_circle)
        
        # 小脑
        cerebellum_circle = Circle((0, -35), 25, fill=True, facecolor='lightsteelblue', 
                                 edgecolor='black', linewidth=1, alpha=0.4)
        ax.add_patch(cerebellum_circle)
        
        # 绘制该状态的活跃区域
        for region_name, region_info in state_info['regions'].items():
            # 调整位置以适应小图
            pos = (region_info['pos'][0] * 0.5, region_info['pos'][1] * 0.5)
            size = region_info['size'] * 0.6
            activation = region_info['activation']
            
            # 根据状态选择颜色
            if state_key == 'pain_state':
                color_intensity = 0.5 + 0.5 * abs(activation)
                color = plt.cm.Reds(color_intensity)
            else:
                color_intensity = 0.5 + 0.5 * abs(activation)
                color = plt.cm.Blues(color_intensity)
            
            # 绘制区域
            circle = Circle(pos, size, color=color, alpha=0.8, 
                          edgecolor='white', linewidth=1)
            ax.add_patch(circle)
            
            # 添加数值（只显示前几个重要的）
            if abs(activation) > 0.4:
                ax.text(pos[0], pos[1], f'{activation:+.1f}', 
                       ha='center', va='center', fontsize=6, fontweight='bold',
                       color='white')
        
        ax.set_xlim(-60, 60)
        ax.set_ylim(-70, 60)
        ax.set_aspect('equal')
        ax.set_title(state_info['name'], fontsize=11, fontweight='bold', color=state_info['color'])
        ax.axis('off')
    
    def draw_activation_comparison(self, ax):
        """绘制激活强度对比"""
        
        # 准备数据
        regions = []
        activations = []
        colors = []
        
        # 疼痛激活区域
        for region_name, region_info in self.pain_regions['enhanced_regions'].items():
            regions.append(region_name.replace('_', ' ')[:15])
            activations.append(region_info['activation'])
            colors.append('#FF3333')
        
        # 疼痛抑制区域
        for region_name, region_info in self.pain_regions['suppressed_regions'].items():
            regions.append(region_name.replace('_', ' ')[:15])
            activations.append(region_info['activation'])
            colors.append('#3333FF')
        
        # 按激活强度排序
        sorted_data = sorted(zip(regions, activations, colors), 
                           key=lambda x: abs(x[1]), reverse=True)
        
        regions_sorted = [x[0] for x in sorted_data]
        activations_sorted = [x[1] for x in sorted_data]
        colors_sorted = [x[2] for x in sorted_data]
        
        # 创建水平柱状图
        y_pos = np.arange(len(regions_sorted))
        bars = ax.barh(y_pos, activations_sorted, color=colors_sorted, alpha=0.8, 
                      edgecolor='black', linewidth=1)
        
        # 添加数值标签
        for i, (bar, activation) in enumerate(zip(bars, activations_sorted)):
            width = bar.get_width()
            ax.text(width + (0.02 if width > 0 else -0.02), 
                   bar.get_y() + bar.get_height()/2, 
                   f'{activation:+.3f}', 
                   ha='left' if width > 0 else 'right', 
                   va='center', fontsize=8, fontweight='bold')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(regions_sorted, fontsize=8)
        ax.set_xlabel('Activation Difference\n(Pain - No Pain)', fontsize=10, fontweight='bold')
        ax.set_title('Brain Region Activation\nDuring Pain States', fontsize=11, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.7, linewidth=2)
        ax.grid(axis='x', alpha=0.3)
        
        # 添加颜色说明
        ax.text(0.02, 0.98, 'Red: Active in Pain\nBlue: Active in No-Pain', 
               transform=ax.transAxes, fontsize=8, 
               verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    def draw_pain_mechanism_explanation(self, ax):
        """绘制疼痛机制说明"""
        
        # 计算统计数据
        enhanced_count = len(self.pain_regions['enhanced_regions'])
        suppressed_count = len(self.pain_regions['suppressed_regions'])
        total_regions = enhanced_count + suppressed_count
        
        enhanced_avg = np.mean([r['activation'] for r in self.pain_regions['enhanced_regions'].values()])
        suppressed_avg = np.mean([abs(r['activation']) for r in self.pain_regions['suppressed_regions'].values()])
        
        # 创建说明文本
        explanation_text = f"""
🧠 BrainGNN Pain State Classification Results (Binary: Pain vs No-Pain)

📊 MODEL PERFORMANCE:
   • Accuracy: 98.7% (Target: 80%+) ✓
   • F1-Score: 98.1%
   • Classification: Binary (2 states)
   • Total Key Regions: {total_regions}

🔴 PAIN STATE (疼痛状态) - {enhanced_count} regions:
   • Enhanced activation during pain perception
   • Average activation: +{enhanced_avg:.3f}
   • Key mechanisms: Sensorimotor integration (Cerebellum), Visual-spatial attention (Occipital), Emotional processing (Limbic)
   • Primary networks: Cerebellar, Visual, Limbic systems

🔵 NO-PAIN STATE (非疼痛状态) - {suppressed_count} regions:
   • Suppressed during pain / Active during no-pain conditions  
   • Average suppression: -{suppressed_avg:.3f}
   • Key mechanisms: Cognitive control (Frontal), Sensorimotor regulation (Motor/Sensory cortex)
   • Primary networks: Frontal executive control, Sensorimotor regulation

🎯 CLINICAL IMPLICATIONS:
   • Binary pain classification reveals distinct brain state patterns
   • Pain state shows enhanced sensory processing and emotional response
   • No-pain state shows active cognitive control and motor regulation
   • Different brain networks are dominant in each pain state
   • Results provide neural targets for pain management interventions
        """
        
        ax.text(0.02, 0.98, explanation_text.strip(), transform=ax.transAxes, 
               fontsize=10, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9, edgecolor='black'))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

def main():
    """主函数"""
    print("🎨 Creating realistic brain pain state mapping...")
    print("🧠 BrainGNN Binary Classification: Pain vs No-Pain (98.7% Accuracy)")
    
    # 创建真实脑形状映射器
    mapper = RealisticBrainPainMapper()
    
    # 生成真实脑图
    fig = mapper.create_realistic_brain_pain_mapping()
    
    print("\n✨ Realistic brain pain mapping completed!")
    print("📊 Analysis Summary:")
    print(f"  • Pain State Regions: {len(mapper.pain_regions['enhanced_regions'])} (Enhanced activation)")
    print(f"  • No-Pain State Regions: {len(mapper.pain_regions['suppressed_regions'])} (Active when no pain)")
    print(f"  • Total Key Regions: {len(mapper.pain_regions['enhanced_regions']) + len(mapper.pain_regions['suppressed_regions'])}")
    print("  • Classification: Binary (Pain vs No-Pain)")
    print("  • Model Accuracy: 98.7%")

if __name__ == "__main__":
    main()