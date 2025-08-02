# BrainNet Viewer - 正确DPV格式使用指南

## 📁 生成的文件

✅ **正确格式的DPV文件：**
- `correct_activation.dpv` - 完整ROI的DPV文件
- `top30_activation.dpv` - Top-30 ROI的DPV文件
- `test_correct_dpv.m` - MATLAB测试脚本

## 🧠 DPV格式说明

**正确格式：**
```
x y z size color shape label
```

**列说明：**
- **x, y, z**: ROI的MNI坐标
- **size**: 节点大小（基于重要性）
- **color**: 颜色值（0-1）
- **shape**: 形状（1=球体）
- **label**: 标签编号

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_correct_dpv.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `correct_activation.dpv`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'correct_activation.dpv')
```

## ⚙️ 推荐设置

### 节点设置
- **Node size scaling**: ✅ 开启
- **Node color**: 根据第5列颜色值
- **Node shape**: 球体
- **Node transparency**: 0.8-1.0

### 表面设置
- **Surface transparency**: 0.3-0.5
- **Lighting**: Phong
- **Color map**: Jet 或 Hot

## 📊 数据统计

| 文件 | ROI数量 | 重要性范围 | 坐标范围 |
|------|---------|------------|----------|
| `correct_activation.dpv` | 100 | 0.5-1.0 | MNI标准 |
| `top30_activation.dpv` | 30 | 0.5-1.0 | MNI标准 |

## 🎯 版本选择

- **完整版本**: 显示所有100个ROI
- **Top-30版本**: 只显示最重要的30个ROI（推荐）

## 🔧 故障排除

### 文件加载失败
- 检查文件格式是否正确（6列）
- 确认坐标在合理范围内
- 验证分隔符为制表符

### 显示异常
- 调整节点大小缩放
- 修改颜色映射
- 调整透明度设置

---
**✅ 现在使用正确格式的DPV文件应该能正常显示激活图！**
