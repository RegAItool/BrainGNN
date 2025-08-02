# BrainNet Viewer 激活图修复指南

## 🔧 问题诊断
如果激活图只显示大脑表面而没有颜色，可能是以下原因：
1. DPV文件格式不被识别
2. 数据范围不合适
3. 阈值设置过高

## 📁 修复版本文件
- `fixed_activation.dpv` - 修复版DPV文件
- `fixed_activation.txt` - TXT格式文件
- `fixed_activation.csv` - CSV格式文件
- `test_activation.dpv` - 简化测试版本
- `test_brainnet_activation.m` - 测试脚本

## 🚀 测试步骤

### 步骤1: 运行测试脚本
```matlab
run('test_brainnet_activation.m')
```

### 步骤2: 手动测试
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 依次尝试加载以下Data文件:
   - `fixed_activation.dpv`
   - `test_activation.dpv`
   - `fixed_activation.txt`

### 步骤3: 调整设置
如果文件加载成功但看不到颜色：
- 降低Threshold到0.1
- 选择Jet颜色映射
- 调整透明度到0.5

## 📊 数据信息
- 总顶点数: 81924
- 激活顶点数: ~24,577
- 激活强度范围: 0.0 - 1.0
- 文件大小: ~737KB

## 🔍 故障排除
1. 检查文件是否存在
2. 确认文件格式正确
3. 尝试不同的阈值设置
4. 检查BrainNet Viewer版本

---
**✅ 使用修复版本应该能正确显示激活图！**
