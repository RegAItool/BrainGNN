# BrainNet Viewer - 脑区激活图完整指南

## 🎯 目标
制作类似论文的彩色脑区激活图，使用`.mesh` + `.dpv`格式替代`.node`/`.edge`格式。

## 📁 生成的文件

### ✅ 基础版本文件
- `brain_activation.txt` - 脑区重要性分数 (100×1)
- `brain_activation.dpv` - 表面顶点激活数据 (81924×1)
- `matlab_activation_map.m` - MATLAB可视化脚本
- `activation_map_settings.m` - 自动设置脚本

### ✅ 高级版本文件
- `advanced_activation.txt` - 精确ROI重要性分数
- `advanced_activation.dpv` - 精确表面顶点激活数据
- `roi_coordinates.txt` - ROI坐标和重要性信息
- `matlab_advanced_activation.m` - 高级MATLAB脚本
- `advanced_activation_settings.m` - 高级设置脚本

## 🧠 数据格式说明

### DPV格式 (Data Per Vertex)
- **文件**: `.dpv`文件
- **内容**: 每个表面顶点的激活值
- **大小**: 81924个顶点 (对应BrainMesh_ICBM152.nv)
- **范围**: 0.0 - 1.0 (标准化激活强度)

### 激活映射原理
1. **ROI坐标**: 使用真实ROI的MNI坐标
2. **距离计算**: 计算每个表面顶点到ROI的距离
3. **高斯核**: 使用高斯核函数进行平滑激活
4. **重要性加权**: 根据ROI重要性分数加权激活

## 🚀 使用方法

### 方法1：MATLAB脚本自动启动

**基础版本：**
```matlab
% 在MATLAB中运行
run('matlab_activation_map.m')
```

**高级版本：**
```matlab
% 在MATLAB中运行
run('matlab_advanced_activation.m')
```

### 方法2：手动在BrainNet Viewer中加载

1. 打开BrainNet Viewer
2. 加载文件：
   - **Surface**: `BrainMesh_ICBM152.nv`
   - **Data**: `brain_activation.dpv` 或 `advanced_activation.dpv`

### 方法3：命令行启动

**基础版本：**
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'brain_activation.dpv')
```

**高级版本：**
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'advanced_activation.dpv')
```

## ⚙️ 推荐设置

### 激活图设置
- **Color map**: Jet 或 Hot (适合激活图)
- **Threshold**: 0.1-0.3 (基础版本) / 0.3-0.5 (高级版本)
- **Transparency**: 0.3-0.5
- **Lighting**: Phong
- **View**: 选择Lateral/Medial/Full视角

### 颜色映射选项
- **Jet**: 蓝色(低) → 绿色 → 黄色 → 红色(高)
- **Hot**: 黑色(低) → 红色 → 黄色 → 白色(高)
- **Cool**: 青色 → 蓝色 → 紫色
- **Parula**: MATLAB默认颜色映射

## 📊 数据统计对比

| 指标 | 基础版本 | 高级版本 |
|------|----------|----------|
| 激活顶点数 | ~24,577 | ~24,577 |
| 激活强度范围 | 0.0 - 0.89 | 0.0 - 1.0 |
| 平均激活强度 | 0.45 | 0.998 |
| 数据精度 | 模拟激活 | 精确ROI映射 |
| 计算复杂度 | 简单 | 复杂 |

## 🎨 美化建议

### 自动设置
在BrainNet Viewer中运行：

**基础版本：**
```matlab
run('activation_map_settings.m')
```

**高级版本：**
```matlab
run('advanced_activation_settings.m')
```

### 手动美化步骤
1. **背景设置**: 白色背景
2. **颜色映射**: 选择Jet或Hot
3. **透明度**: 0.3-0.5
4. **阈值**: 调整显示显著激活
5. **标题**: "BrainGNN ROI激活图 (ABIDE数据)"
6. **颜色条**: 添加颜色条显示激活强度

## 📈 分析要点

### 激活模式分析
1. **激活强度**: 观察不同脑区的激活强度
2. **空间分布**: 分析激活的空间分布模式
3. **对称性**: 检查左右半球激活的对称性
4. **功能网络**: 识别重要的功能网络节点

### 论文展示要点
1. **多视角**: 展示Lateral/Medial/Full视角
2. **颜色条**: 添加标准化颜色条
3. **阈值**: 使用统计阈值显示显著激活
4. **对比**: 与对照组或基线对比

## 🔧 故障排除

### 文件加载失败
- 检查文件路径是否正确
- 确认DPV文件格式正确
- 验证mesh文件存在
- 检查文件大小是否为81924行

### 显示异常
- 调整激活阈值
- 修改颜色映射
- 调整透明度设置
- 检查数据范围

### MATLAB路径问题
- 确保BrainNet Viewer在MATLAB路径中
- 检查工作目录是否正确
- 验证所有依赖文件存在

## 📝 文件说明

### 基础版本文件
| 文件 | 描述 | 格式 | 大小 |
|------|------|------|------|
| `brain_activation.txt` | 脑区重要性分数 | 100×1向量 | 1KB |
| `brain_activation.dpv` | 表面顶点激活数据 | 81924×1向量 | 737KB |
| `matlab_activation_map.m` | 可视化脚本 | MATLAB脚本 | 2.4KB |
| `activation_map_settings.m` | 自动设置脚本 | MATLAB脚本 | 1KB |

### 高级版本文件
| 文件 | 描述 | 格式 | 大小 |
|------|------|------|------|
| `advanced_activation.txt` | 精确ROI重要性分数 | 100×1向量 | 1KB |
| `advanced_activation.dpv` | 精确表面顶点激活数据 | 81924×1向量 | 737KB |
| `roi_coordinates.txt` | ROI坐标和重要性 | 100×4矩阵 | 3KB |
| `matlab_advanced_activation.m` | 高级可视化脚本 | MATLAB脚本 | 2.6KB |
| `advanced_activation_settings.m` | 高级设置脚本 | MATLAB脚本 | 1KB |

## 🎯 版本选择建议

### 选择基础版本的情况
- 快速演示和初步分析
- 对精度要求不高
- 计算资源有限
- 需要简单直观的结果

### 选择高级版本的情况
- 论文发表和学术展示
- 需要精确的ROI映射
- 对激活模式有严格要求
- 需要与真实脑区对应

## 🚀 快速开始

1. **选择版本**: 基础版本或高级版本
2. **启动MATLAB**: 运行对应的MATLAB脚本
3. **调整设置**: 使用推荐设置或自动设置脚本
4. **保存图像**: 导出高质量图像用于论文

---

**✅ 现在您可以使用BrainNet Viewer制作论文级别的脑区激活图了！**

**推荐使用高级版本获得最佳效果。** 