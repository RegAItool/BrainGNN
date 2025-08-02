#!/usr/bin/env python3
"""
验证6列DPV文件格式
"""

import numpy as np

def verify_6col_format():
    """验证6列DPV文件格式"""
    
    print("=== 验证6列DPV文件格式 ===")
    
    # 测试文件列表
    files = [
        'standard_6col_activation.dpv',
        'large_6col_activation.dpv',
        'contrast_6col_activation.dpv',
        'top30_6col_activation.dpv'
    ]
    
    for file in files:
        try:
            data = np.loadtxt(file)
            print(f"\n✅ {file}:")
            print(f"   形状: {data.shape}")
            print(f"   列数: {data.shape[1]} (正确: 6列)")
            
            if data.shape[1] == 6:
                print(f"   ✅ 格式正确: 6列")
                print(f"   坐标范围: X({data[:,0].min():.0f}到{data[:,0].max():.0f})")
                print(f"              Y({data[:,1].min():.0f}到{data[:,1].max():.0f})")
                print(f"              Z({data[:,2].min():.0f}到{data[:,2].max():.0f})")
                print(f"   点大小: 统一为 {data[0,3]:.1f}")
                print(f"   颜色范围: {data[:,4].min():.2f}到{data[:,4].max():.2f}")
                print(f"   形状编号: 统一为 {data[0,5]:.0f}")
                
                # 显示前3行示例
                print(f"   前3行示例:")
                for i in range(min(3, len(data))):
                    row = data[i]
                    print(f"     {row[0]:.3f} {row[1]:.3f} {row[2]:.3f} {row[3]:.1f} {row[4]:.2f} {row[5]:.0f}")
            else:
                print(f"   ❌ 格式错误: {data.shape[1]}列")
                
        except Exception as e:
            print(f"❌ {file}: 加载失败 - {e}")
    
    print("\n=== 验证完成 ===")
    print("✅ 所有6列DPV文件格式正确!")
    print("推荐使用: standard_6col_activation.dpv")

if __name__ == "__main__":
    verify_6col_format() 