#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建适合SurfIce查看的脑图文件
Create brain visualization files for SurfIce viewing
"""

import numpy as np
import nibabel as nib
import pandas as pd
import os
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib import cm

class SurfIceVisualizationCreator:
    """创建SurfIce可视化文件"""
    
    def __init__(self):
        self.setup_data()
        self.output_dir = './figures/surfice_visualization/'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def setup_data(self):
        """设置BrainGNN数据"""
        
        # BrainGNN关键脑区和激活值
        self.regions = {
            # 疼痛激活区域 (正值，红色)
            'Cerebelum_Crus1_R': {'coords': [28, -77, -33], 'value': 0.601},
            'Cerebelum_Crus1_L': {'coords': [-28, -77, -33], 'value': 0.438},
            'Occipital_Mid_R': {'coords': [31, -87, 11], 'value': 0.528},
            'Occipital_Sup_R': {'coords': [20, -93, 15], 'value': 0.528},
            'Occipital_Mid_L': {'coords': [-31, -87, 11], 'value': 0.385},
            'ParaHippocampal_L': {'coords': [-24, -7, -21], 'value': 0.120},
            'Amygdala_R': {'coords': [25, -1, -20], 'value': 0.080},
            
            # 疼痛抑制区域 (负值，蓝色)
            'Frontal_Sup_L': {'coords': [-15, 26, 56], 'value': -0.512},
            'Frontal_Mid_L': {'coords': [-30, 47, 28], 'value': -0.498},
            'Precentral_L': {'coords': [-39, -6, 52], 'value': -0.433},
            'Postcentral_L': {'coords': [-43, -25, 49], 'value': -0.431},
            'Rolandic_Oper_L': {'coords': [-50, 0, 9], 'value': -0.401},
            'Frontal_Sup_R': {'coords': [15, 26, 56], 'value': -0.394},
            'Putamen_R': {'coords': [26, 6, 0], 'value': -0.386}
        }
    
    def create_nifti_overlay(self):
        """创建NIfTI格式的激活图"""
        
        print("🧠 Creating NIfTI overlay for SurfIce...")
        
        # MNI152标准空间参数
        dims = (91, 109, 91)  # 2mm分辨率
        affine = np.array([
            [-2, 0, 0, 90],
            [0, 2, 0, -126],
            [0, 0, 2, -72],
            [0, 0, 0, 1]
        ])
        
        # 创建空白体积
        volume = np.zeros(dims)
        
        # 为每个脑区添加激活
        for region_name, region_data in self.regions.items():
            mni_coords = region_data['coords']
            activation = region_data['value']
            
            # MNI到体素坐标转换
            voxel_coords = nib.affines.apply_affine(np.linalg.inv(affine), mni_coords)
            voxel_coords = voxel_coords.astype(int)
            
            # 创建球形激活区域
            radius = 8  # 体素半径
            
            for i in range(max(0, voxel_coords[0] - radius), 
                         min(dims[0], voxel_coords[0] + radius + 1)):
                for j in range(max(0, voxel_coords[1] - radius), 
                             min(dims[1], voxel_coords[1] + radius + 1)):
                    for k in range(max(0, voxel_coords[2] - radius), 
                                 min(dims[2], voxel_coords[2] + radius + 1)):
                        
                        # 计算到中心的距离
                        dist = np.sqrt((i - voxel_coords[0])**2 + 
                                     (j - voxel_coords[1])**2 + 
                                     (k - voxel_coords[2])**2)
                        
                        if dist <= radius:
                            # 高斯衰减
                            weight = np.exp(-0.5 * (dist / (radius/2))**2)
                            volume[i, j, k] += activation * weight
        
        # 平滑处理
        volume = gaussian_filter(volume, sigma=1.5)
        
        # 创建NIfTI图像
        nii_img = nib.Nifti1Image(volume, affine)
        
        # 保存文件
        nifti_file = os.path.join(self.output_dir, 'braingnn_pain_activation.nii')
        nib.save(nii_img, nifti_file)
        
        # 同时保存压缩版本
        nifti_gz_file = os.path.join(self.output_dir, 'braingnn_pain_activation.nii.gz')
        nib.save(nii_img, nifti_gz_file)
        
        print(f"✅ NIfTI files created:")
        print(f"  • {nifti_file}")
        print(f"  • {nifti_gz_file}")
        
        return nifti_file, nifti_gz_file
    
    def create_text_overlay(self):
        """创建文本格式的覆盖数据"""
        
        print("📝 Creating text overlay for SurfIce...")
        
        # 创建MNI坐标和激活值的文本文件
        text_file = os.path.join(self.output_dir, 'braingnn_activation.txt')
        
        with open(text_file, 'w') as f:
            f.write("# BrainGNN Pain Activation Data\n")
            f.write("# Format: X Y Z Value Label\n")
            f.write("# Positive values = pain activation (red)\n")
            f.write("# Negative values = pain suppression (blue)\n\n")
            
            for region_name, region_data in self.regions.items():
                x, y, z = region_data['coords']
                value = region_data['value']
                f.write(f"{x:6.1f} {y:6.1f} {z:6.1f} {value:7.3f} {region_name}\n")
        
        print(f"✅ Text overlay created: {text_file}")
        
        return text_file
    
    def create_colormap_file(self):
        """创建颜色映射文件"""
        
        print("🎨 Creating custom colormap...")
        
        # 创建红-白-蓝颜色映射
        colormap_file = os.path.join(self.output_dir, 'pain_colormap.txt')
        
        with open(colormap_file, 'w') as f:
            f.write("# Pain activation colormap\n")
            f.write("# Format: Value R G B\n")
            f.write("-0.6 0 0 255\n")     # 深蓝
            f.write("-0.3 100 100 255\n") # 浅蓝
            f.write("0.0 255 255 255\n")  # 白色
            f.write("0.3 255 100 100\n")  # 浅红
            f.write("0.6 255 0 0\n")      # 深红
        
        print(f"✅ Colormap created: {colormap_file}")
        
        return colormap_file
    
    def create_surfice_instructions(self):
        """创建SurfIce使用说明"""
        
        instructions = """# 🧠 SurfIce可视化使用说明

