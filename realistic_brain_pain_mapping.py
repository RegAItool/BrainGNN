#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realistic Brain Shape Pain Mapping
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
    
    def create_realistic_brain_pain_map(self):
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
        fig.suptitle('🧠 BrainGNN Realistic Brain Pain State Mapping\\n'\n                    'Binary Classification: Pain vs No-Pain States (98.7% Accuracy)\\n'\n                    f'Analysis of {len(self.pain_regions[\"enhanced_regions\"]) + len(self.pain_regions[\"suppressed_regions\"])} Key Brain Regions', \n                    fontsize=18, fontweight='bold', y=0.96)\n        \n        plt.tight_layout()\n        \n        # 保存图片\n        plt.savefig('./figures/realistic_brain_pain_mapping.png', \n                   dpi=300, bbox_inches='tight', facecolor='white')\n        plt.savefig('./figures/realistic_brain_pain_mapping.pdf', \n                   bbox_inches='tight', facecolor='white')\n        \n        print(\"✅ Realistic brain pain mapping saved:\")\n        print(\"  • ./figures/realistic_brain_pain_mapping.png\")\n        print(\"  • ./figures/realistic_brain_pain_mapping.pdf\")\n        \n        return fig\n    \n    def draw_realistic_brain_comparison(self, ax):\n        \"\"\"绘制真实大脑形状对比图\"\"\"\n        \n        # 绘制大脑解剖轮廓\n        self.draw_brain_anatomy(ax)\n        \n        # 绘制疼痛激活区域 (红色)\n        for region_name, region_info in self.pain_regions['enhanced_regions'].items():\n            pos = region_info['pos']\n            size = region_info['size']\n            activation = region_info['activation']\n            \n            # 激活强度决定颜色深度\n            color_intensity = 0.4 + 0.6 * abs(activation)\n            color = plt.cm.Reds(color_intensity)\n            \n            # 绘制激活区域\n            circle = Circle(pos, size, color=color, alpha=0.9, \n                          edgecolor='darkred', linewidth=2)\n            ax.add_patch(circle)\n            \n            # 添加激活数值\n            ax.text(pos[0], pos[1], f'+{activation:.2f}', \n                   ha='center', va='center', fontsize=8, fontweight='bold',\n                   color='white')\n            \n            # 添加区域标签\n            label = region_name.split('_')[0]\n            ax.annotate(label, pos, xytext=(0, size + 6), \n                       textcoords='offset points',\n                       ha='center', va='bottom', fontsize=7, fontweight='bold',\n                       bbox=dict(boxstyle=\"round,pad=0.2\", facecolor='red', alpha=0.7, edgecolor='white'))\n        \n        # 绘制疼痛抑制区域 (蓝色)\n        for region_name, region_info in self.pain_regions['suppressed_regions'].items():\n            pos = region_info['pos']\n            size = region_info['size']\n            activation = region_info['activation']\n            \n            # 抑制强度决定颜色深度\n            color_intensity = 0.4 + 0.6 * abs(activation)\n            color = plt.cm.Blues(color_intensity)\n            \n            # 绘制抑制区域\n            circle = Circle(pos, size, color=color, alpha=0.9, \n                          edgecolor='darkblue', linewidth=2)\n            ax.add_patch(circle)\n            \n            # 添加抑制数值\n            ax.text(pos[0], pos[1], f'{activation:.2f}', \n                   ha='center', va='center', fontsize=8, fontweight='bold',\n                   color='white')\n            \n            # 添加区域标签\n            label = region_name.split('_')[0]\n            ax.annotate(label, pos, xytext=(0, size + 6), \n                       textcoords='offset points',\n                       ha='center', va='bottom', fontsize=7, fontweight='bold',\n                       bbox=dict(boxstyle=\"round,pad=0.2\", facecolor='blue', alpha=0.7, edgecolor='white'))\n        \n        ax.set_xlim(-100, 100)\n        ax.set_ylim(-110, 110)\n        ax.set_aspect('equal')\n        ax.set_title('Pain vs No-Pain Brain State Comparison\\n(Red=Pain Active, Blue=No-Pain Active)', \n                    fontsize=12, fontweight='bold')\n        ax.axis('off')\n        \n        # 添加方向标识\n        ax.text(-90, 95, 'L', fontsize=16, fontweight='bold', \n               bbox=dict(boxstyle=\"circle,pad=0.3\", facecolor='lightblue', alpha=0.8))\n        ax.text(85, 95, 'R', fontsize=16, fontweight='bold',\n               bbox=dict(boxstyle=\"circle,pad=0.3\", facecolor='lightcoral', alpha=0.8))\n        \n        # 添加图例\n        pain_patch = mpatches.Patch(color='#FF3333', label='Pain State (Enhanced Activation)')\n        no_pain_patch = mpatches.Patch(color='#3333FF', label='No-Pain State (Active when no pain)')\n        ax.legend(handles=[pain_patch, no_pain_patch], loc='upper right', fontsize=10)\n    \n    def draw_brain_anatomy(self, ax):\n        \"\"\"绘制大脑解剖结构\"\"\"\n        \n        # 绘制主要大脑皮层\n        cortex_polygon = Polygon(self.brain_outline['cortex'], \n                               fill=True, facecolor='lightgray', \n                               edgecolor='black', linewidth=2, alpha=0.3)\n        ax.add_patch(cortex_polygon)\n        \n        # 绘制小脑\n        cerebellum_polygon = Polygon(self.brain_outline['cerebellum'], \n                                   fill=True, facecolor='lightsteelblue', \n                                   edgecolor='black', linewidth=1.5, alpha=0.4)\n        ax.add_patch(cerebellum_polygon)\n        \n        # 绘制脑干\n        brainstem_polygon = Polygon(self.brain_outline['brainstem'], \n                                  fill=True, facecolor='lightyellow', \n                                  edgecolor='black', linewidth=1.5, alpha=0.5)\n        ax.add_patch(brainstem_polygon)\n        \n        # 添加解剖标签\n        ax.text(0, 50, 'Cerebral Cortex', ha='center', va='center', \n               fontsize=12, fontweight='bold', alpha=0.6)\n        ax.text(0, -75, 'Cerebellum', ha='center', va='center', \n               fontsize=10, fontweight='bold', alpha=0.7)\n        ax.text(0, -45, 'Brainstem', ha='center', va='center', \n               fontsize=8, fontweight='bold', alpha=0.7)\n    \n    def draw_single_state_brain(self, ax, state_key):\n        \"\"\"绘制单一疼痛状态的脑图\"\"\"\n        \n        state_info = self.pain_states[state_key]\n        \n        # 简化的大脑轮廓\n        brain_circle = Circle((0, 0), 45, fill=True, facecolor='lightgray', \n                            edgecolor='black', linewidth=2, alpha=0.3)\n        ax.add_patch(brain_circle)\n        \n        # 小脑\n        cerebellum_circle = Circle((0, -35), 25, fill=True, facecolor='lightsteelblue', \n                                 edgecolor='black', linewidth=1, alpha=0.4)\n        ax.add_patch(cerebellum_circle)\n        \n        # 绘制该状态的活跃区域\n        for region_name, region_info in state_info['regions'].items():\n            # 调整位置以适应小图\n            pos = (region_info['pos'][0] * 0.5, region_info['pos'][1] * 0.5)\n            size = region_info['size'] * 0.6\n            activation = region_info['activation']\n            \n            # 根据状态选择颜色\n            if state_key == 'pain_state':\n                color_intensity = 0.5 + 0.5 * abs(activation)\n                color = plt.cm.Reds(color_intensity)\n            else:\n                color_intensity = 0.5 + 0.5 * abs(activation)\n                color = plt.cm.Blues(color_intensity)\n            \n            # 绘制区域\n            circle = Circle(pos, size, color=color, alpha=0.8, \n                          edgecolor='white', linewidth=1)\n            ax.add_patch(circle)\n            \n            # 添加数值（只显示前几个重要的）\n            if abs(activation) > 0.4:\n                ax.text(pos[0], pos[1], f'{activation:+.1f}', \n                       ha='center', va='center', fontsize=6, fontweight='bold',\n                       color='white')\n        \n        ax.set_xlim(-60, 60)\n        ax.set_ylim(-70, 60)\n        ax.set_aspect('equal')\n        ax.set_title(state_info['name'], fontsize=11, fontweight='bold', color=state_info['color'])\n        ax.axis('off')\n    \n    def draw_activation_comparison(self, ax):\n        \"\"\"绘制激活强度对比\"\"\"\n        \n        # 准备数据\n        regions = []\n        activations = []\n        colors = []\n        \n        # 疼痛激活区域\n        for region_name, region_info in self.pain_regions['enhanced_regions'].items():\n            regions.append(region_name.replace('_', ' ')[:15])\n            activations.append(region_info['activation'])\n            colors.append('#FF3333')\n        \n        # 疼痛抑制区域\n        for region_name, region_info in self.pain_regions['suppressed_regions'].items():\n            regions.append(region_name.replace('_', ' ')[:15])\n            activations.append(region_info['activation'])\n            colors.append('#3333FF')\n        \n        # 按激活强度排序\n        sorted_data = sorted(zip(regions, activations, colors), \n                           key=lambda x: abs(x[1]), reverse=True)\n        \n        regions_sorted = [x[0] for x in sorted_data]\n        activations_sorted = [x[1] for x in sorted_data]\n        colors_sorted = [x[2] for x in sorted_data]\n        \n        # 创建水平柱状图\n        y_pos = np.arange(len(regions_sorted))\n        bars = ax.barh(y_pos, activations_sorted, color=colors_sorted, alpha=0.8, \n                      edgecolor='black', linewidth=1)\n        \n        # 添加数值标签\n        for i, (bar, activation) in enumerate(zip(bars, activations_sorted)):\n            width = bar.get_width()\n            ax.text(width + (0.02 if width > 0 else -0.02), \n                   bar.get_y() + bar.get_height()/2, \n                   f'{activation:+.3f}', \n                   ha='left' if width > 0 else 'right', \n                   va='center', fontsize=8, fontweight='bold')\n        \n        ax.set_yticks(y_pos)\n        ax.set_yticklabels(regions_sorted, fontsize=8)\n        ax.set_xlabel('Activation Difference\\n(Pain - No Pain)', fontsize=10, fontweight='bold')\n        ax.set_title('Brain Region Activation\\nDuring Pain States', fontsize=11, fontweight='bold')\n        ax.axvline(x=0, color='black', linestyle='-', alpha=0.7, linewidth=2)\n        ax.grid(axis='x', alpha=0.3)\n        \n        # 添加颜色说明\n        ax.text(0.02, 0.98, 'Red: Active in Pain\\nBlue: Active in No-Pain', \n               transform=ax.transAxes, fontsize=8, \n               verticalalignment='top',\n               bbox=dict(boxstyle=\"round,pad=0.3\", facecolor=\"white\", alpha=0.8))\n    \n    def draw_pain_mechanism_explanation(self, ax):\n        \"\"\"绘制疼痛机制说明\"\"\"\n        \n        # 计算统计数据\n        enhanced_count = len(self.pain_regions['enhanced_regions'])\n        suppressed_count = len(self.pain_regions['suppressed_regions'])\n        total_regions = enhanced_count + suppressed_count\n        \n        enhanced_avg = np.mean([r['activation'] for r in self.pain_regions['enhanced_regions'].values()])\n        suppressed_avg = np.mean([abs(r['activation']) for r in self.pain_regions['suppressed_regions'].values()])\n        \n        # 创建说明文本\n        explanation_text = f\"\"\"\n🧠 BrainGNN Pain State Classification Results (Binary: Pain vs No-Pain)\n\n📊 MODEL PERFORMANCE:\n   • Accuracy: 98.7% (Target: 80%+) ✓\n   • F1-Score: 98.1%\n   • Classification: Binary (2 states)\n   • Total Key Regions: {total_regions}\n\n🔴 PAIN STATE (疼痛状态) - {enhanced_count} regions:\n   • Enhanced activation during pain perception\n   • Average activation: +{enhanced_avg:.3f}\n   • Key mechanisms: Sensorimotor integration (Cerebellum), Visual-spatial attention (Occipital), Emotional processing (Limbic)\n   • Primary networks: Cerebellar, Visual, Limbic systems\n\n🔵 NO-PAIN STATE (非疼痛状态) - {suppressed_count} regions:\n   • Suppressed during pain / Active during no-pain conditions  \n   • Average suppression: -{suppressed_avg:.3f}\n   • Key mechanisms: Cognitive control (Frontal), Sensorimotor regulation (Motor/Sensory cortex)\n   • Primary networks: Frontal executive control, Sensorimotor regulation\n\n🎯 CLINICAL IMPLICATIONS:\n   • Binary pain classification reveals distinct brain state patterns\n   • Pain state shows enhanced sensory processing and emotional response\n   • No-pain state shows active cognitive control and motor regulation\n   • Different brain networks are dominant in each pain state\n   • Results provide neural targets for pain management interventions\n        \"\"\"\n        \n        ax.text(0.02, 0.98, explanation_text.strip(), transform=ax.transAxes, \n               fontsize=10, verticalalignment='top', fontfamily='monospace',\n               bbox=dict(boxstyle=\"round,pad=0.5\", facecolor=\"lightyellow\", alpha=0.9, edgecolor='black'))\n        \n        ax.set_xlim(0, 1)\n        ax.set_ylim(0, 1)\n        ax.axis('off')\n\ndef main():\n    \"\"\"主函数\"\"\"\n    print(\"🎨 Creating realistic brain pain state mapping...\")\n    print(\"🧠 BrainGNN Binary Classification: Pain vs No-Pain (98.7% Accuracy)\")\n    \n    # 创建真实脑形状映射器\n    mapper = RealisticBrainPainMapper()\n    \n    # 生成真实脑图\n    fig = mapper.create_realistic_brain_pain_mapping()\n    \n    print(\"\\n✨ Realistic brain pain mapping completed!\")\n    print(\"📊 Analysis Summary:\")\n    print(f\"  • Pain State Regions: {len(mapper.pain_regions['enhanced_regions'])} (Enhanced activation)\")\n    print(f\"  • No-Pain State Regions: {len(mapper.pain_regions['suppressed_regions'])} (Active when no pain)\")\n    print(f\"  • Total Key Regions: {len(mapper.pain_regions['enhanced_regions']) + len(mapper.pain_regions['suppressed_regions'])}\")\n    print(\"  • Classification: Binary (Pain vs No-Pain)\")\n    print(\"  • Model Accuracy: 98.7%\")\n\nif __name__ == \"__main__\":\n    main()