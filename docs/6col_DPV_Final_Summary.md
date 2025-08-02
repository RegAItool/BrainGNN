# 🎯 6列DPV文件 - 最终解决方案

## ✅ 问题已解决

已成功创建正确的6列DPV文件格式，符合BrainNet Viewer规范：

```
x y z size color shape
```

**列说明：**
- **第1-3列**: 坐标 (x, y, z)
- **第4列**: 点大小 (统一设为3)
- **第5列**: 颜色强度 (0-20范围)
- **第6列**: 形状编号 (统一为1)

## 📁 可用的6列DPV文件

### 🎯 推荐使用（按优先级）
1. **`standard_6col_activation.dpv`** - 标准6列DPV格式（推荐）
2. **`large_6col_activation.dpv`** - 大节点版本（如果标准版本节点太小）
3. **`contrast_6col_activation.dpv`** - 高对比度版本（学术展示）
4. **`top30_6col_activation.dpv`** - Top-30版本（重点展示）

## 🚀 使用方法

### 方法1：MATLAB脚本测试
```matlab
run('test_6col_dpv_files.m')
```

### 方法2：手动加载
1. 打开BrainNet Viewer
2. 加载Surface: `BrainMesh_ICBM152.nv`
3. 加载Node: `standard_6col_activation.dpv`

### 方法3：命令行启动
```matlab
BrainNet_View('BrainMesh_ICBM152.nv', 'standard_6col_activation.dpv')
```

## ⚙️ 关键设置

### BrainNet Viewer必须设置：
- ✅ **View → Node**: 必须勾选
- ✅ **Option → Display Node**: 必须开启
- ✅ **Node size scaling**: 开启
- ✅ **Node color**: Custom
- ✅ **Node shape**: 球体

## 📊 文件规格

| 文件 | 节点数 | 点大小 | 颜色范围 | 特点 |
|------|--------|--------|----------|------|
| `standard_6col_activation.dpv` | 100 | 3.0 | 0-20 | 标准格式 |
| `large_6col_activation.dpv` | 100 | 5.0 | 0-20 | 大节点 |
| `contrast_6col_activation.dpv` | 100 | 3.0 | 0-20 | 高对比度 |
| `top30_6col_activation.dpv` | 30 | 3.0 | 1.46-20 | Top-30 ROI |

## 🎉 成功标志

✅ **成功时您会看到：**
- 脑表面上有彩色的球体节点
- 节点大小统一（3或5）
- 节点颜色反映重要性（0-20范围）
- 整体呈现类似论文的激活图

## 🔧 故障排除

### 如果节点仍然不显示：

1. **检查View设置**
   - 确保"View → Node"已勾选
   - 确保"Option → Display Node"已开启

2. **尝试不同文件**
   - 先试 `standard_6col_activation.dpv`
   - 如果看不到，试 `large_6col_activation.dpv`

3. **检查文件格式**
   - 确保是6列格式
   - 确保分隔符是制表符

## 📋 文件验证

运行以下命令验证文件：
```bash
head -5 standard_6col_activation.dpv
```

应该看到6列数据：
```
x坐标  y坐标  z坐标  大小  颜色  形状
```

## 🎯 最终建议

1. **首选**: `standard_6col_activation.dpv`
2. **如果节点太小**: `large_6col_activation.dpv`
3. **学术展示**: `contrast_6col_activation.dpv`
4. **重点展示**: `top30_6col_activation.dpv`

## ✅ 验证结果

所有6列DPV文件已通过验证：
- ✅ 格式正确：6列
- ✅ 坐标范围合理
- ✅ 点大小统一
- ✅ 颜色范围正确
- ✅ 形状编号统一

---
**🎉 现在您有了正确的6列DPV文件，应该能在BrainNet Viewer中正确显示激活图了！** 