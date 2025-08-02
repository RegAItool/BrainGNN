# BrainNet Viewer - 脑区激活图使用指南

## 📁 生成的文件

✅ **激活图文件：**
- `brain_activation.txt` - 脑区重要性分数
- `brain_activation.dpv` - 表面顶点激活数据
- `matlab_activation_map.m` - MATLAB可视化脚本
- `activation_map_settings.m` - 自动设置脚本

## 🧠 激活图说明

**数据格式：**
- `.txt` 文件：100个ROI的重要性分数
- `.dpv` 文件：81924个表面顶点的激活值
- 激活模式：基于高斯分布的脑区激活

**激活区域：**
- 前额叶：双侧前额叶激活
- 顶叶：双侧顶叶激活  
- 颞叶：双侧颞叶激活
- 枕叶：双侧枕叶激活

## 🚀 使用方法

### 方法1：MATLAB脚本自动启动
```matlab
% 在MATLAB中运行
run('matlab_activation_map.m')
```

### 方法2：手动在BrainNet Viewer中加载
1. 打开BrainNet Viewer
2. 加载文件：
   - **Surface**: `BrainMesh_ICBM152.nv`
   - **Data**: `brain_activation.dpv`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'brain_activation.dpv')
```

## ⚙️ 推荐设置

### 激活图设置
- **Color map**: Jet 或 Hot (适合激活图)
- **Threshold**: 0.1-0.3 (显示显著激活)
- **Transparency**: 0.3-0.5
- **Lighting**: Phong
- **View**: 选择Lateral/Medial/Full视角

### 颜色映射
- **Jet**: 蓝色(低) → 绿色 → 黄色 → 红色(高)
- **Hot**: 黑色(低) → 红色 → 黄色 → 白色(高)

## 📊 数据统计

- **激活顶点数**: 81924个表面顶点
- **激活强度范围**: 0.0 - 0.9
- **激活区域**: 8个主要脑区
- **数据格式**: DPV (Data Per Vertex)

## 🎨 美化建议

### 自动设置
在BrainNet Viewer中运行：
```matlab
run('activation_map_settings.m')
```

### 手动美化
1. **背景**: 白色背景
2. **颜色映射**: Jet或Hot
3. **透明度**: 0.3-0.5
4. **阈值**: 0.1-0.3
5. **标题**: "BrainGNN ROI重要性激活图 (ABIDE数据)"

## 📈 分析要点

1. **激活强度**: 观察不同脑区的激活强度
2. **空间分布**: 分析激活的空间分布模式
3. **对称性**: 检查左右半球激活的对称性
4. **功能网络**: 识别重要的功能网络节点

## 🔧 故障排除

### 文件加载失败
- 检查文件路径是否正确
- 确认DPV文件格式正确
- 验证mesh文件存在

### 显示异常
- 调整激活阈值
- 修改颜色映射
- 调整透明度设置

### MATLAB路径问题
- 确保BrainNet Viewer在MATLAB路径中
- 检查工作目录是否正确

## 📝 文件说明

| 文件 | 描述 | 格式 |
|------|------|------|
| `brain_activation.txt` | 脑区重要性分数 | 100×1向量 |
| `brain_activation.dpv` | 表面顶点激活数据 | 81924×1向量 |
| `matlab_activation_map.m` | 可视化脚本 | MATLAB脚本 |
| `activation_map_settings.m` | 自动设置脚本 | MATLAB脚本 |

---

**✅ 准备就绪！您现在可以使用BrainNet Viewer来可视化BrainGNN模型识别出的脑区激活模式。**
