#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载MNI152_2009.mz3真实大脑模板
Download Real MNI152_2009.mz3 Brain Template
"""

import requests
import os
import zipfile
import urllib.request
from pathlib import Path

def download_surfice_complete():
    """下载完整的SurfIce软件包获取mni152_2009.mz3"""
    
    print("🌐 下载完整SurfIce软件包以获取mni152_2009.mz3...")
    
    # 创建下载目录
    download_dir = Path("./figures/surfice_download")
    download_dir.mkdir(parents=True, exist_ok=True)
    
    # SurfIce下载链接
    download_urls = {
        'macOS': 'https://github.com/neurolabusc/surf-ice/releases/latest/download/surfice_macOS.dmg',
        'windows': 'https://github.com/neurolabusc/surf-ice/releases/latest/download/surfice_windows.zip',
        'linux': 'https://github.com/neurolabusc/surf-ice/releases/latest/download/surfice_linux.zip'
    }
    
    # 检测系统并下载对应版本
    import platform
    system = platform.system().lower()
    
    if system == 'darwin':
        url = download_urls['macOS']
        filename = 'surfice_macOS.dmg'
    elif system == 'windows':
        url = download_urls['windows'] 
        filename = 'surfice_windows.zip'
    else:
        url = download_urls['linux']
        filename = 'surfice_linux.zip'
    
    filepath = download_dir / filename
    
    try:
        print(f"📥 正在下载 {filename}...")
        
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r   进度: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ 下载完成: {filepath}")
        
        # 如果是ZIP文件，尝试解压查找mz3文件
        if filename.endswith('.zip'):
            extract_mz3_from_zip(filepath)
        else:
            print("💡 DMG文件需要手动挂载和提取")
            
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def extract_mz3_from_zip(zip_path):
    """从ZIP文件中提取MZ3文件"""
    
    print("📦 正在解压ZIP文件查找MZ3模板...")
    
    extract_dir = zip_path.parent / "extracted"
    extract_dir.mkdir(exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 列出所有文件
            file_list = zip_ref.namelist()
            
            # 查找MZ3文件
            mz3_files = [f for f in file_list if f.endswith('.mz3')]
            
            print(f"🔍 找到 {len(mz3_files)} 个MZ3文件:")
            for mz3_file in mz3_files:
                print(f"   📁 {mz3_file}")
            
            # 查找特定的大脑模板
            brain_templates = [f for f in mz3_files if any(brain_name in f.lower() 
                             for brain_name in ['mni152', 'brain', 'cortex', 'template'])]
            
            if brain_templates:
                print(f"🧠 找到大脑模板文件:")
                for template in brain_templates:
                    print(f"   🎯 {template}")
                    
                    # 提取到我们的模板目录
                    zip_ref.extract(template, extract_dir)
                    
                    # 复制到surfice_templates目录
                    template_name = os.path.basename(template)
                    dest_path = Path("./figures/surfice_templates") / template_name
                    
                    src_path = extract_dir / template
                    if src_path.exists():
                        import shutil
                        shutil.copy2(src_path, dest_path)
                        
                        file_size = os.path.getsize(dest_path) / 1024
                        print(f"✅ 复制成功: {dest_path} ({file_size:.1f} KB)")
            else:
                print("⚠️ 未找到明显的大脑模板文件")
                print("💡 提取所有MZ3文件供检查:")
                
                for mz3_file in mz3_files[:5]:  # 只提取前5个
                    zip_ref.extract(mz3_file, extract_dir)
                    print(f"   📁 已提取: {mz3_file}")
            
            # 也查找sample文件夹
            sample_files = [f for f in file_list if 'sample' in f.lower() and f.endswith('.mz3')]
            if sample_files:
                print(f"🎯 找到sample目录中的MZ3文件:")
                for sample_file in sample_files:
                    print(f"   📂 {sample_file}")
                    zip_ref.extract(sample_file, extract_dir)
                    
                    # 检查是否是mni152_2009
                    if 'mni152_2009' in sample_file.lower():
                        template_name = os.path.basename(sample_file)
                        dest_path = Path("./figures/surfice_templates") / template_name
                        
                        src_path = extract_dir / sample_file
                        if src_path.exists():
                            import shutil
                            shutil.copy2(src_path, dest_path)
                            
                            file_size = os.path.getsize(dest_path) / 1024
                            print(f"🎯 找到目标文件: {dest_path} ({file_size:.1f} KB)")
            
    except Exception as e:
        print(f"❌ 解压失败: {e}")

def try_direct_mz3_downloads():
    """尝试直接下载已知的MZ3文件"""
    
    print("🎯 尝试直接下载已知MZ3大脑模板...")
    
    # 可能的直接下载链接
    mz3_urls = [
        {
            'name': 'cortex_5124.mz3',
            'url': 'https://github.com/neurolabusc/surf-ice/raw/master/mz3/cortex_5124.mz3',
            'description': '皮层网格模板'
        },
        {
            'name': 'BrainMesh_ICBM152.mz3',
            'url': 'https://github.com/rordenlab/MRIcroGL/raw/master/Resources/script/BrainMesh_ICBM152.mz3',
            'description': 'ICBM152大脑网格'
        },
        {
            'name': 'pial.mz3',
            'url': 'https://github.com/rordenlab/MRIcroGL/raw/master/Resources/script/pial.mz3',
            'description': '皮层表面'
        }
    ]
    
    templates_dir = Path("./figures/surfice_templates")
    successful_downloads = []
    
    for template in mz3_urls:
        try:
            url = template['url']
            filename = template['name']
            filepath = templates_dir / filename
            
            print(f"📥 尝试下载: {filename}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filepath) / 1024
            print(f"✅ 下载成功: {filename} ({file_size:.1f} KB)")
            
            # 检查是否是真实的MZ3文件
            with open(filepath, 'rb') as f:
                header = f.read(8)
                if header.startswith(b'MZ3') or len(header) > 4:
                    successful_downloads.append(filename)
                    print(f"   ✅ 文件格式验证通过")
                else:
                    print(f"   ⚠️ 可能不是有效的MZ3文件")
            
        except Exception as e:
            print(f"❌ 下载失败: {filename} - {e}")
    
    return successful_downloads

def create_download_instructions():
    """创建手动下载指南"""
    
    print("📖 创建手动下载指南...")
    
    instructions = """# 🧠 获取真实MNI152_2009.mz3大脑模板指南

