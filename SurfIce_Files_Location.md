# 🧠 SurfIce文件位置指南

## 📁 文件确实存在！正确路径如下：

### 🧠 大脑模板文件：
```
/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_templates/mni152.mz3
/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_templates/simple_brain.ply
```

### 📊 激活数据文件：
```
/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_visualization/braingnn_pain_activation.nii.gz
```

### 📖 或者这个版本：
```
/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_data/overlays/braingnn_pain_activation.nii.gz
```

## 🚀 在SurfIce中使用的完整步骤：

### 步骤1: 加载大脑模板
1. 打开SurfIce
2. **Mesh** → **Load Mesh**
3. 导航到：`/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_templates/`
4. 选择：`mni152.mz3`

### 步骤2: 加载激活数据
1. **Overlay** → **Add Overlay**
2. 导航到：`/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_visualization/`
3. 选择：`braingnn_pain_activation.nii.gz`

## 💡 快速查找技巧：

### 在Finder中快速定位：
1. 打开Finder
2. 按 Cmd+Shift+G
3. 输入：`/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/`
4. 您会看到两个文件夹：
   - `surfice_templates/` (包含大脑模板)
   - `surfice_visualization/` (包含激活数据)

## 🎯 最简单的方法：

### 方法1: 直接拖拽
1. 在Finder中打开这些文件夹
2. 将文件直接拖拽到SurfIce窗口

### 方法2: 使用完整路径
- 在SurfIce文件选择对话框中，直接输入完整路径

## 📋 文件检查清单：

- ✅ `mni152.mz3` (3.1 MB) - 在 surfice_templates/
- ✅ `simple_brain.ply` (85 KB) - 在 surfice_templates/  
- ✅ `braingnn_pain_activation.nii.gz` (197 KB) - 在 surfice_visualization/
- ✅ 备用版本在 surfice_data/overlays/

## 🔍 如果还是找不到：

尝试在终端中确认：
```bash
ls -la /Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_templates/
ls -la /Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures/surfice_visualization/
```

---
🧠 **所有文件都在您的电脑上！**
📂 **只需要知道正确的路径**