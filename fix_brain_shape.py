#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复大脑形状 - 创建真实的大脑模型
Fix Brain Shape - Create Realistic Brain Model
"""

import numpy as np
import os
from pathlib import Path

def create_realistic_brain_ply():
    """创建真实的大脑PLY模型"""
    
    print("🧠 创建真实大脑形状...")
    
    # 更精细的参数
    phi = np.linspace(0, np.pi, 50)  # 增加分辨率
    theta = np.linspace(0, 2*np.pi, 100)
    
    vertices = []
    faces = []
    
    for i, p in enumerate(phi):
        for j, t in enumerate(theta):
            # 基础椭球参数 (更真实的大脑比例)
            a, b, c = 85, 110, 70  # 左右、前后、上下
            
            # 基础椭球坐标
            x = a * np.sin(p) * np.cos(t)
            y = b * np.sin(p) * np.sin(t)
            z = c * np.cos(p)
            
            # 大脑形状修正 - 更真实的解剖结构
            
            # 1. 前额叶突出 (额叶)
            if y > 60:  # 前部
                y *= 1.3  # 更突出
                z *= 0.8  # 稍微压扁
                if z > 20:
                    z *= 0.9
            
            # 2. 颞叶下垂和侧面突出
            if abs(x) > 60 and z < 20 and abs(y) < 40:
                z -= 35  # 向下延伸
                x *= 1.25  # 侧面更宽
                if x > 0:
                    x += 10
                else:
                    x -= 10
            
            # 3. 枕叶后突 (后脑勺)
            if y < -80:  # 后部
                y *= 1.15
                z *= 0.95
                if abs(x) < 40:  # 中线区域更突出
                    y *= 1.1
            
            # 4. 顶叶圆弧 (头顶)
            if z > 40:
                z *= 1.1  # 头顶更圆
                if abs(x) < 50 and abs(y) < 30:
                    z *= 1.15  # 正顶部最高
            
            # 5. 脑干和小脑区域 (底部)
            if z < -30:
                z *= 0.7  # 底部收窄
                if abs(x) < 30 and y > -40:  # 脑干区域
                    x *= 0.8
                    y *= 0.8
            
            # 6. 左右半球分离的暗示 (纵裂)
            if abs(x) < 3 and z > 0:  # 中线附近
                z *= 0.98  # 轻微凹陷
            
            # 7. 侧脑室区域 (轻微内凹)
            if abs(x) > 20 and abs(x) < 40 and abs(y) < 20 and z > 10:
                distance_from_center = np.sqrt((abs(x)-30)**2 + y**2 + (z-25)**2)
                if distance_from_center < 20:
                    factor = 0.95 - 0.05 * np.exp(-distance_from_center/10)
                    x *= factor
                    y *= factor
                    z *= factor
            
            # 8. 增加表面粗糙度 (皮层沟回)
            noise_scale = 2.0
            noise_x = noise_scale * np.sin(4*p) * np.cos(6*t)
            noise_y = noise_scale * np.cos(3*p) * np.sin(5*t)  
            noise_z = noise_scale * np.sin(5*p) * np.cos(4*t)
            
            x += noise_x
            y += noise_y
            z += noise_z
            
            vertices.append([x, y, z])
            
            # 创建三角面
            if i < len(phi)-1 and j < len(theta)-1:
                v1 = i * len(theta) + j
                v2 = i * len(theta) + (j + 1) % len(theta)
                v3 = (i + 1) * len(theta) + j
                v4 = (i + 1) * len(theta) + (j + 1) % len(theta)
                
                # 两个三角形组成一个四边形
                faces.append([3, v1, v2, v3])
                faces.append([3, v2, v4, v3])
    
    # 保存为PLY文件
    ply_path = "./figures/surfice_templates/realistic_brain.ply"
    
    with open(ply_path, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment Created by BrainGNN - Realistic Brain Model\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write(f"element face {len(faces)}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")
        
        # 写入顶点
        for v in vertices:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        
        # 写入面
        for face in faces:
            f.write(f"{face[0]} {face[1]} {face[2]} {face[3]}\n")
    
    file_size = os.path.getsize(ply_path) / 1024
    print(f"✅ 真实大脑PLY创建: {ply_path} ({file_size:.1f} KB)")
    
    return ply_path

def create_anatomical_brain_obj():
    """创建解剖学正确的OBJ大脑"""
    
    print("🧠 创建解剖学OBJ大脑...")
    
    # 使用更真实的大脑轮廓数据点
    brain_landmarks = [
        # 前额叶关键点
        [0, 100, 45], [30, 95, 40], [-30, 95, 40],
        [50, 85, 25], [-50, 85, 25],
        
        # 顶叶关键点  
        [0, 20, 75], [40, 10, 70], [-40, 10, 70],
        [60, 20, 50], [-60, 20, 50],
        
        # 枕叶关键点
        [0, -95, 35], [25, -90, 30], [-25, -90, 30],
        [45, -85, 15], [-45, -85, 15],
        
        # 颞叶关键点
        [70, 30, -10], [-70, 30, -10],
        [75, 0, -15], [-75, 0, -15],
        [70, -30, -20], [-70, -30, -20],
        
        # 底部和脑干
        [0, 20, -40], [20, 10, -45], [-20, 10, -45],
        [0, -20, -35], [15, -30, -40], [-15, -30, -40]
    ]
    
    # 使用关键点生成更多顶点
    vertices = []
    
    # 基于关键点插值生成完整表面
    phi_vals = np.linspace(0, np.pi, 40)
    theta_vals = np.linspace(0, 2*np.pi, 80)
    
    for p in phi_vals:
        for t in theta_vals:
            # 基础形状
            a, b, c = 80, 105, 65
            x = a * np.sin(p) * np.cos(t)
            y = b * np.sin(p) * np.sin(t)
            z = c * np.cos(p)
            
            # 基于关键点调整形状
            for landmark in brain_landmarks:
                lx, ly, lz = landmark
                distance = np.sqrt((x-lx)**2 + (y-ly)**2 + (z-lz)**2)
                if distance < 50:  # 影响半径
                    influence = np.exp(-distance/25)
                    # 向关键点方向调整
                    x += (lx - x) * influence * 0.1
                    y += (ly - y) * influence * 0.1  
                    z += (lz - z) * influence * 0.1
            
            vertices.append([x, y, z])
    
    # 生成面
    faces = []
    rows, cols = len(phi_vals), len(theta_vals)
    
    for i in range(rows-1):
        for j in range(cols-1):
            v1 = i * cols + j
            v2 = i * cols + (j + 1) % cols
            v3 = (i + 1) * cols + j
            v4 = (i + 1) * cols + (j + 1) % cols
            
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
    
    # 保存OBJ文件
    obj_path = "./figures/surfice_templates/realistic_brain.obj"
    
    with open(obj_path, 'w') as f:
        f.write("# Realistic Brain Model for SurfIce\n")
        f.write("# Generated by BrainGNN - Anatomically Correct\n\n")
        
        # 写入顶点
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        
        # 写入面 (OBJ格式索引从1开始)
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
    
    file_size = os.path.getsize(obj_path) / 1024
    print(f"✅ 真实大脑OBJ创建: {obj_path} ({file_size:.1f} KB)")
    
    return obj_path

def diagnose_original_brain():
    """诊断原始大脑文件问题"""
    
    print("🔍 诊断原始brain_fixed.ply问题...")
    
    original_file = "./figures/surfice_templates/brain_fixed.ply"
    
    if not os.path.exists(original_file):
        print("❌ 原始文件不存在")
        return
    
    try:
        with open(original_file, 'r') as f:
            lines = f.readlines()
        
        print(f"📋 文件总行数: {len(lines)}")
        print(f"📋 文件头: {lines[:10]}")
        
        # 找到顶点数量
        vertex_count = 0
        face_count = 0
        
        for line in lines:
            if line.startswith("element vertex"):
                vertex_count = int(line.split()[-1])
            elif line.startswith("element face"):
                face_count = int(line.split()[-1])
        
        print(f"📊 顶点数量: {vertex_count}")
        print(f"📊 面数量: {face_count}")
        
        # 检查第一个顶点坐标
        in_vertices = False
        vertex_lines = []
        
        for line in lines:
            if line.strip() == "end_header":
                in_vertices = True
                continue
            if in_vertices and len(vertex_lines) < 5:
                vertex_lines.append(line.strip())
        
        print(f"📊 前5个顶点:")
        for i, vline in enumerate(vertex_lines):
            print(f"   顶点{i+1}: {vline}")
        
        # 分析坐标范围
        x_coords, y_coords, z_coords = [], [], []
        
        for line in vertex_lines[:100]:  # 分析前100个顶点
            if line and not line.startswith('3'):  # 不是面数据
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                        x_coords.append(x)
                        y_coords.append(y)
                        z_coords.append(z)
                    except:
                        pass
        
        if x_coords:
            print(f"📊 坐标范围分析:")
            print(f"   X: {min(x_coords):.1f} 到 {max(x_coords):.1f}")
            print(f"   Y: {min(y_coords):.1f} 到 {max(y_coords):.1f}")
            print(f"   Z: {min(z_coords):.1f} 到 {max(z_coords):.1f}")
            
            # 判断问题
            z_range = max(z_coords) - min(z_coords)
            if z_range < 50:
                print("❌ 问题发现: Z轴范围太小，大脑被压扁成帽子状")
            
            if max(z_coords) < 0:
                print("❌ 问题发现: 大脑可能翻转了")
    
    except Exception as e:
        print(f"❌ 诊断错误: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 修复大脑形状问题")
    print("🎯 创建真实的大脑模型")
    print("=" * 60)
    
    # 1. 诊断原始文件问题
    diagnose_original_brain()
    
    print("\n" + "-" * 40)
    
    # 2. 创建真实的大脑模型
    realistic_ply = create_realistic_brain_ply()
    realistic_obj = create_anatomical_brain_obj()
    
    print("\n" + "=" * 60)
    print("✅ 大脑形状修复完成!")
    print("")
    print("🧠 新的真实大脑模型:")
    print(f"  📁 PLY格式: {realistic_ply}")
    print(f"  📁 OBJ格式: {realistic_obj}")
    print("")
    print("🎯 在SurfIce中使用:")
    print("  1. File → Open → realistic_brain.ply")
    print("  2. Overlay → Add → braingnn_pain_activation.nii.gz")
    print("")
    print("🧠 这次应该显示真正的大脑，不是帽子!")
    print("=" * 60)

if __name__ == "__main__":
    main()