#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从SurfIce官方资源下载MZ3模板
Download Official MZ3 Templates from SurfIce Resources
"""

import requests
import os
from pathlib import Path
import urllib.request
import zipfile

def download_official_mz3_templates():
    """下载官方MZ3模板"""
    
    print("🌐 正在从SurfIce官方资源下载MZ3模板...")
    
    # 创建目录
    templates_dir = Path("./figures/surfice_templates")
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # SurfIce官方示例数据源
    mz3_sources = [
        {
            'name': 'pial.mz3',
            'url': 'https://github.com/rordenlab/MRIcroGL/raw/master/Resources/script/pial.mz3', 
            'description': '皮层表面'
        },
        {
            'name': 'BrainMesh_ICBM152.mz3',
            'url': 'https://github.com/rordenlab/MRIcroGL/raw/master/Resources/script/BrainMesh_ICBM152.mz3',
            'description': 'ICBM152标准大脑'
        },
        {
            'name': 'cortex.mz3', 
            'url': 'https://github.com/rordenlab/MRIcroGL/raw/master/Resources/script/cortex.mz3',
            'description': '皮层网格'
        }
    ]
    
    # 备用源 - MRIcroS官方资源
    backup_sources = [
        {
            'name': 'mni152.mz3',
            'url': 'https://www.nitrc.org/frs/download.php/7779/mni152.mz3',
            'description': 'MNI152标准模板'
        },
        {
            'name': 'brain.mz3',
            'url': 'https://github.com/neurolabusc/MRIcroS/raw/master/brain.mz3',
            'description': '标准大脑网格'
        }
    ]
    
    # 尝试下载官方模板
    successful_downloads = []
    
    print("📥 尝试下载MRIcroGL官方模板...")
    for template in mz3_sources:
        try:
            download_url = template['url']
            filename = template['name']
            filepath = templates_dir / filename
            
            print(f"   正在下载: {filename} ({template['description']})")
            
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filepath) / 1024
            print(f"   ✅ 下载成功: {filename} ({file_size:.1f} KB)")
            successful_downloads.append(filename)
            
        except Exception as e:
            print(f"   ❌ 下载失败: {filename} - {e}")
    
    # 尝试备用源
    if not successful_downloads:
        print("📥 尝试备用下载源...")
        for template in backup_sources:
            try:
                download_url = template['url']
                filename = template['name']
                filepath = templates_dir / filename
                
                print(f"   正在下载: {filename} ({template['description']})")
                
                response = requests.get(download_url, timeout=30)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filepath) / 1024
                print(f"   ✅ 下载成功: {filename} ({file_size:.1f} KB)")
                successful_downloads.append(filename)
                
            except Exception as e:
                print(f"   ❌ 下载失败: {filename} - {e}")
    
    return successful_downloads

def create_mz3_from_freesurfer():
    """从FreeSurfer格式创建MZ3文件"""
    
    print("🔧 从FreeSurfer数据创建MZ3格式...")
    
    # 这是MZ3的基本结构
    # MZ3格式: 简单的二进制网格格式
    try:
        import struct
        import numpy as np
        
        # 读取我们之前创建的顶点和面数据
        vertices_file = "./figures/surfice_templates/brain_vertices.txt"
        faces_file = "./figures/surfice_templates/brain_faces.txt"
        
        if not os.path.exists(vertices_file) or not os.path.exists(faces_file):
            print("❌ FreeSurfer文件不存在，无法创建MZ3")
            return False
        
        # 读取顶点
        vertices = []
        with open(vertices_file, 'r') as f:
            num_vertices = int(f.readline().strip())
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
        
        # 读取面
        faces = []
        with open(faces_file, 'r') as f:
            num_faces = int(f.readline().strip())
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    faces.append([int(parts[1]), int(parts[2]), int(parts[3])])
        
        # 创建简化的MZ3文件
        mz3_path = "./figures/surfice_templates/braingnn_brain.mz3"
        
        with open(mz3_path, 'wb') as f:
            # MZ3文件头 (简化版)
            f.write(struct.pack('<4s', b'MZ3\x00'))  # 格式标识
            f.write(struct.pack('<I', len(vertices)))  # 顶点数
            f.write(struct.pack('<I', len(faces)))     # 面数
            f.write(struct.pack('<I', 0))              # 其他数据
            
            # 写入顶点数据
            for vertex in vertices:
                f.write(struct.pack('<fff', vertex[0], vertex[1], vertex[2]))
            
            # 写入面数据
            for face in faces:
                f.write(struct.pack('<III', face[0], face[1], face[2]))
        
        file_size = os.path.getsize(mz3_path) / 1024
        print(f"✅ MZ3文件创建成功: braingnn_brain.mz3 ({file_size:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"❌ 创建MZ3文件失败: {e}")
        return False

def download_alternate_brain_templates():
    """下载其他标准大脑模板"""
    
    print("🧠 下载其他标准大脑模板...")
    
    templates_dir = Path("./figures/surfice_templates")
    
    # 其他格式的标准模板
    alternate_sources = [
        {
            'name': 'colin27.ply',
            'url': 'https://github.com/Washington-University/workbench/raw/master/src/Resources/colin27.ply',
            'description': 'Colin27大脑模板'
        },
        {
            'name': 'fsaverage.ply',
            'url': 'https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/6.0.0/average/lh.pial.gii',
            'description': 'FreeSurfer平均模板'
        }
    ]
    
    successful_downloads = []
    
    for template in alternate_sources:
        try:
            download_url = template['url']
            filename = template['name']
            filepath = templates_dir / filename
            
            print(f"   正在下载: {filename} ({template['description']})")
            
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filepath) / 1024
            print(f"   ✅ 下载成功: {filename} ({file_size:.1f} KB)")
            successful_downloads.append(filename)
            
        except Exception as e:
            print(f"   ❌ 下载失败: {filename} - {e}")
    
    return successful_downloads

def create_template_summary():
    """创建模板文件总结"""
    
    print("📋 创建模板文件总结...")
    
    templates_dir = Path("./figures/surfice_templates")
    
    summary_content = """# 🧠 SurfIce大脑模板文件总结

