# BrainNet Viewer - 最终DPV激活图指南

## 🎯 问题解决

您之前遇到的DPV文件不显示颜色的问题已经解决！

**问题原因：** 之前的DPV文件格式不正确。BrainNet Viewer的DPV格式要求：
```
x y z size color shape label
```

**解决方案：** 现在创建了正确格式的DPV文件。

## 📁 生成的文件

### ✅ 正确格式的DPV文件
- `correct_activation.dpv` - 完整100个ROI的激活图
- `top30_activation.dpv` - Top-30 ROI的激活图（推荐）

### 📋 验证和测试文件
- `verify_dpv_format.py` - Python格式验证脚本
- `test_final_dpv.m` - MATLAB测试脚本

## 🧠 DPV格式详解

**正确格式（7列）：**
```
x坐标  y坐标  z坐标  重要性  颜色值  形状  标签
```

**列说明：**
- **x, y, z**: ROI的MNI坐标
- **size**: 节点大小（基于重要性分数）
- **color**: 颜色值（0-1，用于颜色映射）
- **shape**: 形状（1=球体）
- **label**: 标签编号

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_final_dpv.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `correct_activation.dpv` 或 `top30_activation.dpv`

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

| 文件 | ROI数量 | 重要性范围 | 颜色范围 | 推荐用途 |
|------|---------|------------|----------|----------|
| `correct_activation.dpv` | 100 | 13.319-13.360 | 0.000-1.000 | 完整分析 |
| `top30_activation.dpv` | 30 | 13.319-13.360 | 0.000-1.000 | 重点展示 |

## 🎯 版本选择建议

### 完整版本 (`correct_activation.dpv`)
- **优点**: 显示所有ROI，信息完整
- **缺点**: 可能过于密集，难以看清重点
- **适用**: 详细分析，学术论文

### Top-30版本 (`top30_activation.dpv`)
- **优点**: 突出最重要的ROI，清晰易读
- **缺点**: 信息不完整
- **适用**: 演示展示，重点突出

## 🔧 故障排除

### 如果仍然不显示颜色：

1. **检查Node设置**
   - 确保"Node color"设置为"Custom"
   - 确保"Node size scaling"开启

2. **调整颜色映射**
   - 尝试不同的颜色映射：Jet, Hot, Parula
   - 调整颜色范围

3. **检查文件格式**
   - 运行 `python verify_dpv_format.py` 验证格式
   - 确保文件是制表符分隔

4. **重新加载**
   - 关闭BrainNet Viewer
   - 重新打开并加载文件

### 如果节点太小或太大：
- 调整"Node size scaling"参数
- 修改"Node size"基础值

## 📈 预期效果

使用正确格式的DPV文件，您应该看到：

1. **彩色节点**: 不同重要性的ROI显示不同颜色
2. **大小差异**: 重要ROI显示为更大的节点
3. **空间分布**: ROI在脑表面的正确位置
4. **激活模式**: 类似论文中的脑区激活图

## 🎉 成功标志

✅ **成功时您会看到：**
- 脑表面上有彩色的球体节点
- 节点大小反映重要性
- 节点颜色反映激活强度
- 整体呈现类似论文的激活图

## 📝 使用步骤总结

1. **验证文件**: `python verify_dpv_format.py`
2. **选择文件**: 推荐使用 `top30_activation.dpv`
3. **启动BrainNet Viewer**: 加载Surface和Node文件
4. **调整设置**: 按照推荐设置配置
5. **查看结果**: 应该看到彩色的脑区激活图

---

**🎯 现在您应该能够看到类似论文中的彩色脑区激活图了！**

如果仍有问题，请检查：
- BrainNet Viewer版本
- 文件路径是否正确
- MATLAB工作目录设置 