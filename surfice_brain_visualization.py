#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SurfIce人脑可视化数据生成器
SurfIce Brain Visualization Data Generator for BrainGNN Pain Classification
"""

import numpy as np
import pandas as pd
import os
import nibabel as nib
from scipy.spatial.distance import cdist
import json

class SurfIceBrainDataGenerator:
    """SurfIce大脑数据生成器"""
    
    def __init__(self):
        self.setup_brain_data()
        self.setup_output_dirs()
        
    def setup_brain_data(self):
        """设置脑区数据 - BrainGNN疼痛分类结果"""
        
        # BrainGNN关键脑区结果 (MNI坐标)
        self.brain_regions = {
            # 疼痛激活区域 (正值)
            'Cerebelum_Crus1_R': {
                'mni_coords': [28, -77, -33],
                'activation': 0.601,
                'hemisphere': 'R',
                'lobe': 'Cerebellum',
                'network': 'Sensorimotor',
                'aal_id': 104,
                'description': 'Primary sensorimotor integration'
            },
            'Cerebelum_Crus1_L': {
                'mni_coords': [-28, -77, -33],
                'activation': 0.438,
                'hemisphere': 'L',
                'lobe': 'Cerebellum',
                'network': 'Sensorimotor',
                'aal_id': 103,
                'description': 'Bilateral cerebellar coordination'
            },
            'Occipital_Mid_R': {
                'mni_coords': [31, -87, 11],
                'activation': 0.528,
                'hemisphere': 'R',
                'lobe': 'Occipital',
                'network': 'Visual',
                'aal_id': 54,
                'description': 'Visual-spatial pain processing'
            },
            'Occipital_Sup_R': {
                'mni_coords': [20, -93, 15],
                'activation': 0.528,
                'hemisphere': 'R',
                'lobe': 'Occipital',
                'network': 'Visual',
                'aal_id': 52,
                'description': 'Enhanced visual attention'
            },
            'Occipital_Mid_L': {
                'mni_coords': [-31, -87, 11],
                'activation': 0.385,
                'hemisphere': 'L',
                'lobe': 'Occipital',
                'network': 'Visual',
                'aal_id': 53,
                'description': 'Bilateral visual processing'
            },
            'ParaHippocampal_L': {
                'mni_coords': [-24, -7, -21],
                'activation': 0.120,
                'hemisphere': 'L',
                'lobe': 'Temporal',
                'network': 'Limbic',
                'aal_id': 39,
                'description': 'Pain memory encoding'
            },
            'Amygdala_R': {
                'mni_coords': [25, -1, -20],
                'activation': 0.080,
                'hemisphere': 'R',
                'lobe': 'Temporal',
                'network': 'Limbic',
                'aal_id': 42,
                'description': 'Emotional pain response'
            },
            
            # 疼痛抑制区域 (负值)
            'Frontal_Sup_L': {
                'mni_coords': [-15, 26, 56],
                'activation': -0.512,
                'hemisphere': 'L',
                'lobe': 'Frontal',
                'network': 'Executive',
                'aal_id': 3,
                'description': 'Top-down cognitive control'
            },
            'Frontal_Mid_L': {
                'mni_coords': [-30, 47, 28],
                'activation': -0.498,
                'hemisphere': 'L',
                'lobe': 'Frontal',
                'network': 'Executive',
                'aal_id': 5,
                'description': 'Executive function regulation'
            },
            'Precentral_L': {
                'mni_coords': [-39, -6, 52],
                'activation': -0.433,
                'hemisphere': 'L',
                'lobe': 'Frontal',
                'network': 'Motor',
                'aal_id': 1,
                'description': 'Motor cortex inhibition'
            },
            'Postcentral_L': {
                'mni_coords': [-43, -25, 49],
                'activation': -0.431,
                'hemisphere': 'L',
                'lobe': 'Parietal',
                'network': 'Somatosensory',
                'aal_id': 57,
                'description': 'Sensory cortex regulation'
            },
            'Rolandic_Oper_L': {
                'mni_coords': [-50, 0, 9],
                'activation': -0.401,
                'hemisphere': 'L',
                'lobe': 'Frontal',
                'network': 'Sensorimotor',
                'aal_id': 17,
                'description': 'Sensorimotor integration'
            },
            'Frontal_Sup_R': {
                'mni_coords': [15, 26, 56],
                'activation': -0.394,
                'hemisphere': 'R',
                'lobe': 'Frontal',
                'network': 'Executive',
                'aal_id': 4,
                'description': 'Bilateral cognitive control'
            },
            'Putamen_R': {
                'mni_coords': [26, 6, 0],
                'activation': -0.386,
                'hemisphere': 'R',
                'lobe': 'Subcortical',
                'network': 'Subcortical',
                'aal_id': 76,
                'description': 'Motor regulation suppression'
            }
        }
        
    def setup_output_dirs(self):
        """设置输出目录"""
        
        self.output_dir = './figures/surfice_data/'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 创建子目录
        subdirs = ['meshes', 'overlays', 'scripts', 'nodes', 'edges']
        for subdir in subdirs:
            os.makedirs(os.path.join(self.output_dir, subdir), exist_ok=True)
    
    def create_node_file(self):
        """创建SurfIce节点文件"""
        
        print("📍 Creating SurfIce node file...")
        
        # 创建节点数据
        nodes_data = []
        
        for region_name, region_data in self.brain_regions.items():
            x, y, z = region_data['mni_coords']
            activation = region_data['activation']
            
            # SurfIce节点格式：X Y Z Color Size Label
            # 颜色：1=红色(激活), 2=蓝色(抑制), 3=绿色, 4=黄色
            color = 1 if activation > 0 else 2
            size = abs(activation) * 10 + 2  # 大小基于激活强度
            
            nodes_data.append({
                'X': x,
                'Y': y, 
                'Z': z,
                'Color': color,
                'Size': size,
                'Label': region_name,
                'Activation': activation,
                'Network': region_data['network'],
                'Lobe': region_data['lobe']
            })
        
        # 保存为CSV格式
        df = pd.DataFrame(nodes_data)
        node_file = os.path.join(self.output_dir, 'nodes', 'braingnn_pain_nodes.csv')
        df.to_csv(node_file, index=False)
        
        # 保存为SurfIce .node格式
        node_surfice_file = os.path.join(self.output_dir, 'nodes', 'braingnn_pain_nodes.node')
        with open(node_surfice_file, 'w') as f:
            f.write("// BrainGNN Pain State Classification Nodes\n")
            f.write("// Format: X Y Z Color Size Label\n")
            for _, row in df.iterrows():
                f.write(f"{row['X']:.1f} {row['Y']:.1f} {row['Z']:.1f} {row['Color']} {row['Size']:.1f} {row['Label']}\n")
        
        print(f"✅ Node files created:")
        print(f"  • CSV: {node_file}")
        print(f"  • Node: {node_surfice_file}")
        
        return node_file, node_surfice_file
    
    def create_edge_file(self):
        """创建SurfIce连接边文件"""
        
        print("🔗 Creating SurfIce edge file...")
        
        edges_data = []
        
        # 按网络创建连接
        networks = {}
        for region_name, region_data in self.brain_regions.items():
            network = region_data['network']
            if network not in networks:
                networks[network] = []
            networks[network].append({
                'name': region_name,
                'coords': region_data['mni_coords'],
                'activation': region_data['activation']
            })
        
        # 创建网络内连接
        edge_id = 0
        for network_name, regions in networks.items():
            if len(regions) > 1:
                for i in range(len(regions)):
                    for j in range(i + 1, len(regions)):
                        region1 = regions[i]
                        region2 = regions[j]
                        
                        # 计算连接强度 (基于激活值相似性)
                        strength = 1.0 - abs(region1['activation'] - region2['activation'])
                        
                        edges_data.append({
                            'ID': edge_id,
                            'Node1': region1['name'],
                            'Node2': region2['name'],
                            'X1': region1['coords'][0],
                            'Y1': region1['coords'][1],
                            'Z1': region1['coords'][2],
                            'X2': region2['coords'][0],
                            'Y2': region2['coords'][1],
                            'Z2': region2['coords'][2],
                            'Strength': strength,
                            'Network': network_name
                        })
                        edge_id += 1
        
        # 保存边文件
        df_edges = pd.DataFrame(edges_data)
        edge_file = os.path.join(self.output_dir, 'edges', 'braingnn_pain_edges.csv')
        df_edges.to_csv(edge_file, index=False)
        
        # 保存为SurfIce .edge格式
        edge_surfice_file = os.path.join(self.output_dir, 'edges', 'braingnn_pain_edges.edge')
        with open(edge_surfice_file, 'w') as f:
            f.write("// BrainGNN Pain State Network Connections\n")
            f.write("// Format: X1 Y1 Z1 X2 Y2 Z2 Strength\n")
            for _, row in df_edges.iterrows():
                f.write(f"{row['X1']:.1f} {row['Y1']:.1f} {row['Z1']:.1f} ")
                f.write(f"{row['X2']:.1f} {row['Y2']:.1f} {row['Z2']:.1f} ")
                f.write(f"{row['Strength']:.3f}\n")
        
        print(f"✅ Edge files created:")
        print(f"  • CSV: {edge_file}")
        print(f"  • Edge: {edge_surfice_file}")
        
        return edge_file, edge_surfice_file
    
    def create_overlay_data(self):
        """创建SurfIce覆盖层数据"""
        
        print("🎨 Creating SurfIce overlay data...")
        
        # 创建体素级激活图
        # 标准MNI空间：91x109x91体素，2mm分辨率
        voxel_size = 2.0  # mm
        origin = [-90, -126, -72]  # MNI原点偏移
        
        dims = (91, 109, 91)
        activation_volume = np.zeros(dims)
        
        # 为每个脑区创建高斯激活核
        for region_name, region_data in self.brain_regions.items():
            mni_coords = region_data['mni_coords']
            activation = region_data['activation']
            
            # 转换MNI坐标到体素坐标
            voxel_coords = [
                int((mni_coords[0] - origin[0]) / voxel_size),
                int((mni_coords[1] - origin[1]) / voxel_size),
                int((mni_coords[2] - origin[2]) / voxel_size)
            ]
            
            # 检查坐标是否在体积范围内
            if (0 <= voxel_coords[0] < dims[0] and 
                0 <= voxel_coords[1] < dims[1] and 
                0 <= voxel_coords[2] < dims[2]):
                
                # 创建高斯核 (半径约15mm)
                sigma = 7.5 / voxel_size  # 转换为体素单位
                
                for i in range(max(0, voxel_coords[0] - 15), 
                             min(dims[0], voxel_coords[0] + 16)):
                    for j in range(max(0, voxel_coords[1] - 15), 
                                 min(dims[1], voxel_coords[1] + 16)):
                        for k in range(max(0, voxel_coords[2] - 15), 
                                     min(dims[2], voxel_coords[2] + 16)):
                            
                            # 计算高斯权重
                            distance = np.sqrt((i - voxel_coords[0])**2 + 
                                             (j - voxel_coords[1])**2 + 
                                             (k - voxel_coords[2])**2)
                            
                            weight = np.exp(-0.5 * (distance / sigma)**2)
                            activation_volume[i, j, k] += activation * weight
        
        # 保存为NIfTI格式 (SurfIce支持)
        # 创建仿射矩阵
        affine = np.array([
            [-voxel_size, 0, 0, -origin[0]],
            [0, voxel_size, 0, origin[1]],
            [0, 0, voxel_size, origin[2]],
            [0, 0, 0, 1]
        ])
        
        # 创建NIfTI图像
        nii_img = nib.Nifti1Image(activation_volume, affine)
        
        # 保存文件
        overlay_file = os.path.join(self.output_dir, 'overlays', 'braingnn_pain_activation.nii.gz')
        nib.save(nii_img, overlay_file)
        
        print(f"✅ Overlay file created: {overlay_file}")
        
        return overlay_file
    
    def create_surfice_script(self):
        """创建SurfIce加载脚本"""
        
        print("📜 Creating SurfIce script...")
        
        script_content = '''
// BrainGNN Pain State Classification - SurfIce Visualization Script
// 使用方法：在SurfIce中执行此脚本

// 加载标准大脑模板
MESHLOAD('BrainMesh_ICBM152.mz3');

// 设置渲染参数
SHADERNAME('Brain');
LIGHTNAME('Standard');

// 加载疼痛激活覆盖层
OVERLAYLOAD('./overlays/braingnn_pain_activation.nii.gz');
OVERLAYCOLORNAME(1, 'RdBu');
OVERLAYMINMAX(1, -0.6, 0.6);
OVERLAYOPACITY(1, 0.8);

// 加载脑区节点
NODELOAD('./nodes/braingnn_pain_nodes.node');
NODEOPACITY(0.9);
NODESIZE(8);

// 加载网络连接
EDGELOAD('./edges/braingnn_pain_edges.edge');
EDGEOPACITY(0.7);
EDGEWIDTH(2);

// 设置视角 - 左侧视图
AZIMUTH(270);
ELEVATION(0);

// 保存渲染图像
SAVEBMP('./braingnn_pain_left_view.png');

// 右侧视图
AZIMUTH(90);
SAVEBMP('./braingnn_pain_right_view.png');

// 上方视图
AZIMUTH(0);
ELEVATION(90);
SAVEBMP('./braingnn_pain_top_view.png');

// 前方视图
AZIMUTH(0);
ELEVATION(0);
SAVEBMP('./braingnn_pain_front_view.png');

// 显示信息
PRINT('BrainGNN Pain Classification Visualization Loaded');
PRINT('Red regions: Pain activation');
PRINT('Blue regions: Pain suppression');
PRINT('Accuracy: 98.7%');
'''
        
        script_file = os.path.join(self.output_dir, 'scripts', 'load_braingnn_pain.txt')
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        print(f"✅ SurfIce script created: {script_file}")
        
        return script_file
    
    def create_readme(self):
        """创建使用说明"""
        
        readme_content = """# BrainGNN Pain State Classification - SurfIce Visualization

