#!/usr/bin/env python3
"""
验证BrainNet Viewer文件
检查所有生成的文件是否正确
"""

import os
import json
import numpy as np
from datetime import datetime

def verify_brainnet_files():
    """验证BrainNet Viewer文件"""
    print("🔍 验证BrainNet Viewer文件...")
    print("=" * 50)
    
    # 检查必需的文件
    required_files = [
        'bridge_nodes.node',
        'bridge_edges.edge', 
        'brainnet_data_info.json',
        'simple_brainnet_script.m',
        'brainnet_bridge.m',
        'brainnet_visualization.m',
        'advanced_brainnet_visualization.m'
    ]
    
    print("📁 检查必需文件:")
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} - 缺失")
            all_files_exist = False
    
    print("\n📊 验证数据文件:")
    
    # 检查节点文件
    if os.path.exists('bridge_nodes.node'):
        try:
            nodes = np.loadtxt('bridge_nodes.node')
            print(f"   ✅ 节点文件: {nodes.shape[0]} 个节点")
            print(f"      坐标范围: X[{nodes[:,0].min():.2f}, {nodes[:,0].max():.2f}]")
            print(f"                Y[{nodes[:,1].min():.2f}, {nodes[:,1].max():.2f}]")
            print(f"                Z[{nodes[:,2].min():.2f}, {nodes[:,2].max():.2f}]")
            print(f"      大小范围: [{nodes[:,3].min():.2f}, {nodes[:,3].max():.2f}]")
            print(f"      颜色范围: [{nodes[:,4].min():.2f}, {nodes[:,4].max():.2f}]")
        except Exception as e:
            print(f"   ❌ 节点文件格式错误: {e}")
    
    # 检查边文件
    if os.path.exists('bridge_edges.edge'):
        try:
            edges = np.loadtxt('bridge_edges.edge')
            print(f"   ✅ 边文件: {edges.shape[0]} 条边")
            print(f"      权重范围: [{edges[:,2].min():.2f}, {edges[:,2].max():.2f}]")
        except Exception as e:
            print(f"   ❌ 边文件格式错误: {e}")
    
    # 检查数据信息
    if os.path.exists('brainnet_data_info.json'):
        try:
            with open('brainnet_data_info.json', 'r') as f:
                data_info = json.load(f)
            print(f"   ✅ 数据信息: {data_info['roi_count']} 个ROI")
            print(f"      最大重要性: {data_info['max_importance']:.4f}")
            print(f"      平均重要性: {data_info['mean_importance']:.4f}")
        except Exception as e:
            print(f"   ❌ 数据信息文件错误: {e}")
    
    # 检查BrainNet Viewer
    brainnet_path = './imports/BrainNetViewer_20191031'
    if os.path.exists(brainnet_path):
        print(f"   ✅ BrainNet Viewer: {brainnet_path}")
        brainnet_files = os.listdir(brainnet_path)
        print(f"      包含 {len(brainnet_files)} 个文件")
    else:
        print(f"   ❌ BrainNet Viewer: {brainnet_path} - 未找到")
    
    print("\n🎯 使用说明:")
    print("=" * 50)
    
    if all_files_exist:
        print("✅ 所有文件都已正确生成！")
        print("\n📝 使用方法:")
        print("1. 打开MATLAB")
        print("2. 切换到工作目录:")
        print("   cd('/Users/hanyu/Documents/BrainGNN_Pytorch-main')")
        print("3. 运行脚本:")
        print("   run('simple_brainnet_script.m')")
        print("\n或者使用BrainNet GUI:")
        print("1. addpath('./imports/BrainNetViewer_20191031');")
        print("2. BrainNet;")
        print("3. 在GUI中加载 bridge_nodes.node 和 bridge_edges.edge")
        
        print("\n📈 预期结果:")
        print("- brainnet_simple_visualization.png (BrainNet可视化)")
        print("- brainnet_3d_scatter.png (3D散点图)")
        
        print("\n🎉 现在可以生成专业的大脑网络可视化了！")
    else:
        print("❌ 部分文件缺失，请重新运行 brainnet_visualization.py")
    
    print("\n📅 验证时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    verify_brainnet_files() 