#!/usr/bin/env python3
"""
创建正确的6列节点文件
BrainNet Viewer标准格式：x y z size color shape
"""

import numpy as np

def create_correct_6col_node():
    """创建正确的6列节点文件"""
    
    print("=== 创建正确的6列节点文件 ===")
    
    # 1. 加载原始数据
    try:
        original_data = np.loadtxt('correct_activation.dpv')
        print(f"✅ 加载原始数据: {original_data.shape}")
    except:
        print("❌ 无法加载原始数据，使用模拟数据")
        # 创建模拟数据
        n_rois = 30
        original_data = np.zeros((n_rois, 7))
        original_data[:, 0] = np.random.uniform(-80, 80, n_rois)  # x
        original_data[:, 1] = np.random.uniform(-100, 100, n_rois)  # y
        original_data[:, 2] = np.random.uniform(-60, 60, n_rois)   # z
        original_data[:, 3] = np.random.uniform(5, 15, n_rois)     # size
        original_data[:, 4] = np.random.uniform(0, 1, n_rois)      # color
        original_data[:, 5] = 1  # shape
        original_data[:, 6] = np.arange(1, n_rois + 1)  # label
    
    # 2. 创建正确的6列格式
    print("\n=== 创建6列格式 ===")
    
    # 只保留前6列：x y z size color shape
    node_data = original_data[:, :6].copy()
    
    # 修复各列：
    # 第1-3列：坐标（保持不变）
    print("1. 坐标列（1-3列）: 保持不变")
    
    # 第4列：点大小（统一设为3）
    print("2. 点大小（第4列）: 统一设为3")
    node_data[:, 3] = 3.0
    
    # 第5列：颜色强度（0-20范围）
    print("3. 颜色强度（第5列）: 调整到0-20范围")
    # 基于重要性分数创建颜色
    importance_scores = original_data[:, 3]  # 使用原始的重要性分数
    normalized_scores = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
    node_data[:, 4] = normalized_scores * 20  # 0-20范围
    
    # 第6列：形状编号（统一为1）
    print("4. 形状编号（第6列）: 统一设为1")
    node_data[:, 5] = 1
    
    # 3. 创建多个版本
    print("\n=== 创建多个版本 ===")
    
    # 版本1: 标准6列格式
    standard_file = 'standard_6col.node'
    np.savetxt(standard_file, node_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 标准6列格式: {standard_file}")
    
    # 版本2: 大节点版本
    large_data = node_data.copy()
    large_data[:, 3] = 5.0  # 更大的节点
    large_file = 'large_6col.node'
    np.savetxt(large_file, large_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 大节点版本: {large_file}")
    
    # 版本3: 高对比度版本
    contrast_data = node_data.copy()
    # 创建更明显的颜色对比
    contrast_data[:, 4] = np.linspace(0, 20, len(contrast_data))  # 线性分布
    contrast_file = 'contrast_6col.node'
    np.savetxt(contrast_file, contrast_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 高对比度版本: {contrast_file}")
    
    # 版本4: Top-30版本
    # 选择最重要的30个ROI
    sorted_indices = np.argsort(importance_scores)[::-1]
    top30_indices = sorted_indices[:30]
    top30_data = node_data[top30_indices, :]
    top30_file = 'top30_6col.node'
    np.savetxt(top30_file, top30_data, fmt='%.6f', delimiter='\t')
    print(f"✅ Top-30版本: {top30_file}")
    
    # 4. 显示数据统计
    print("\n=== 数据统计 ===")
    print(f"节点数量: {len(node_data)}")
    print(f"坐标范围: X({node_data[:,0].min():.0f}到{node_data[:,0].max():.0f})")
    print(f"              Y({node_data[:,1].min():.0f}到{node_data[:,1].max():.0f})")
    print(f"              Z({node_data[:,2].min():.0f}到{node_data[:,2].max():.0f})")
    print(f"点大小: 统一为 {node_data[0,3]:.1f}")
    print(f"颜色范围: {node_data[:,4].min():.2f} 到 {node_data[:,4].max():.2f}")
    print(f"形状编号: 统一为 {node_data[0,5]:.0f}")
    
    # 5. 显示前5行示例
    print("\n=== 6列格式示例（前5行）===")
    print("x\t\ty\t\tz\t\tsize\tcolor\tshape")
    print("-" * 60)
    for i in range(min(5, len(node_data))):
        row = node_data[i]
        print(f"{row[0]:.3f}\t{row[1]:.3f}\t{row[2]:.3f}\t{row[3]:.1f}\t{row[4]:.2f}\t{row[5]:.0f}")
    
    # 6. 创建MATLAB测试脚本
    matlab_script = '''%% BrainNet Viewer - 6列节点文件测试
% 测试正确的6列节点文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer 6列节点文件测试 ===\\n');

%% 1. 检查文件
files_to_test = {
    'standard_6col.node',
    'large_6col.node', 
    'contrast_6col.node',
    'top30_6col.node'
};

for i = 1:length(files_to_test)
    if exist(files_to_test{i}, 'file')
        fprintf('✅ %s 存在\\n', files_to_test{i});
    else
        fprintf('❌ %s 不存在\\n', files_to_test{i});
    end
end

%% 2. 测试加载
fprintf('\\n=== 测试文件加载 ===\\n');

try
    % 测试标准版本
    data = load('standard_6col.node');
    fprintf('✅ 标准6列版本加载成功\\n');
    fprintf('   数据形状: %s\\n', mat2str(size(data)));
    fprintf('   列数: %d (正确)\\n', size(data, 2));
    
    if size(data, 2) == 6
        fprintf('✅ 格式正确: 6列 (x, y, z, size, color, shape)\\n');
    else
        fprintf('❌ 格式错误: 期望6列，实际%d列\\n', size(data, 2));
    end
    
    % 显示数据统计
    fprintf('   坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\\n', ...
            min(data(:,1)), max(data(:,1)), ...
            min(data(:,2)), max(data(:,2)), ...
            min(data(:,3)), max(data(:,3)));
    fprintf('   点大小: 统一为 %.1f\\n', data(1,4));
    fprintf('   颜色范围: %.2f 到 %.2f\\n', min(data(:,5)), max(data(:,5)));
    fprintf('   形状编号: 统一为 %.0f\\n', data(1,6));
    
catch ME
    fprintf('❌ 文件加载失败: %s\\n', ME.message);
    return;
end

%% 3. 启动BrainNet Viewer
fprintf('\\n=== 启动BrainNet Viewer ===\\n');

try
    if exist('BrainNet_View', 'file')
        fprintf('✅ BrainNet Viewer 可用\\n');
        
        % 尝试启动
        fprintf('正在启动BrainNet Viewer...\\n');
        BrainNet_View('BrainMesh_ICBM152.nv', 'standard_6col.node');
        fprintf('✅ BrainNet Viewer已启动\\n');
        
    else
        fprintf('❌ BrainNet Viewer 不可用\\n');
        fprintf('请手动打开BrainNet Viewer并加载:\\n');
        fprintf('  Surface: BrainMesh_ICBM152.nv\\n');
        fprintf('  Node: standard_6col.node\\n');
    end
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\\n');
    fprintf('  Node: standard_6col.node\\n');
end

%% 4. 推荐设置
fprintf('\\n=== 推荐设置 ===\\n');
fprintf('在BrainNet Viewer中:\\n');
fprintf('  • View → Node: 必须勾选\\n');
fprintf('  • Option → Display Node: 必须开启\\n');
fprintf('  • Node size scaling: 开启\\n');
fprintf('  • Node color: Custom\\n');
fprintf('  • Node shape: 球体\\n');
fprintf('  • Surface transparency: 0.3-0.5\\n');

%% 5. 文件选择建议
fprintf('\\n=== 文件选择建议 ===\\n');
fprintf('• standard_6col.node: 标准版本（推荐）\\n');
fprintf('• large_6col.node: 大节点版本\\n');
fprintf('• contrast_6col.node: 高对比度版本\\n');
fprintf('• top30_6col.node: Top-30版本\\n');

%% 6. 故障排除
fprintf('\\n=== 故障排除 ===\\n');
fprintf('如果节点仍然不显示:\\n');
fprintf('  1. 确保View → Node已勾选\\n');
fprintf('  2. 确保Option → Display Node已开启\\n');
fprintf('  3. 尝试large_6col.node（更大节点）\\n');
fprintf('  4. 检查文件格式（必须是6列）\\n');

fprintf('\\n✅ 测试完成!\\n');
fprintf('现在应该能正确显示节点了!\\n');
'''
    
    with open('test_6col_nodes.m', 'w', encoding='utf-8') as f:
        f.write(matlab_script)
    
    print(f"MATLAB测试脚本已保存: test_6col_nodes.m")
    
    # 7. 创建使用说明
    instructions = '''# BrainNet Viewer - 6列节点文件使用指南

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
'''
    
    with open('6col_Node_Format_Guide.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"使用指南已保存: 6col_Node_Format_Guide.md")
    
    print("\n✅ 6列节点文件创建完成!")
    print("推荐使用: standard_6col.node")
    print("如果仍有问题，请尝试: large_6col.node")

if __name__ == "__main__":
    create_correct_6col_node() 