## 📂 生成的文件
- `braingnn_pain_activation.nii` - 未压缩的NIfTI激活图
- `braingnn_pain_activation.nii.gz` - 压缩的NIfTI激活图
- `braingnn_activation.txt` - 文本格式的激活数据
- `pain_colormap.txt` - 自定义颜色映射

## 🚀 在SurfIce中查看

### 方法1: 加载NIfTI覆盖层 (推荐)
1. 打开SurfIce
2. **File** → **Open** → 选择标准大脑模板 (如MNI152)
3. **Overlay** → **Add overlay** → 选择 `braingnn_pain_activation.nii.gz`
4. **Overlay** → **Color** → 选择 "Red-Blue" 或 "Hot-Cold"
5. 设置阈值: Min = -0.6, Max = 0.6

### 方法2: 使用菜单加载
1. **Mesh** → **Load Mesh** → 选择脑表面网格
2. **Overlay** → **Load Overlay** → 选择激活文件
3. 调整透明度和颜色

### 🎨 推荐设置
- **着色器**: Matte 或 Phong
- **透明度**: 70-80%
- **颜色方案**: Red-Blue (双极)
- **阈值**: ±0.1 到 ±0.6

### 📸 保存图像
- **File** → **Save Bitmap** - 保存当前视图
- 建议保存多个角度：
  - 左侧视图 (L)
  - 右侧视图 (R)
  - 顶部视图 (Superior)
  - 前视图 (Anterior)

## 🔍 数据说明
- **红色区域**: 疼痛状态激活增强 (7个区域)
- **蓝色区域**: 疼痛状态激活抑制 (7个区域)
- **分类准确率**: 98.7%
- **坐标系**: MNI标准空间

## ⚡ 快速提示
- 使用鼠标左键旋转视图
- 使用鼠标右键缩放
- 按住Shift拖动来平移
- 双击重置视图

## 📊 关键脑区
### 疼痛激活 (红色)
- 小脑Crus1区 (双侧)
- 枕叶中部/上部
- 海马旁回
- 杏仁核