## 📊 数据概览
- **分类任务**: 疼痛 vs 无疼痛状态
- **准确率**: 98.7%
- **脑区数量**: 14个关键区域
- **坐标系**: MNI空间

## 📁 文件结构
```
surfice_data/
├── nodes/
│   ├── braingnn_pain_nodes.csv    # 脑区节点数据
│   └── braingnn_pain_nodes.node   # SurfIce节点格式
├── edges/
│   ├── braingnn_pain_edges.csv    # 网络连接数据
│   └── braingnn_pain_edges.edge   # SurfIce连接格式
├── overlays/
│   └── braingnn_pain_activation.nii.gz  # 激活覆盖层
├── scripts/
│   └── load_braingnn_pain.txt     # SurfIce加载脚本
└── README.md                      # 本文件
```

## 🚀 使用方法

### 1. 安装SurfIce
- 访问: https://www.nitrc.org/projects/surfice/
- 下载适合您系统的版本
- macOS: Surfice_macOS.dmg
- Windows: surfice_windows.zip
- Linux: surfice_linux.zip

### 2. 加载数据
有两种方法：

#### 方法A: 使用脚本自动加载
1. 打开SurfIce
2. 菜单: Scripting → Load Script
3. 选择: `scripts/load_braingnn_pain.txt`
4. 脚本将自动加载所有数据和设置视角

