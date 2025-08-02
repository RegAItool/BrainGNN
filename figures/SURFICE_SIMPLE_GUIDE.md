# 🧠 SurfIce简单使用指南 - BrainGNN疼痛可视化

## 🎯 找到的解决方案！

我们已经为您准备好了：
- ✅ **大脑模板**: `surfice_templates/mni152.mz3`
- ✅ **激活数据**: `surfice_visualization/braingnn_pain_activation.nii.gz`

## 🚀 3步骤加载 (超简单!)

### 步骤1: 打开SurfIce
- 双击SurfIce应用图标

### 步骤2: 加载大脑模板
- **Mesh** → **Load Mesh** 
- 选择: `surfice_templates/mni152.mz3`
- 或者选择: `surfice_templates/simple_brain.ply`

### 步骤3: 加载疼痛激活数据
- **Overlay** → **Add Overlay**
- 选择: `surfice_visualization/braingnn_pain_activation.nii.gz`

## 🎨 调整显示效果

### 颜色设置:
- **Overlay** → **Color** → 选择 "Hot-Cold" 或 "Red-Blue"
- 设置阈值: Min = -0.6, Max = 0.6

### 透明度:
- **Overlay** → **Opacity** → 设置为 70-80%

## 📁 文件位置提醒

```
您的桌面/BrainGNN_Pytorch-main/figures/
├── surfice_templates/
│   ├── mni152.mz3           ← 大脑模板 (步骤2用)
│   └── simple_brain.ply     ← 备用模板
└── surfice_visualization/
    └── braingnn_pain_activation.nii.gz  ← 激活数据 (步骤3用)
```

## 🎯 如果还是找不到模板...

### 方法A: 在SurfIce中查找内置模板
1. 打开SurfIce
2. 查看启动界面是否有 "Examples" 或 "Templates"
3. 选择任何大脑相关的模板

### 方法B: 跳过模板，直接查看激活
1. **File** → **Open** → 直接选择 `braingnn_pain_activation.nii.gz`
2. SurfIce可能会自动加载基础模板

### 方法C: 使用我们生成的简单模板
- 使用 `simple_brain.ply` (我们创建的简化大脑)

## 🧠 您将看到什么

- 🔴 **红色区域**: 疼痛时激活增强的脑区
  - 小脑、枕叶、海马旁回、杏仁核
  
- 🔵 **蓝色区域**: 疼痛时激活减少的脑区  
  - 前额叶、运动感觉皮层、壳核

- 📊 **分类准确率**: 98.7%
- 🎯 **14个关键脑区**

## ⚡ 最简单的方法

如果上面都不行，试试这个：
1. 打开SurfIce
2. 直接拖拽 `braingnn_pain_activation.nii.gz` 到SurfIce窗口
3. 看看会发生什么！

## 🆘 需要帮助？

如果SurfIce还是有问题，我们还有其他优秀的可视化：
- `professional_human_brain.html` (浏览器3D可视化)
- `real_brain_shape.html` (交互式脑图)

这些都可以直接在浏览器中查看！

---
🧠 **BrainGNN Pain Classification - 98.7% Accuracy**  
🎯 **Professional Neuroscience Visualization**