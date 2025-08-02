# BrainNet Viewer - MNI坐标DPV文件使用指南

## 🎯 问题解决

已创建基于真实MNI坐标的6列DPV文件格式：
```
x y z size color shape
```

**列说明：**
- **第1-3列**: 真实MNI坐标 (x, y, z)
- **第4列**: 点大小 (基于重要性，2-5范围)
- **第5列**: 颜色强度 (基于重要性，0-20范围)
- **第6列**: 形状编号 (统一为1)

## 📁 生成的文件

### 🎯 推荐使用的MNI坐标DPV文件
- `mni_standard_6col_activation.dpv` - 标准MNI DPV格式（推荐）
- `mni_large_6col_activation.dpv` - 大节点版本
- `mni_contrast_6col_activation.dpv` - 高对比度版本
- `mni_top30_6col_activation.dpv` - Top-30版本

### 🔧 测试文件
- `test_mni_dpv_files.m` - MATLAB测试脚本

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_mni_dpv_files.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `mni_standard_6col_activation.dpv`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'mni_standard_6col_activation.dpv')
```

## ⚙️ 关键设置

### BrainNet Viewer设置
- **View → Node**: ✅ 必须勾选
- **Option → Display Node**: ✅ 必须开启
- **Node size scaling**: ✅ 开启
- **Node color**: Custom
- **Node shape**: 球体

## 📊 文件规格

| 文件 | 节点数 | 坐标类型 | 点大小范围 | 颜色范围 | 特点 |
|------|--------|----------|------------|----------|------|
| `mni_standard_6col_activation.dpv` | 100 | 真实MNI | 2-5 | 0-20 | 标准格式 |
| `mni_large_6col_activation.dpv` | 100 | 真实MNI | 4-8 | 0-20 | 大节点 |
| `mni_contrast_6col_activation.dpv` | 100 | 真实MNI | 2-5 | 0-20 | 高对比度 |
| `mni_top30_6col_activation.dpv` | 30 | 真实MNI | 2-5 | 0-20 | Top-30 ROI |

## 🎉 成功标志

✅ **成功时您会看到：**
- 脑表面上有彩色的球体节点
- 节点位置在真实的大脑区域内
- 节点大小反映重要性
- 节点颜色反映重要性
- 整体呈现类似论文的激活图

## 🔧 故障排除

### 如果节点仍然不显示：

1. **检查View设置**
   - 确保"View → Node"已勾选
   - 确保"Option → Display Node"已开启

2. **尝试不同文件**
   - `mni_standard_6col_activation.dpv` (标准)
   - `mni_large_6col_activation.dpv` (大节点)

3. **检查文件格式**
   - 确保是6列格式
   - 确保分隔符是制表符

---
**🎯 现在使用基于真实MNI坐标的DPV格式应该能正确显示激活图了！**