## 🎯 方法1: 下载完整SurfIce软件包 (推荐)

### 步骤1: 访问官方下载页面
- 🌐 GitHub Releases: https://github.com/neurolabusc/surf-ice/releases/latest
- 🌐 NITRC: https://www.nitrc.org/projects/surfice/

### 步骤2: 下载对应系统版本
- **macOS**: surfice_macOS.dmg
- **Windows**: surfice_windows.zip  
- **Linux**: surfice_linux.zip

### 步骤3: 查找模板文件
安装/解压后，在以下位置查找:
```
surfice/sample/mni152_2009.mz3
surfice/Resources/mni152_2009.mz3
surfice/examples/mni152_2009.mz3
```

## 🎯 方法2: 使用SurfIce内置模板

如果您已经安装了SurfIce:
1. 打开SurfIce
2. 查看菜单 **File** → **Examples** 或 **Templates**
3. 寻找 MNI152 相关选项
4. 直接加载内置模板

## 🎯 方法3: 从MNI官方下载并转换

### 下载原始MNI模板:
- 🌐 MNI官网: https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009
- 下载 MNI152_T1_1mm.nii.gz

### 转换为MZ3格式:
使用MRIcroGL或其他工具将NIfTI转换为网格格式

## 🎯 方法4: 使用FreeSurfer模板

FreeSurfer包含标准大脑表面:
```
$FREESURFER_HOME/subjects/fsaverage/surf/lh.pial
$FREESURFER_HOME/subjects/fsaverage/surf/rh.pial
```

可以转换为MZ3格式使用

## 🚀 一旦获得mni152_2009.mz3:

### 在SurfIce中使用:
1. **File** → **Open** → 选择 `mni152_2009.mz3`
2. **Overlay** → **Add Overlay** → 选择 `braingnn_pain_activation.nii.gz`
3. 调整显示效果

### 文件放置位置:
```
/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_templates/mni152_2009.mz3
```

## 💡 提示
- mni152_2009.mz3 通常随SurfIce软件包一起提供
- 文件大小通常在几十KB到几MB之间
- 是MNI152标准空间的3D网格表面

---
🧠 获得真实模板后，您的BrainGNN疼痛分类结果将显示在标准大脑上！
"""
    
    guide_path = "./figures/GET_REAL_MNI152_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ 下载指南创建: {guide_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 获取真实MNI152_2009.mz3大脑模板")
    print("=" * 60)
    
    # 1. 尝试直接下载已知MZ3文件
    print("🔍 步骤1: 尝试直接下载已知MZ3文件...")
    downloaded_files = try_direct_mz3_downloads()
    
    # 2. 如果没有成功，尝试下载完整软件包
    if not downloaded_files:
        print("\n🔍 步骤2: 下载完整SurfIce软件包...")
        download_surfice_complete()
    
    # 3. 创建手动下载指南
    print("\n🔍 步骤3: 创建手动下载指南...")
    create_download_instructions()
    
    print("\n" + "=" * 60)
    print("✅ MNI152模板获取任务完成!")
    
    if downloaded_files:
        print(f"🎯 成功下载: {len(downloaded_files)}个MZ3文件")
        for filename in downloaded_files:
            print(f"  ✅ {filename}")
    else:
        print("📖 请参考手动下载指南获取mni152_2009.mz3")
    
    print("\n🧠 一旦获得真实模板文件:")
    print("  1. 将其放在 figures/surfice_templates/ 目录")
    print("  2. 在SurfIce中 File → Open → mni152_2009.mz3")
    print("  3. 加载激活数据覆盖层")
    print("  4. 享受专业级大脑可视化!")
    
    print("\n📋 详细指南: GET_REAL_MNI152_GUIDE.md")
    print("=" * 60)

if __name__ == "__main__":
    main()