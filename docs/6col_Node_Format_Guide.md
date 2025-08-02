# BrainNet Viewer - 6列节点文件使用指南

## 🎯 问题解决

已创建正确的6列节点文件格式：
```
x y z size color shape
```

**列说明：**
- **第1-3列**: 坐标 (x, y, z)
- **第4列**: 点大小 (统一设为3)
- **第5列**: 颜色强度 (0-20范围)
- **第6列**: 形状编号 (统一为1)

## 📁 生成的文件

### 🎯 推荐使用的节点文件
- `standard_6col.node` - 标准6列格式（推荐）
- `large_6col.node` - 大节点版本
- `contrast_6col.node` - 高对比度版本
- `top30_6col.node` - Top-30版本

### 🔧 测试文件
- `test_6col_nodes.m` - MATLAB测试脚本

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_6col_nodes.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `standard_6col.node`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'standard_6col.node')
```

## ⚙️ 关键设置

### BrainNet Viewer设置
- **View → Node**: ✅ 必须勾选
- **Option → Display Node**: ✅ 必须开启
- **Node size scaling**: ✅ 开启
- **Node color**: Custom
- **Node shape**: 球体

## 📊 文件对比

| 文件 | 特点 | 推荐用途 |
|------|------|----------|
| `standard_6col.node` | 标准6列格式 | 一般使用 |
| `large_6col.node` | 大节点 | 演示展示 |
| `contrast_6col.node` | 高对比度 | 学术论文 |
| `top30_6col.node` | Top-30 ROI | 重点展示 |

## 🎉 成功标志

✅ **成功时您会看到：**
- 脑表面上有彩色的球体节点
- 节点大小统一为3
- 节点颜色反映重要性
- 整体呈现类似论文的激活图

## 🔧 故障排除

### 如果节点仍然不显示：

1. **检查View设置**
   - 确保"View → Node"已勾选
   - 确保"Option → Display Node"已开启

2. **尝试不同文件**
   - `standard_6col.node` (标准)
   - `large_6col.node` (大节点)

3. **检查文件格式**
   - 确保是6列格式
   - 确保分隔符是制表符

---
**🎯 现在使用正确的6列格式应该能正确显示节点了！**
