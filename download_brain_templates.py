#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载SurfIce大脑模板文件
Download brain template files for SurfIce
"""

import requests
import os
from urllib.parse import urlparse

class BrainTemplateDownloader:
    """大脑模板下载器"""
    
    def __init__(self):
        self.output_dir = './figures/surfice_templates/'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def download_file(self, url, filename):
        """下载文件"""
        
        filepath = os.path.join(self.output_dir, filename)
        
        if os.path.exists(filepath):
            print(f"✅ {filename} already exists")
            return filepath
        
        try:
            print(f"⬇️ Downloading {filename}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            return None
    
    def download_common_templates(self):
        """下载常用大脑模板"""
        
        print("🧠 Downloading brain templates for SurfIce...")
        
        # SurfIce常用模板URL
        templates = {
            # FreeSurfer模板
            'BrainMesh_ICBM152.mz3': 'https://github.com/rordenlab/SurfIce-templates/raw/master/BrainMesh_ICBM152.mz3',
            'BrainMesh_ICBM152Left.mz3': 'https://github.com/rordenlab/SurfIce-templates/raw/master/BrainMesh_ICBM152Left.mz3',
            'BrainMesh_ICBM152Right.mz3': 'https://github.com/rordenlab/SurfIce-templates/raw/master/BrainMesh_ICBM152Right.mz3',
            
            # 备用链接
            'mni152.mz3': 'https://www.nitrc.org/frs/download.php/11665/BrainMesh_ICBM152.mz3',
        }
        
        downloaded_files = []
        
        for filename, url in templates.items():
            try:
                result = self.download_file(url, filename)
                if result:
                    downloaded_files.append(result)
            except Exception as e:
                print(f"⚠️ Skipping {filename}: {e}")
                continue
        
        return downloaded_files
    
    def create_simple_brain_mesh(self):
        """创建简单的大脑网格文件"""
        
        print("🔧 Creating simple brain mesh...")
        
        # 创建简化的大脑表面网格 (球形近似)
        import numpy as np
        
        # 生成球面坐标
        phi = np.linspace(0, 2*np.pi, 50)  # 经度
        theta = np.linspace(0, np.pi, 25)   # 纬度
        
        vertices = []
        faces = []
        
        # 生成顶点
        for i, t in enumerate(theta):
            for j, p in enumerate(phi):
                x = 70 * np.sin(t) * np.cos(p)  # 半径约70mm
                y = 85 * np.sin(t) * np.sin(p)  # 前后稍长
                z = 65 * np.cos(t)              # 上下稍短
                
                # 大脑形状调整
                if y > 40:  # 前额叶
                    y *= 1.2
                    z *= 0.9
                elif abs(x) > 50 and z < 20:  # 颞叶
                    z -= 15
                
                vertices.append([x, y, z])
        
        # 生成三角面
        for i in range(len(theta)-1):
            for j in range(len(phi)-1):
                # 当前四边形的四个顶点索引
                v1 = i * len(phi) + j
                v2 = i * len(phi) + (j + 1) % len(phi)
                v3 = (i + 1) * len(phi) + j
                v4 = (i + 1) * len(phi) + (j + 1) % len(phi)
                
                # 分割为两个三角形
                faces.append([v1, v2, v3])
                faces.append([v2, v4, v3])
        
        # 保存为PLY格式 (SurfIce支持)
        ply_file = os.path.join(self.output_dir, 'simple_brain.ply')
        
        with open(ply_file, 'w') as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(vertices)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write(f"element face {len(faces)}\n")
            f.write("property list uchar int vertex_indices\n")
            f.write("end_header\n")
            
            # 写入顶点
            for vertex in vertices:
                f.write(f"{vertex[0]:.2f} {vertex[1]:.2f} {vertex[2]:.2f}\n")
            
            # 写入面
            for face in faces:
                f.write(f"3 {face[0]} {face[1]} {face[2]}\n")
        
        print(f"✅ Simple brain mesh created: {ply_file}")
        
        return ply_file
    
    def create_usage_instructions(self):
        """创建使用说明"""
        
        instructions = """# 🧠 SurfIce大脑模板使用指南

## 📁 模板文件说明

### 下载的模板 (如果成功):
- `BrainMesh_ICBM152.mz3` - 完整ICBM152大脑网格
- `BrainMesh_ICBM152Left.mz3` - 左半球
- `BrainMesh_ICBM152Right.mz3` - 右半球

### 本地生成的模板:
- `simple_brain.ply` - 简化大脑网格 (总是可用)

## 🚀 在SurfIce中使用

### 方法1: 使用下载的模板 (推荐)
1. 打开SurfIce
2. **Mesh** → **Load Mesh**
3. 选择 `BrainMesh_ICBM152.mz3`
4. **Overlay** → **Add Overlay**
5. 选择 `../surfice_visualization/braingnn_pain_activation.nii.gz`

### 方法2: 使用简化模板
1. 打开SurfIce
2. **Mesh** → **Load Mesh**
3. 选择 `simple_brain.ply`
4. 加载激活覆盖层

### 方法3: 使用SurfIce内置模板
1. 打开SurfIce
2. 在启动界面或菜单中查找:
   - "Load Standard Brain"
   - "Templates"
   - "Examples"
3. 选择任何大脑模板

## 🔧 替代方案

### 如果没有合适的模板:
1. **使用在线资源**:
   - 访问: https://github.com/rordenlab/SurfIce-templates
   - 手动下载模板文件

2. **使用其他软件查看**:
   - FSLeyes (免费)
   - MRIcroGL
   - 3D Slicer

3. **转换我们的可视化**:
   - 使用Python脚本重新生成其他格式

## 📊 关键提示

### 文件兼容性:
- `.mz3` - SurfIce原生格式 (最佳)
- `.ply` - 通用3D格式 (良好)
- `.obj` - 3D对象格式 (支持)
- `.stl` - 立体光刻格式 (支持)

### 加载顺序:
1. 先加载大脑网格 (Mesh)
2. 再加载激活覆盖层 (Overlay)
3. 调整颜色和透明度

## ⚡ 快速开始

### 最简单的方法:
```
1. 打开SurfIce
2. 如果看到任何大脑模板选项，直接选择
3. 然后加载我们的激活文件:
   ../surfice_visualization/braingnn_pain_activation.nii.gz
```

---
🧠 BrainGNN Pain Classification
📊 98.7% Accuracy Visualization
"""
        
        instructions_file = os.path.join(self.output_dir, 'TEMPLATE_USAGE.md')
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"✅ Usage instructions: {instructions_file}")
        
        return instructions_file

def main():
    """主函数"""
    print("=" * 60)
    print("🧠 SurfIce Brain Template Downloader")
    print("=" * 60)
    
    downloader = BrainTemplateDownloader()
    
    # 尝试下载标准模板
    print("\n📥 Attempting to download standard templates...")
    downloaded = downloader.download_common_templates()
    
    # 创建简单模板 (备用)
    print("\n🔧 Creating backup template...")
    simple_template = downloader.create_simple_brain_mesh()
    
    # 创建使用说明
    instructions = downloader.create_usage_instructions()
    
    print("\n" + "=" * 60)
    print("✅ Template setup completed!")
    
    if downloaded:
        print(f"📥 Downloaded {len(downloaded)} template(s)")
    else:
        print("⚠️ No templates downloaded from internet")
    
    print(f"🔧 Created local template: simple_brain.ply")
    print("📖 Read TEMPLATE_USAGE.md for instructions")
    print("=" * 60)

if __name__ == "__main__":
    main()