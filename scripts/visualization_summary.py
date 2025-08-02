#!/usr/bin/env python3
"""
大脑可视化总结
展示所有生成的真实大脑形状可视化文件
"""

import os
import glob
from datetime import datetime

def list_visualization_files():
    """列出所有可视化文件"""
    print("🧠 BrainGNN 真实大脑形状可视化总结")
    print("=" * 60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 查找所有PNG文件
    png_files = glob.glob("*.png")
    brain_files = [f for f in png_files if any(keyword in f.lower() for keyword in ['brain', 'real', 'final', 'atlas'])]
    
    print(f"📁 找到 {len(brain_files)} 个大脑可视化文件:")
    print()
    
    # 按类型分类
    categories = {
        "真实大脑形状图": [f for f in brain_files if 'real' in f.lower() and 'brain' in f.lower()],
        "最终大脑可视化": [f for f in brain_files if 'final' in f.lower()],
        "高级大脑分析": [f for f in brain_files if 'advanced' in f.lower() or 'comprehensive' in f.lower()],
        "Atlas映射图": [f for f in brain_files if 'atlas' in f.lower()],
        "3D大脑图": [f for f in brain_files if '3d' in f.lower()],
        "其他大脑图": [f for f in brain_files if not any(keyword in f.lower() for keyword in ['real', 'final', 'advanced', 'comprehensive', 'atlas', '3d'])]
    }
    
    for category, files in categories.items():
        if files:
            print(f"📊 {category}:")
            for file in sorted(files):
                size = os.path.getsize(file) / 1024  # KB
                print(f"   • {file} ({size:.1f} KB)")
            print()
    
    return brain_files

def show_file_info():
    """显示文件详细信息"""
    print("📋 文件详细信息:")
    print("-" * 40)
    
    brain_files = glob.glob("*brain*.png") + glob.glob("*real*.png") + glob.glob("*atlas*.png")
    
    for file in sorted(brain_files):
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            mtime = datetime.fromtimestamp(os.path.getmtime(file))
            print(f"📄 {file}")
            print(f"   大小: {size:.1f} KB")
            print(f"   修改时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

def show_usage_instructions():
    """显示使用说明"""
    print("🎯 使用说明:")
    print("-" * 40)
    print("1. 真实大脑形状可视化:")
    print("   • final_real_brain_visualization.png - 最终真实大脑形状图")
    print("   • advanced_brain_shape_visualization.png - 高级大脑形状图")
    print("   • real_brain_shape_visualization.png - 基础真实大脑形状图")
    print()
    print("2. 大脑分析图:")
    print("   • comprehensive_brain_analysis.png - 综合大脑分析")
    print("   • brain_region_analysis.png - 脑区分析")
    print("   • detailed_brain_visualization.png - 详细大脑可视化")
    print()
    print("3. Atlas映射图:")
    print("   • final_brain_atlas_mapping.png - 最终Atlas映射")
    print("   • brain_atlas_mapping_real.png - 真实Atlas映射")
    print("   • brain_atlas_visualization.png - 基础Atlas可视化")
    print()
    print("4. 3D可视化:")
    print("   • 3d_brain_visualization.png - 3D大脑可视化")
    print("   • real_brain_atlas_3d.png - 真实3D大脑Atlas")
    print()
    print("5. 其他可视化:")
    print("   • brain_importance_heatmap.png - 重要性热力图")
    print("   • brain_outline_visualization.png - 大脑轮廓图")
    print()

def show_model_performance():
    """显示模型性能信息"""
    print("📈 BrainGNN 模型性能:")
    print("-" * 40)
    print("• 测试准确率: 52.2%")
    print("• 训练准确率: ~83% (存在过拟合)")
    print("• ROI数量: 100个")
    print("• 数据集: ABIDE resting-state fMRI")
    print("• 模型: BrainGNN with Graph Pooling")
    print()

def main():
    """主函数"""
    print("🚀 BrainGNN 真实大脑形状可视化总结")
    print("=" * 60)
    
    # 显示模型性能
    show_model_performance()
    
    # 列出可视化文件
    brain_files = list_visualization_files()
    
    # 显示文件信息
    show_file_info()
    
    # 显示使用说明
    show_usage_instructions()
    
    print("✅ 总结完成！")
    print("🎉 现在你有了真实的大脑形状可视化，而不是简单的圆圈！")
    print("📁 所有文件都保存在当前目录中。")

if __name__ == '__main__':
    main() 