#### 方法B: 手动加载
1. 加载大脑网格: Mesh → Open → 选择标准脑模板
2. 加载激活图: Overlay → Open → `overlays/braingnn_pain_activation.nii.gz`
3. 加载节点: Node → Open → `nodes/braingnn_pain_nodes.node`
4. 加载连接: Edge → Open → `edges/braingnn_pain_edges.edge`

### 3. 调整显示
- **颜色映射**: Overlay → Color → RdBu (红-蓝)
- **阈值**: 设置为 -0.6 到 0.6
- **透明度**: 调整overlay和node的透明度
- **视角**: 使用鼠标旋转或预设视角

## 🎨 可视化说明

### 颜色编码
- 🔴 **红色区域**: 疼痛状态下激活增强
- 🔵 **蓝色区域**: 疼痛状态下激活抑制
- 🟡 **连接线**: 神经网络连接强度

### 关键脑区
#### 疼痛激活区域
- 小脑脚1区 (双侧): 感觉运动整合
- 枕叶中/上回 (右侧): 视觉-空间疼痛处理
- 海马旁回 (左侧): 疼痛记忆编码
- 杏仁核 (右侧): 情绪性疼痛反应

#### 疼痛抑制区域  
- 额上/中回 (左侧): 自上而下认知控制
- 中央前/后回 (左侧): 运动感觉皮层调节
- 壳核 (右侧): 运动调节抑制

