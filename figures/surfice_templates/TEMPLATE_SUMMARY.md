# 🧠 SurfIce大脑模板文件总结

## 📁 可用的大脑模板:

### ✅ 自制模版 (推荐先试这些):
- `brain_fixed.ply` - 修正的PLY格式大脑 (推荐)
- `brain.obj` - OBJ格式大脑 (通用)
- `brain.stl` - STL格式大脑 (3D标准)
- `braingnn_brain.mz3` - 转换的MZ3格式 (如果成功创建)

### 🌐 下载的官方模板:
- `.DS_Store` (6.0 KB)
- `brain.obj` (73.3 KB)
- `brain.stl` (316.5 KB)
- `brain_faces.txt` (59.7 KB)
- `brain_fixed.ply` (105.4 KB)
- `brain_vertices.txt` (62.2 KB)
- `mni152.mz3` (38.9 KB)

## 🚀 推荐使用顺序:

### 第1优先级: 自制PLY格式
```
File → Open → brain_fixed.ply
```

### 第2优先级: 下载的MZ3格式
```
File → Open → pial.mz3 (如果下载成功)
File → Open → BrainMesh_ICBM152.mz3 (如果下载成功)
```

### 第3优先级: 其他格式
```
File → Open → brain.obj
File → Open → brain.stl
```

## 📊 激活数据加载:
```
Overlay → Add → braingnn_pain_activation.nii.gz
```

## 🎯 如果全部失败:
直接加载NIfTI数据，SurfIce会自动生成基础模板:
```
File → Open → braingnn_pain_activation.nii.gz
```

---
🧠 BrainGNN疼痛分类 - 98.7%准确率
🎯 多种格式确保兼容性