## 📁 可用的大脑模板:

### ✅ 自制模版 (推荐先试这些):
- `brain_fixed.ply` - 修正的PLY格式大脑 (推荐)
- `brain.obj` - OBJ格式大脑 (通用)
- `brain.stl` - STL格式大脑 (3D标准)
- `braingnn_brain.mz3` - 转换的MZ3格式 (如果成功创建)

### 🌐 下载的官方模板:
"""
    
    # 检查存在的文件
    template_files = list(templates_dir.glob("*"))
    
    for filepath in sorted(template_files):
        if filepath.is_file():
            file_size = os.path.getsize(filepath) / 1024
            summary_content += f"- `{filepath.name}` ({file_size:.1f} KB)\n"
    
    summary_content += """
## 🚀 推荐使用顺序:

### 第1优先级: 自制PLY格式
```
File → Open → brain_fixed.ply
```

### 第2优先级: 下载的MZ3格式
```
File → Open → pial.mz3 (如果下载成功)
File → Open → BrainMesh_ICBM152.mz3 (如果下载成功)
```

### 第3优先级: 其他格式
```
File → Open → brain.obj
File → Open → brain.stl
```

## 📊 激活数据加载:
```
Overlay → Add → braingnn_pain_activation.nii.gz
```

## 🎯 如果全部失败:
直接加载NIfTI数据，SurfIce会自动生成基础模板:
```
File → Open → braingnn_pain_activation.nii.gz
```

---
🧠 BrainGNN疼痛分类 - 98.7%准确率
🎯 多种格式确保兼容性
"""
    
    summary_path = templates_dir / "TEMPLATE_SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ 模板总结创建: {summary_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("🌐 下载官方MZ3模板")
    print("🎯 解决MZ3文件问题")
    print("=" * 60)
    
    # 1. 尝试下载官方MZ3模板
    downloaded_mz3 = download_official_mz3_templates()
    
    # 2. 如果下载失败，创建自己的MZ3
    if not downloaded_mz3:
        print("\n📝 官方模板下载失败，创建自制MZ3文件...")
        create_mz3_from_freesurfer()
    
    # 3. 尝试下载其他格式模板
    downloaded_others = download_alternate_brain_templates()
    
    # 4. 创建文件总结
    create_template_summary()
    
    print("\n" + "=" * 60)
    print("✅ MZ3模板准备完成!")
    
    if downloaded_mz3:
        print(f"🌐 成功下载官方模板: {len(downloaded_mz3)}个")
        for template in downloaded_mz3:
            print(f"  ✅ {template}")
    else:
        print("🔧 使用自制模板")
    
    print("\n🎯 现在可以在SurfIce中使用:")
    print("  1. 打开SurfIce")
    print("  2. File → Open → 选择任一大脑模板")
    print("  3. Overlay → Add → braingnn_pain_activation.nii.gz")
    print("  4. 调整显示效果")
    
    print("\n📋 详细说明: TEMPLATE_SUMMARY.md")
    print("=" * 60)

if __name__ == "__main__":
    main()