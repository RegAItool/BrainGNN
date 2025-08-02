# BrainNet Viewer 快速开始指南

## 🎉 恭喜！所有文件都已准备就绪

您的BrainGNN模型训练已完成，BrainNet Viewer文件也已成功生成。现在可以创建专业的大脑网络可视化了！

## 📁 生成的文件

✅ **节点文件**: `bridge_nodes.node` (679 bytes) - 包含100个ROI的3D坐标和重要性
✅ **边文件**: `bridge_edges.edge` (2400 bytes) - 包含ROI之间的连接关系  
✅ **MATLAB脚本**: `simple_brainnet_script.m` (3250 bytes) - 自动生成可视化
✅ **BrainNet Viewer**: `./imports/BrainNetViewer_20191031/` - 专业大脑可视化工具

## 🧠 数据信息

- **ROI总数**: 100个脑区
- **最大重要性**: 0.5573
- **平均重要性**: 0.5549
- **坐标范围**: X[-45.25, 44.90], Y[-37.76, 49.20], Z[-40.56, 42.59]

## 🚀 使用方法

### 方法1: 自动脚本 (推荐)

1. **打开MATLAB**
2. **切换到工作目录**:
   ```matlab
   cd('/Users/hanyu/Documents/BrainGNN_Pytorch-main')
   ```
3. **运行脚本**:
   ```matlab
   run('simple_brainnet_script.m')
   ```

### 方法2: BrainNet GUI

1. **添加BrainNet路径**:
   ```matlab
   addpath('./imports/BrainNetViewer_20191031');
   ```
2. **启动BrainNet GUI**:
   ```matlab
   BrainNet;
   ```
3. **在GUI中加载文件**:
   - 节点文件: `bridge_nodes.node`
   - 边文件: `bridge_edges.edge`

## 📈 预期结果

运行后将生成:
- `brainnet_simple_visualization.png` - 专业的大脑网络可视化
- `brainnet_3d_scatter.png` - 3D散点图

## 🎯 BrainNet Viewer 优势

✅ **真实大脑形状** - 使用解剖学准确的大脑模板  
✅ **专业可视化** - 专为大脑网络设计  
✅ **多种视角** - 支持不同角度的可视化  
✅ **高质量输出** - 适合论文和报告  
✅ **标准化** - 符合神经影像学标准  
✅ **交互式** - 支持GUI操作  

## 🐛 故障排除

### 问题1: BrainNet Viewer未找到
**解决**: 
```matlab
addpath('./imports/BrainNetViewer_20191031');
```

### 问题2: 文件不存在
**解决**: 确保在正确目录中运行
```matlab
pwd  % 检查当前目录
ls   % 列出文件
```

### 问题3: MATLAB未安装
**解决**: 
- 安装MATLAB
- 或使用在线MATLAB服务
- 或使用Octave (开源替代)

## 📊 模型性能回顾

您的BrainGNN模型训练结果:
- **测试准确率**: 52.17%
- **训练准确率**: 83.41%
- **最佳模型**: 保存在 `./model/` 目录
- **训练日志**: 保存在 `./log/` 目录

## 🎨 可视化特点

- **ROI重要性**: 用颜色和大小表示
- **网络连接**: 显示脑区间的功能连接
- **3D空间**: 真实的大脑解剖位置
- **专业质量**: 适合学术论文和报告

## 📝 下一步

1. 在MATLAB中运行可视化脚本
2. 调整参数以获得最佳效果
3. 保存高质量图像用于论文
4. 分析重要ROI的神经解剖学意义

---

**🎉 现在您可以生成专业的大脑网络可视化了！**

*生成时间: 2025-07-05 12:19:42* 