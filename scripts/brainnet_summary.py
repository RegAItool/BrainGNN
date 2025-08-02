#!/usr/bin/env python3
"""
BrainNet Viewer 总结
展示所有生成的文件和使用方法
"""

import os
import json
import numpy as np
from datetime import datetime

def show_brainnet_files():
    """显示BrainNet Viewer相关文件"""
    print("🧠 BrainNet Viewer 文件总结")
    print("=" * 60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # BrainNet Viewer相关文件
    brainnet_files = [
        'simple_brainnet_script.m',
        'brainnet_bridge.m',
        'brainnet_visualization.m',
        'advanced_brainnet_visualization.m',
        'bridge_nodes.node',
        'bridge_edges.edge',
        'brainnet_data_info.json',
        'BrainNet_Viewer_Instructions.md'
    ]
    
    print("📁 BrainNet Viewer 文件:")
    for file in brainnet_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"   ✅ {file} ({size:.1f} KB)")
        else:
            print(f"   ❌ {file} (未找到)")
    print()

def show_data_info():
    """显示数据信息"""
    print("📊 数据信息:")
    print("-" * 40)
    
    if os.path.exists('brainnet_data_info.json'):
        with open('brainnet_data_info.json', 'r') as f:
            data_info = json.load(f)
        
        print(f"• ROI总数: {data_info['roi_count']}")
        print(f"• 最大重要性: {data_info['max_importance']:.4f}")
        print(f"• 平均重要性: {data_info['mean_importance']:.4f}")
        print(f"• 前10个重要ROI: {data_info['top_rois']}")
        print(f"• 节点文件: {data_info['node_file']}")
        print(f"• 边文件: {data_info['edge_file']}")
    else:
        print("❌ 数据信息文件不存在")
    print()

def show_node_data():
    """显示节点数据"""
    print("📈 节点数据预览:")
    print("-" * 40)
    
    if os.path.exists('bridge_nodes.node'):
        with open('bridge_nodes.node', 'r') as f:
            lines = f.readlines()
        
        print("格式: x y z size color")
        print("前5个节点:")
        for i, line in enumerate(lines[:5]):
            parts = line.strip().split('\t')
            print(f"  节点{i+1}: x={parts[0]}, y={parts[1]}, z={parts[2]}, size={parts[3]}, color={parts[4]}")
    else:
        print("❌ 节点文件不存在")
    print()

def show_usage_instructions():
    """显示使用说明"""
    print("🎯 使用方法:")
    print("-" * 40)
    print("1. 打开MATLAB")
    print("2. 切换到工作目录:")
    print("   cd('/Users/hanyu/Documents/BrainGNN_Pytorch-main')")
    print("3. 运行脚本:")
    print("   run('simple_brainnet_script.m')")
    print()
    print("或者使用BrainNet GUI:")
    print("1. addpath('./imports/BrainNetViewer_20191031');")
    print("2. BrainNet;")
    print("3. 在GUI中加载 bridge_nodes.node 和 bridge_edges.edge")
    print()

def show_expected_results():
    """显示预期结果"""
    print("📈 预期结果:")
    print("-" * 40)
    print("运行后将生成:")
    print("• brainnet_simple_visualization.png - BrainNet Viewer可视化")
    print("• brainnet_3d_scatter.png - 3D散点图")
    print()
    print("特点:")
    print("• 真实的大脑形状")
    print("• 专业的网络可视化")
    print("• ROI重要性用颜色和大小表示")
    print("• 高质量输出，适合论文")
    print()

def show_troubleshooting():
    """显示故障排除"""
    print("🐛 故障排除:")
    print("-" * 40)
    print("问题1: BrainNet Viewer未找到")
    print("解决: addpath('./imports/BrainNetViewer_20191031');")
    print()
    print("问题2: 文件不存在")
    print("解决: 确保在正确目录中运行")
    print()
    print("问题3: MATLAB未安装")
    print("解决: 安装MATLAB或使用在线服务")
    print()

def show_advantages():
    """显示BrainNet Viewer的优势"""
    print("🎯 BrainNet Viewer 优势:")
    print("-" * 40)
    print("✅ 真实大脑形状 - 使用解剖学准确的大脑模板")
    print("✅ 专业可视化 - 专为大脑网络设计")
    print("✅ 多种视角 - 支持不同角度的可视化")
    print("✅ 高质量输出 - 适合论文和报告")
    print("✅ 标准化 - 符合神经影像学标准")
    print("✅ 交互式 - 支持GUI操作")
    print()

def main():
    """主函数"""
    print("🚀 BrainNet Viewer 总结")
    print("=" * 60)
    
    # 显示文件信息
    show_brainnet_files()
    
    # 显示数据信息
    show_data_info()
    
    # 显示节点数据
    show_node_data()
    
    # 显示使用说明
    show_usage_instructions()
    
    # 显示预期结果
    show_expected_results()
    
    # 显示优势
    show_advantages()
    
    # 显示故障排除
    show_troubleshooting()
    
    print("✅ BrainNet Viewer 总结完成！")
    print("🎉 现在你可以使用BrainNet Viewer生成专业的大脑网络可视化了！")
    print("📁 所有文件都已准备就绪，可以直接在MATLAB中使用。")

if __name__ == '__main__':
    main() 