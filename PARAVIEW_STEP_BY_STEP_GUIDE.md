# 🔬 ParaView 3D脑图查看完整指南

## 🚀 快速开始 (3分钟查看您的脑图)

### Step 1: 启动ParaView
```bash
# 方法1: 命令行启动
paraview

# 方法2: 从应用程序启动
# Finder → Applications → ParaView-6.0.0.app
```

### Step 2: 加载第一个文件 - 大脑表面
1. 点击 **File → Open**
2. 导航到您的项目目录：`~/Desktop/BrainGNN_Pytorch-main/paraview_data/`
3. 选择 `brain_activation_surface.vtk`
4. 点击 **OK**
5. 在左侧属性面板点击 **Apply** ✅

**🎉 恭喜！您应该看到一个3D大脑表面了！**

### Step 3: 设置激活颜色映射
1. 在左侧 **Properties** 面板中：
   - 找到 **Coloring** 下拉菜单
   - 选择 **"PainActivation"** (而不是"Solid Color")
2. 点击 **Apply** ✅

**🌈 现在大脑表面应该显示颜色了！红色=疼痛激活，蓝色=疼痛抑制**

### Step 4: 添加脑区节点
1. **File → Open**
2. 选择 `brain_regions_pain.vtk`
3. 点击 **Apply**
4. 在Properties面板中：
   - **Representation**: 改为 **"Point Gaussian"**
   - **Coloring**: 选择 **"Activation"**
   - **Gaussian Radius**: 设为 **5.0**
5. 点击 **Apply** ✅

**🔴🔵 现在您看到14个关键脑区的球体！**

### Step 5: 调整视角
- **鼠标左键拖拽**: 旋转查看
- **鼠标滚轮**: 放大缩小
- **Shift + 左键拖拽**: 平移

---

## 🎨 高级可视化技巧

### 🔧 预设最佳视角

点击工具栏上的这些按钮获得标准视角：
- **+X** : 右侧面视图
- **-X** : 左侧面视图  
- **+Z** : 顶部视图
- **+Y** : 前面视图

### 🌈 自定义颜色方案

1. 找到颜色条 (右侧竖直条)
2. 点击颜色条旁的 **齿轮图标** ⚙️
3. 在 **Choose Preset** 中选择：
   - **"Cool to Warm"** (蓝-白-红，经典)
   - **"Viridis"** (紫-蓝-绿-黄，现代)
   - **"Plasma"** (紫-粉-黄，高对比)

### 📊 显示数值范围

1. **View → Color Legend** 
2. 勾选 **Show Color Legend**
3. 调整位置和大小

---

## 🎬 使用自动化脚本 (推荐！)

### 方法1: Python Shell中运行
1. 在ParaView中：**Tools → Python Shell**
2. 点击 **Run Script**
3. 选择 `paraview_brain_visualization.py`
4. **🎉 自动加载所有文件并设置最佳效果！**

### 方法2: 命令行批量处理
```bash
cd ~/Desktop/BrainGNN_Pytorch-main
pvpython paraview_data/paraview_brain_visualization.py
```

---

## 📸 保存高质量图片

### 💾 快速截图
**File → Save Screenshot**
- **文件名**: `my_brain_3d.png`
- **分辨率**: 选择 **1920 x 1080** 或更高

### 🎯 发表质量设置
1. **File → Save Screenshot**
2. 高级设置：
   - **Image Resolution**: `3840 x 2160` (4K)
   - **Quality**: `100`
   - **Transparent Background**: 勾选 (如果需要透明背景)

---

## 🔍 探索您的数据

### 📊 查看脑区信息
1. 使用 **Select Points On** 工具 (工具栏上的十字箭头图标)
2. 点击任意脑区球体
3. 在 **Information** 面板查看：
   - 区域名称
   - 激活值
   - 网络类型

### 📏 测量功能
1. **Filters → Ruler**
2. 点击两个点测量距离 (mm单位)

### ✂️ 切片查看
1. **Filters → Slice** 
2. 调整切片平面查看大脑内部

---

## 🐛 常见问题解决

### ❓ 看不到颜色？
**解决方案**:
1. 确保选择了正确的数据数组 (PainActivation 或 Activation)
2. 点击 **Rescale to Data Range** 按钮
3. 检查颜色映射范围

### ❓ 球体太小/太大？
**解决方案**:
1. 调整 **Gaussian Radius** (2.0 - 10.0)
2. 或者改变 **Scale Factor**

### ❓ 性能慢？
**解决方案**:
1. **View → Render View → LOD Threshold**: 设为较小值
2. 关闭不需要的数据对象
3. 降低表面分辨率

---

## 🎯 具体查看内容说明

### 🧠 您将看到的内容：

1. **灰色大脑表面**: 基于标准MNI模板的真实大脑形状
2. **彩色激活热图**: 
   - 🔴 **红色区域**: 疼痛时激活增强
   - 🔵 **蓝色区域**: 疼痛时激活减少
3. **球体标记**: 14个关键脑区
   - 大小表示激活强度
   - 颜色表示激活方向
4. **连接线**: 脑区间的功能连接

### 📊 数值含义：
- **激活值范围**: -0.6 到 +0.6
- **正值**: 疼痛状态下激活增强
- **负值**: 疼痛状态下激活抑制
- **坐标**: MNI标准空间 (毫米)

---

## 🎮 交互操作总结

| 操作 | 方法 |
|------|------|
| 旋转视角 | 鼠标左键拖拽 |
| 缩放 | 鼠标滚轮 |
| 平移 | Shift + 左键拖拽 |
| 选择对象 | Ctrl + 点击 |
| 重置视角 | View → Reset Camera |
| 全屏显示 | F11 |

---

## 🏆 发表质量输出

### 📸 标准视角截图
建议保存这4个标准视角：
1. **Left Lateral** (-90°, 0°)
2. **Right Lateral** (90°, 0°)  
3. **Superior** (0°, 90°)
4. **Anterior** (0°, 0°)

### 🎨 颜色方案建议
- **科学期刊**: Cool to Warm (蓝-白-红)
- **现代风格**: Viridis (紫-蓝-绿-黄)
- **高对比**: Plasma (紫-粉-黄)

---

## 🚀 现在就开始！

1. **启动ParaView**: `paraview`
2. **打开文件**: `brain_activation_surface.vtk`
3. **设置颜色**: 选择 "PainActivation"
4. **探索数据**: 旋转、缩放、截图！

**🎉 享受您的专业3D脑图可视化体验！**