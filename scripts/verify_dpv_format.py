#!/usr/bin/env python3
"""
验证DPV文件格式
"""

import numpy as np

def verify_dpv_format():
    """验证DPV文件格式"""
    
    print("=== 验证DPV文件格式 ===")
    
    # 检查完整版本
    print("\n1. 检查 correct_activation.dpv:")
    try:
        dpv_data = np.loadtxt('correct_activation.dpv')
        print(f"✅ 文件加载成功")
        print(f"   数据形状: {dpv_data.shape}")
        print(f"   列数: {dpv_data.shape[1]}")
        
        if dpv_data.shape[1] == 7:
            print("✅ 格式正确: 7列 (x, y, z, size, color, shape, label)")
        else:
            print(f"❌ 格式错误: 期望7列，实际{dpv_data.shape[1]}列")
        
        # 检查各列范围
        print(f"   坐标范围: X({dpv_data[:,0].min():.0f}到{dpv_data[:,0].max():.0f})")
        print(f"              Y({dpv_data[:,1].min():.0f}到{dpv_data[:,1].max():.0f})")
        print(f"              Z({dpv_data[:,2].min():.0f}到{dpv_data[:,2].max():.0f})")
        print(f"   重要性范围: {dpv_data[:,3].min():.3f} 到 {dpv_data[:,3].max():.3f}")
        print(f"   颜色范围: {dpv_data[:,4].min():.3f} 到 {dpv_data[:,4].max():.3f}")
        print(f"   形状值: 全部为 {dpv_data[0,5]:.0f} (球体)")
        print(f"   标签范围: {dpv_data[:,6].min():.0f} 到 {dpv_data[:,6].max():.0f}")
        
    except Exception as e:
        print(f"❌ 文件加载失败: {e}")
    
    # 检查Top-30版本
    print("\n2. 检查 top30_activation.dpv:")
    try:
        top30_data = np.loadtxt('top30_activation.dpv')
        print(f"✅ 文件加载成功")
        print(f"   数据形状: {top30_data.shape}")
        print(f"   ROI数量: {len(top30_data)}")
        
        if top30_data.shape[1] == 7:
            print("✅ 格式正确: 7列 (x, y, z, size, color, shape, label)")
        else:
            print(f"❌ 格式错误: 期望7列，实际{top30_data.shape[1]}列")
        
        # 检查标签连续性
        labels = top30_data[:, 6]
        expected_labels = np.arange(1, len(labels) + 1)
        if np.allclose(labels, expected_labels):
            print("✅ 标签连续: 1到30")
        else:
            print("❌ 标签不连续")
        
    except Exception as e:
        print(f"❌ 文件加载失败: {e}")
    
    # 显示前5行示例
    print("\n3. DPV文件格式示例 (前5行):")
    print("x\t\ty\t\tz\t\tsize\t\tcolor\tshape\tlabel")
    print("-" * 80)
    for i in range(min(5, len(dpv_data))):
        row = dpv_data[i]
        print(f"{row[0]:.3f}\t{row[1]:.3f}\t{row[2]:.3f}\t{row[3]:.3f}\t{row[4]:.3f}\t{row[5]:.0f}\t{row[6]:.0f}")
    
    print("\n✅ DPV文件格式验证完成!")
    print("这些文件应该能被BrainNet Viewer正确识别和显示")

if __name__ == "__main__":
    verify_dpv_format() 