### 疼痛抑制 (蓝色)
- 额上/中回
- 中央前/后回
- 壳核

---
🧠 BrainGNN Pain Classification Project
📊 98.7% Accuracy | 14 Key Brain Regions
"""
        
        instructions_file = os.path.join(self.output_dir, 'SURFICE_INSTRUCTIONS.md')
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"✅ Instructions created: {instructions_file}")
        
        return instructions_file
    
    def create_all_files(self):
        """创建所有文件"""
        
        print("🚀 Creating SurfIce visualization files...")
        print("🧠 BrainGNN Pain Classification - 98.7% Accuracy")
        
        # 创建各种格式的文件
        nifti_file, nifti_gz_file = self.create_nifti_overlay()
        text_file = self.create_text_overlay()
        colormap_file = self.create_colormap_file()
        instructions_file = self.create_surfice_instructions()
        
        # 创建预览图
        self.create_preview_image()
        
        print("\n✅ All files created successfully!")
        print(f"📁 Output directory: {self.output_dir}")
        print("\n📂 Generated files:")
        print(f"  • NIfTI overlay: {os.path.basename(nifti_gz_file)}")
        print(f"  • Text data: {os.path.basename(text_file)}")
        print(f"  • Instructions: {os.path.basename(instructions_file)}")
        
        print("\n🎯 Next steps:")
        print("1. Open SurfIce")
        print("2. Load a brain template (File → Open)")
        print("3. Add overlay (Overlay → Add overlay → braingnn_pain_activation.nii.gz)")
        print("4. Adjust colors and thresholds")
        
        return {
            'nifti': nifti_file,
            'nifti_gz': nifti_gz_file,
            'text': text_file,
            'colormap': colormap_file,
            'instructions': instructions_file
        }
    
    def create_preview_image(self):
        """创建预览图像"""
        
        print("📸 Creating preview image...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 左图：脑区位置
        ax1.set_title('Brain Regions - MNI Coordinates', fontsize=14)
        
        colors = []
        x_coords = []
        y_coords = []
        labels = []
        
        for region_name, region_data in self.regions.items():
            x, y, z = region_data['coords']
            value = region_data['value']
            
            x_coords.append(x)
            y_coords.append(y)
            colors.append('red' if value > 0 else 'blue')
            labels.append(region_name.split('_')[0])
        
        scatter = ax1.scatter(x_coords, y_coords, c=colors, s=200, alpha=0.7, edgecolors='white', linewidth=2)
        
        for i, label in enumerate(labels):
            ax1.annotate(label, (x_coords[i], y_coords[i]), fontsize=8, ha='center')
        
        ax1.set_xlabel('X (Left ← → Right)', fontsize=12)
        ax1.set_ylabel('Y (Posterior ← → Anterior)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(-80, 80)
        ax1.set_ylim(-120, 80)
        
        # 右图：激活强度
        ax2.set_title('Activation Strength by Region', fontsize=14)
        
        regions = list(self.regions.keys())
        values = [self.regions[r]['value'] for r in regions]
        colors = ['red' if v > 0 else 'blue' for v in values]
        
        bars = ax2.barh(range(len(regions)), values, color=colors, alpha=0.7)
        ax2.set_yticks(range(len(regions)))
        ax2.set_yticklabels([r.replace('_', ' ') for r in regions], fontsize=10)
        ax2.set_xlabel('Activation Value', fontsize=12)
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(True, axis='x', alpha=0.3)
        
        plt.suptitle('BrainGNN Pain Classification - SurfIce Visualization Data\n98.7% Accuracy', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        preview_file = os.path.join(self.output_dir, 'preview.png')
        plt.savefig(preview_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Preview image created: {preview_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("🧠 SurfIce Visualization File Creator")
    print("=" * 60)
    
    # 创建可视化文件
    creator = SurfIceVisualizationCreator()
    files = creator.create_all_files()
    
    print("\n" + "=" * 60)
    print("✅ SurfIce visualization files ready!")
    print("🎯 Please follow the instructions in SURFICE_INSTRUCTIONS.md")
    print("=" * 60)

if __name__ == "__main__":
    main()