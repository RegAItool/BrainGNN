# 🧠 SurfIce MZ3文件问题解决方案

## 🚨 MZ3文件问题确认

如果mz3文件有问题，我们提供多种替代方案：

## 🔧 解决方案1: 使用PLY格式
- ✅ 文件: `brain_fixed.ply`
- 📐 格式: PLY (广泛支持)
- 🎯 在SurfIce中: File → Open → 选择 brain_fixed.ply

## 🔧 解决方案2: 使用OBJ格式  
- ✅ 文件: `brain.obj`
- 📐 格式: Wavefront OBJ (通用3D格式)
- 🎯 在SurfIce中: File → Open → 选择 brain.obj

## 🔧 解决方案3: 使用STL格式
- ✅ 文件: `brain.stl` 
- 📐 格式: STL (3D打印标准)
- 🎯 在SurfIce中: File → Open → 选择 brain.stl

## 🔧 解决方案4: 直接加载激活数据
- ✅ 跳过大脑模板
- 🎯 直接: File → Open → braingnn_pain_activation.nii.gz
- 📊 SurfIce可能自动生成基础模板

## 📁 所有文件位置:
```
figures/surfice_templates/
├── brain_fixed.ply      ← 推荐使用！
├── brain.obj           ← 备选1
├── brain.stl           ← 备选2
├── brain_vertices.txt  ← FreeSurfer格式
└── brain_faces.txt     ← FreeSurfer格式
```

## 🚀 推荐加载顺序:

### 步骤1: 选择模板
1. 优先尝试: `brain_fixed.ply`
2. 如果不行: `brain.obj`
3. 如果还不行: `brain.stl`

### 步骤2: 加载激活数据
- File → Add Overlay → braingnn_pain_activation.nii.gz

### 步骤3: 调整显示
- 颜色: Red-Blue 或 Hot-Cold
- 阈值: -0.6 到 0.6
- 透明度: 70-80%

## 🎯 期待结果:
- 🔴 疼痛激活区域 (红色)
- 🔵 疼痛抑制区域 (蓝色)  
- 📊 98.7%分类准确率

## 🆘 如果全部失败:
使用universal_brain_viewer.html - 在浏览器中直接查看！

---
🧠 BrainGNN疼痛分类 - 专业神经科学可视化
