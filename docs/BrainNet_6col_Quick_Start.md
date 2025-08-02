# BrainNet Viewer 6列格式快速开始指南

## 🎉 恭喜！已生成标准的6列格式BrainNet Viewer文件

您的BrainGNN模型训练已完成，现在有了**标准的6列格式**BrainNet Viewer文件，这是最推荐使用的格式！

## 📁 生成的文件

✅ **节点文件**: `brainnet_nodes_100_6col.node` (100行, 6列) - 标准6列格式
✅ **边文件**: `brainnet_edges_100.edge` (100x100矩阵) - 真实FC矩阵
✅ **MATLAB脚本**: `matlab_online_script_100_6col.m` - 6列格式可视化脚本

## 📋 6列格式说明

### Node文件格式 (brainnet_nodes_100_6col.node)
```
x       y       z       size    color   module
```

| 列号 | 名称 | 说明 | 示例值 |
|------|------|------|--------|
| 1 | x | X坐标 (mm, MNI空间) | -22.583 |
| 2 | y | Y坐标 (mm, MNI空间) | 79.354 |
| 3 | z | Z坐标 (mm, MNI空间) | 59.759 |
| 4 | size | 节点大小 (半径) | 13.360 |
| 5 | color | 颜色值 (0-1) | 1.000000 |
| 6 | module | 模块编号 (1-6) | 4 |

### 数据特点
- **坐标范围**: MNI标准空间 (X[-90,90], Y[-126,90], Z[-72,108])
- **节点大小**: 13.319-13.360 (基于重要性)
- **颜色值**: 0-1 (归一化的重要性分数)
- **模块分布**: 6个模块 (基于FC相似性聚类)
  - Module 1: 25个节点
  - Module 2: 13个节点  
  - Module 3: 20个节点
  - Module 4: 15个节点
  - Module 5: 17个节点
  - Module 6: 10个节点

## 🚀 使用方法

### 方法1: MATLAB在线版 (推荐)
1. **访问**: https://matlab.mathworks.com/
2. **上传文件**:
   - `brainnet_nodes_100_6col.node`
   - `brainnet_edges_100.edge`
   - `matlab_online_script_100_6col.m`
3. **运行脚本**:
   ```matlab
   run('matlab_online_script_100_6col.m')
   ```
4. **下载结果**: `matlab_online_brainnet_100_6col.png`

### 方法2: 本地MATLAB + BrainNet Viewer
```matlab
% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 使用BrainNet_MapCfg
BrainNet_MapCfg('brainnet_nodes_100_6col.node', 'brainnet_edges_100.edge');
```

## 🎨 可视化内容

运行后将生成包含8个子图的综合可视化：

1. **3D ROI分布** (按模块着色)
2. **功能连接矩阵** (热图)
3. **ROI重要性分布** (直方图)
4. **模块分布** (饼图)
5. **2D投影** (按重要性着色)
6. **连接强度分布** (直方图)
7. **节点大小分布** (直方图)
8. **模块内平均连接强度** (柱状图)

## 📊 数据统计

- **节点总数**: 100个ROI
- **最大重要性**: 1.0000
- **平均重要性**: 0.5549
- **连接矩阵**: 100x100, 9900个非零元素
- **连接强度范围**: [0.000000, 0.211666]
- **模块数量**: 6个功能模块

## 🔧 优势

✅ **标准格式**: 符合BrainNet Viewer官方推荐
✅ **模块分析**: 支持社区检测和模块网络分析
✅ **真实数据**: 基于ABIDE真实FC矩阵
✅ **重要性映射**: 与BrainGNN模型输出一致
✅ **专业质量**: 适合论文和报告

## 📈 预期结果

运行后将获得专业的大脑网络可视化，包括：
- 按功能模块着色的3D大脑网络
- 真实的功能连接强度分布
- ROI重要性在空间上的分布
- 模块化网络结构分析
- 高质量图像，适合学术发表

现在您拥有了最标准的BrainNet Viewer文件格式，可以生成最专业的大脑网络可视化！🎯 