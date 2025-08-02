# 🧠 SurfIce 下载和安装指南

## 🚀 快速下载链接

### macOS (推荐)
**直接下载链接**: [Surfice_macOS.dmg](https://github.com/rordenlab/surfice/releases/latest/download/Surfice_macOS.dmg)

### 其他系统
- **Windows**: [surfice_windows.zip](https://github.com/rordenlab/surfice/releases/latest/download/surfice_windows.zip)
- **Linux**: [surfice_linux.zip](https://github.com/rordenlab/surfice/releases/latest/download/surfice_linux.zip)

## 📥 安装步骤

### macOS 安装
1. 下载 `Surfice_macOS.dmg`
2. 双击打开DMG文件
3. 将SurfIce拖拽到Applications文件夹
4. 打开应用程序，允许来自未认证开发者的软件

### 打开权限设置 (macOS)
如果遇到安全提示：
1. 系统偏好设置 → 安全性与隐私
2. 点击"仍要打开" 或 "允许"
3. 或者使用命令行：`sudo xattr -rd com.apple.quarantine /Applications/SurfIce.app`

## 🎯 加载BrainGNN数据

### 方法1: 自动脚本加载 (推荐)
1. 打开SurfIce应用
2. 菜单: `Scripting` → `Load Script`
3. 选择: `scripts/load_braingnn_pain.txt`
4. 所有数据将自动加载！

### 方法2: 手动加载
1. **加载大脑模板**: `Mesh` → `Open` → 选择标准脑模板
2. **加载激活图**: `Overlay` → `Open` → `overlays/braingnn_pain_activation.nii.gz`
3. **加载脑区节点**: `Node` → `Open` → `nodes/braingnn_pain_nodes.node`
4. **加载网络连接**: `Edge` → `Open` → `edges/braingnn_pain_edges.edge`

## 🎨 可视化调整

### 颜色设置
- **激活图颜色**: RdBu (红-蓝色谱)
- **阈值范围**: -0.6 到 0.6
- **透明度**: 70-80%

### 预设视角
- **左侧视图**: Azimuth 270°, Elevation 0°
- **右侧视图**: Azimuth 90°, Elevation 0°
- **顶部视图**: Azimuth 0°, Elevation 90°
- **正面视图**: Azimuth 0°, Elevation 0°

## 💾 保存图像
使用菜单 `File` → `Save Bitmap` 保存高质量图像

## 🆘 需要帮助？
- 官方文档: https://www.nitrc.org/projects/surfice/
- GitHub: https://github.com/rordenlab/surfice
- 使用问题请查看本文件夹中的 `README.md`

---
🧠 **BrainGNN Pain Classification - 98.7% Accuracy**
🎯 **Professional Neuroimaging Visualization**