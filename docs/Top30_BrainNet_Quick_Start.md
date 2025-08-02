# BrainNet Viewer - Top-30重要节点可视化指南

## 📁 生成的文件

✅ **Top-30节点文件已生成：**
- `top30.node` - 30个最重要ROI的6列格式节点文件
- `top30.edge` - 30×30的连接矩阵
- `matlab_top30_visualization.m` - MATLAB可视化脚本
- `brainnet_settings.m` - 自动设置脚本

## 🧠 节点信息

**Top-10最重要ROI：**
1. 重要性: 13.360, 模块: 4, 坐标: (-22.6, 79.4, 59.8)
2. 重要性: 13.355, 模块: 3, 坐标: (17.8, -92.3, -43.9)
3. 重要性: 13.350, 模块: 1, 坐标: (-79.5, 61.1, 36.2)
4. 重要性: 13.350, 模块: 5, 坐标: (37.5, -121.6, 102.6)
5. 重要性: 13.349, 模块: 5, 坐标: (59.8, -80.1, -39.3)

**文件格式：**
- 第1-3列：3D坐标 (x, y, z)
- 第4列：节点大小 (重要性分数)
- 第5列：颜色值 (0-1)
- 第6列：模块编号 (1-5)

## 🚀 使用方法

### 方法1：MATLAB脚本自动启动
```matlab
% 在MATLAB中运行
run('matlab_top30_visualization.m')
```

### 方法2：手动在BrainNet Viewer中加载
1. 打开BrainNet Viewer
2. 加载文件：
   - **Surface**: `BrainMesh_ICBM152.nv`
   - **Node**: `top30.node`
   - **Edge**: `top30.edge`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'top30.node', 'top30.edge')
```

## ⚙️ 推荐设置

### 节点设置
- **Node size scaling**: ✅ 开启 (根据第4列自动缩放)
- **Node color**: 根据第5列颜色值
- **Node transparency**: 0.8-1.0

### 边设置
- **Edge threshold**: 0.1-0.3 (过滤弱连接)
- **Edge color**: 根据连接强度
- **Edge transparency**: 0.3-0.5

### 表面设置
- **Surface transparency**: 0.3-0.5
- **Lighting**: Phong
- **Color map**: Jet 或 Hot

### 视角设置
- **View**: Lateral/Medial/Full
- **Rotation**: 自由调整
- **Zoom**: 适当缩放

## 📊 数据统计

- **节点数**: 30个最重要ROI
- **边数**: 870个非零连接
- **重要性范围**: 13.322 - 13.360
- **边强度范围**: 0.000029 - 0.163237
- **模块数**: 5个功能模块

## 🎨 美化建议

### 自动设置
在BrainNet Viewer中运行：
```matlab
run('brainnet_settings.m')
```

### 手动美化
1. **背景**: 白色背景
2. **节点**: 根据重要性调整大小
3. **边**: 根据强度调整透明度
4. **标题**: "BrainGNN Top-30重要ROI网络 (ABIDE数据)"

## 📈 分析要点

1. **重要性分布**: 观察Top-30节点的空间分布
2. **模块组织**: 分析5个功能模块的连接模式
3. **连接强度**: 识别强连接和弱连接
4. **空间聚类**: 观察重要ROI是否在特定脑区聚集

## 🔧 故障排除

### 文件加载失败
- 检查文件路径是否正确
- 确认文件格式为制表符分隔
- 验证节点和边文件维度匹配

### 显示异常
- 调整边阈值过滤弱连接
- 修改节点大小缩放
- 调整透明度设置

### MATLAB路径问题
- 确保BrainNet Viewer在MATLAB路径中
- 检查工作目录是否正确

## 📝 文件说明

| 文件 | 描述 | 格式 |
|------|------|------|
| `top30.node` | Top-30节点文件 | 30×6矩阵 |
| `top30.edge` | Top-30连接矩阵 | 30×30矩阵 |
| `matlab_top30_visualization.m` | 可视化脚本 | MATLAB脚本 |
| `brainnet_settings.m` | 自动设置脚本 | MATLAB脚本 |

---

**✅ 准备就绪！您现在可以使用BrainNet Viewer来可视化BrainGNN模型识别出的Top-30重要脑区网络。** 