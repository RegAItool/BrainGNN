# BrainGNN Pain State Classification - SurfIce Visualization

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
