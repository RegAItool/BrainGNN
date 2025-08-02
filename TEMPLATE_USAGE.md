# 🧠 SurfIce大脑模板使用指南

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
