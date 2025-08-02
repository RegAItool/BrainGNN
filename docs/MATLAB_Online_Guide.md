# MATLAB在线版BrainNet Viewer使用指南

## 🎯 推荐方案：MATLAB在线版

**优点：**
- ✅ 无需下载安装
- ✅ 免费使用
- ✅ 功能完整
- ✅ 专业可视化
- ✅ 立即可用

## 🚀 使用步骤

### 1. 访问MATLAB在线版
访问：https://matlab.mathworks.com/

### 2. 上传文件
将以下文件上传到MATLAB在线版：
- `bridge_nodes.node` (节点文件)
- `bridge_edges.edge` (边文件)
- `matlab_online_script.m` (脚本文件)

### 3. 运行脚本
在MATLAB在线版中运行：
```matlab
run('matlab_online_script.m')
```

### 4. 下载结果
脚本会自动生成 `matlab_online_brainnet.png` 文件，您可以下载保存。

## 📊 预期结果

运行后将生成包含以下内容的可视化：
- **3D大脑网络图** - 显示ROI在3D空间中的分布
- **2D投影图** - 大脑网络的2D投影
- **重要性分布直方图** - ROI重要性的统计分布
- **连接强度分布** - 网络连接强度的统计

## 🎨 可视化特点

- **ROI重要性** - 用颜色和大小表示
- **网络连接** - 显示脑区间的功能连接
- **3D空间** - 真实的大脑解剖位置
- **专业质量** - 适合论文和报告

## 📈 数据信息

您的BrainGNN模型数据：
- **ROI总数**: 100个脑区
- **最大重要性**: 0.5573
- **平均重要性**: 0.5549
- **坐标范围**: X[-45.25, 44.90], Y[-37.76, 49.20], Z[-40.56, 42.59]

## 🔧 备选方案

### 方案A：本地MATLAB
如果您想下载MATLAB，可以使用 `full_brainnet_script.m` 脚本。

### 方案B：BrainNet Viewer GUI
在MATLAB中运行：
```matlab
addpath('./imports/BrainNetViewer_20191031');
BrainNet;
```

然后在GUI中手动加载：
- 节点文件：`bridge_nodes.node`
- 边文件：`bridge_edges.edge`

## 🎯 优势对比

| 方案 | 安装难度 | 可视化质量 | 专业性 | 推荐度 |
|------|----------|------------|--------|--------|
| MATLAB在线版 | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 本地MATLAB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Python版本 | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

## 📝 使用建议

1. **首选MATLAB在线版** - 最简单快捷
2. **如果需要更专业的结果** - 考虑下载MATLAB
3. **如果只是快速查看** - Python版本也够用

---

**🎉 现在您可以在MATLAB在线版中生成专业的大脑网络可视化了！** 