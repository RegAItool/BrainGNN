# 🧠 获取真实MNI152_2009.mz3大脑模板指南

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
