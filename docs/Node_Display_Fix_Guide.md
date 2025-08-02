# BrainNet Viewer - 节点显示修复指南

## 🎯 问题解决

已修复以下常见问题：
1. ✅ 颜色值范围调整 (0-1 → 0-20)
2. ✅ 确保节点大小 ≥ 3
3. ✅ 文件扩展名改为 .node
4. ✅ 确保坐标在合理范围内

## 📁 生成的文件

### 🎯 推荐使用的节点文件
- `fixed_activation.node` - 标准修复版本
- `simple_activation.node` - 简化版本（6列）
- `large_activation.node` - 大节点版本
- `contrast_activation.node` - 高对比度版本

### 🔧 测试文件
- `test_fixed_nodes.m` - MATLAB测试脚本

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_fixed_nodes.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `fixed_activation.node`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'fixed_activation.node')
```

## ⚙️ 关键设置

### BrainNet Viewer设置
- **View → Node**: ✅ 必须勾选
- **Option → Display Node**: ✅ 必须开启
- **Node size scaling**: ✅ 开启
- **Node color**: Custom
- **Node shape**: 球体

## 🔧 故障排除

### 如果节点仍然不显示：

1. **检查View设置**
   - 确保"View → Node"已勾选
   - 确保"Option → Display Node"已开启

2. **尝试不同文件**
   - `fixed_activation.node` (标准)
   - `large_activation.node` (大节点)
   - `contrast_activation.node` (高对比度)

3. **调整参数**
   - 增加Node size scaling
   - 调整Node size基础值

4. **检查文件格式**
   - 确保是.node文件
   - 确保分隔符是制表符

## 📊 文件对比

| 文件 | 特点 | 推荐用途 |
|------|------|----------|
| `fixed_activation.node` | 标准修复 | 一般使用 |
| `simple_activation.node` | 6列格式 | 兼容性测试 |
| `large_activation.node` | 大节点 | 演示展示 |
| `contrast_activation.node` | 高对比度 | 学术论文 |

## 🎉 成功标志

✅ **成功时您会看到：**
- 脑表面上有彩色的球体节点
- 节点大小适中，清晰可见
- 节点颜色反映重要性
- 整体呈现类似论文的激活图

---
**🎯 现在应该能正确显示节点了！**