### 神经网络
- **感觉运动网络**: 疼痛感知和运动响应
- **视觉网络**: 视觉-空间疼痛处理
- **边缘网络**: 情绪和记忆相关
- **执行网络**: 认知控制和调节

## 🔧 故障排除

### 常见问题
1. **文件无法加载**: 确保文件路径正确，使用相对路径
2. **显示异常**: 检查颜色映射和阈值设置
3. **性能问题**: 降低mesh分辨率或overlay透明度

### 系统要求
- **GPU**: 支持OpenGL 3.3+
- **内存**: 推荐4GB+
- **存储**: 确保有足够空间保存渲染图像

## 📚 参考文献
- BrainGNN: Graph Neural Networks for Brain Network Analysis
- SurfIce: Surface rendering for neuroimaging
- MNI空间: Montreal Neurological Institute coordinate system

## 📧 联系信息
如有问题，请参考SurfIce官方文档或社区支持。

---
🧠 **Generated for BrainGNN Pain Classification Project**
📊 **98.7% Classification Accuracy**
🎯 **Professional Neuroscience Visualization**
"""
        
        readme_file = os.path.join(self.output_dir, 'README.md')
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ README created: {readme_file}")
        
        return readme_file
    
    def create_all_data(self):
        """创建所有SurfIce数据文件"""
        
        print("🚀 Creating complete SurfIce visualization dataset...")
        print("🧠 BrainGNN Pain Classification: 98.7% Accuracy")
        
        # 创建各种数据文件
        node_csv, node_file = self.create_node_file()
        edge_csv, edge_file = self.create_edge_file()
        overlay_file = self.create_overlay_data()
        script_file = self.create_surfice_script()
        readme_file = self.create_readme()
        
        # 创建总结报告
        summary = {
            'dataset': 'BrainGNN Pain State Classification',
            'accuracy': '98.7%',
            'total_regions': len(self.brain_regions),
            'enhanced_regions': len([r for r in self.brain_regions.values() if r['activation'] > 0]),
            'suppressed_regions': len([r for r in self.brain_regions.values() if r['activation'] < 0]),
            'files_created': {
                'nodes_csv': node_csv,
                'nodes_surfice': node_file,
                'edges_csv': edge_csv,
                'edges_surfice': edge_file,
                'overlay_nifti': overlay_file,
                'script': script_file,
                'readme': readme_file
            },
            'networks': list(set([r['network'] for r in self.brain_regions.values()])),
            'coordinate_system': 'MNI',
            'software': 'SurfIce'
        }
        
        # 保存总结
        summary_file = os.path.join(self.output_dir, 'surfice_data_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n🎉 SurfIce visualization dataset completed!")
        print("📁 All files saved to: ./figures/surfice_data/")
        print("\n📊 Dataset Summary:")
        print(f"  • Total brain regions: {summary['total_regions']}")
        print(f"  • Enhanced regions: {summary['enhanced_regions']}")
        print(f"  • Suppressed regions: {summary['suppressed_regions']}")
        print(f"  • Neural networks: {len(summary['networks'])}")
        
        print("\n📂 Generated Files:")
        print(f"  • Node data: {os.path.basename(node_file)}")
        print(f"  • Edge data: {os.path.basename(edge_file)}")
        print(f"  • Overlay data: {os.path.basename(overlay_file)}")
        print(f"  • SurfIce script: {os.path.basename(script_file)}")
        print(f"  • Usage guide: README.md")
        
        print("\n🚀 Next Steps:")
        print("1. Download SurfIce: https://www.nitrc.org/projects/surfice/")
        print("2. Open SurfIce application")
        print("3. Load script: scripts/load_braingnn_pain.txt")
        print("4. Or manually load each file type")
        print("5. Adjust colors, thresholds, and views as needed")
        
        return summary

def main():
    """主函数"""
    print("🎯 BrainGNN SurfIce Visualization Data Generator")
    print("🧠 Creating professional neuroimaging visualization data...")
    
    # 创建数据生成器
    generator = SurfIceBrainDataGenerator()
    
    # 生成所有数据
    summary = generator.create_all_data()
    
    print("\n✅ SurfIce data generation completed successfully!")
    print("📖 Please read the README.md for detailed usage instructions.")

if __name__ == "__main__":
    main()