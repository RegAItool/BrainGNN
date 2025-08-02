# BrainNet Viewer 使用说明

## 🧠 概述

BrainNet Viewer 是一个专业的MATLAB工具箱，用于可视化大脑网络。我们已经为你准备好了所有必要的文件，可以直接在MATLAB中使用BrainNet Viewer绘制真实的大脑形状。

## 📁 生成的文件

### 数据文件
- `bridge_nodes.node` - 节点文件（包含ROI坐标和重要性）
- `bridge_edges.edge` - 边文件（连接矩阵）
- `brainnet_data_info.json` - 数据信息文件

### MATLAB脚本
- `simple_brainnet_script.m` - 简单脚本（推荐使用）
- `brainnet_bridge.m` - 桥接脚本
- `brainnet_visualization.m` - 基础脚本
- `advanced_brainnet_visualization.m` - 高级脚本

## 🚀 使用方法

### 方法1: 运行简单脚本（推荐）

1. 打开MATLAB
2. 切换到工作目录：`cd('/Users/hanyu/Documents/BrainGNN_Pytorch-main')`
3. 运行脚本：
   ```matlab
   run('simple_brainnet_script.m')
   ```

### 方法2: 使用BrainNet GUI

1. 打开MATLAB
2. 切换到工作目录
3. 运行：
   ```matlab
   addpath('./imports/BrainNetViewer_20191031');
   BrainNet;
   ```
4. 在GUI中手动加载：
   - 节点文件：`bridge_nodes.node`
   - 边文件：`bridge_edges.edge`

### 方法3: 命令行运行

```bash
matlab -batch "run('simple_brainnet_script.m')"
```

## 📊 数据说明

### 节点文件格式 (bridge_nodes.node)
```
x    y    z    size    color
```
- x, y, z: ROI的3D坐标
- size: 节点大小（基于重要性）
- color: 颜色值（基于重要性）

### 边文件格式 (bridge_edges.edge)
```
20x20的连接矩阵，表示ROI之间的连接强度
```

## 🎨 可视化选项

### 视角设置
- `[0, 0, 1]` - 背侧视图
- `[1, 0, 0]` - 外侧视图
- `[0, 1, 0]` - 前侧视图

### 颜色映射
- 使用热力图颜色映射
- 重要性越高，颜色越红
- 重要性越低，颜色越蓝

### 节点大小
- 基于ROI重要性自动调整
- 重要性越高，节点越大

## 🔧 自定义设置

### 修改视角
在脚本中修改 `cfg.views` 参数：
```matlab
cfg.views = [0, 0, 1];  % 背侧视图
% 或
cfg.views = [1, 0, 0];  % 外侧视图
```

### 修改节点大小
```matlab
cfg.node_size = 2;  % 调整节点大小
```

### 修改边大小
```matlab
cfg.edge_size = 1;  % 调整边大小
```

## 📈 预期结果

运行脚本后，你将得到：

1. **BrainNet Viewer可视化** (`brainnet_simple_visualization.png`)
   - 真实的大脑形状
   - ROI重要性用颜色和大小表示
   - 专业的网络可视化

2. **3D散点图** (`brainnet_3d_scatter.png`)
   - 3D空间中的ROI分布
   - 重要性用颜色表示

## 🐛 故障排除

### 问题1: BrainNet Viewer未找到
**解决方案：**
```matlab
addpath('./imports/BrainNetViewer_20191031');
```

### 问题2: 文件不存在
**解决方案：**
确保在正确的目录中运行脚本：
```matlab
cd('/Users/hanyu/Documents/BrainGNN_Pytorch-main');
```

### 问题3: MATLAB未安装
**解决方案：**
- 安装MATLAB
- 或使用在线MATLAB服务

## 📋 数据信息

- **ROI数量**: 100个
- **显示ROI**: 前20个最重要的ROI
- **最大重要性**: 基于模型输出的最大值
- **数据集**: ABIDE resting-state fMRI
- **模型**: BrainGNN with Graph Pooling

## 🎯 优势

使用BrainNet Viewer的优势：

1. **真实大脑形状**: 使用解剖学准确的大脑模板
2. **专业可视化**: 专为大脑网络设计
3. **多种视角**: 支持不同角度的可视化
4. **高质量输出**: 适合论文和报告
5. **标准化**: 符合神经影像学标准

## 📞 支持

如果遇到问题，请检查：

1. MATLAB是否正确安装
2. BrainNet Viewer路径是否正确
3. 数据文件是否存在
4. 工作目录是否正确

---

**🎉 现在你可以使用BrainNet Viewer生成专业的大脑网络可视化了！** 