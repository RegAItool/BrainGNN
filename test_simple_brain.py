#!/usr/bin/env python3
"""
创建一个简单的测试大脑形状，确保ParaView可以正常显示
"""

import numpy as np
import vtk
import os

def create_simple_brain_surface():
    """创建简单但真实的大脑形状"""
    
    print("🧠 Creating simple brain surface for testing...")
    
    # 创建一个椭球体作为基础，然后变形成大脑形状
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(70.0)
    sphere.SetPhiResolution(50)
    sphere.SetThetaResolution(50)
    sphere.Update()
    
    # 获取球体的点
    sphere_mesh = sphere.GetOutput()
    points = sphere_mesh.GetPoints()
    n_points = points.GetNumberOfPoints()
    
    # 创建新的点数组来存储变形后的坐标
    new_points = vtk.vtkPoints()
    activation_values = vtk.vtkFloatArray()
    activation_values.SetName("PainActivation")
    
    # 脑区数据
    brain_regions = {
        'Cerebelum_Crus1_R': {'coords': [28, -77, -33], 'activation': 0.601},
        'Cerebelum_Crus1_L': {'coords': [-28, -77, -33], 'activation': 0.438},
        'Occipital_Mid_R': {'coords': [31, -87, 11], 'activation': 0.528},
        'Frontal_Sup_L': {'coords': [-15, 26, 56], 'activation': -0.512},
        'Frontal_Mid_L': {'coords': [-30, 47, 28], 'activation': -0.498},
        'Precentral_L': {'coords': [-39, -6, 52], 'activation': -0.433}
    }
    
    # 变形每个点使其更像大脑
    for i in range(n_points):
        point = points.GetPoint(i)
        x, y, z = point
        
        # 大脑形状变形
        # 1. 前后拉长
        y *= 1.2
        
        # 2. 左右稍微压缩
        x *= 0.95
        
        # 3. 上下压缩
        z *= 0.8
        
        # 4. 前额叶突出
        if y > 40:
            y *= 1.1
            z *= 0.9
        
        # 5. 后脑勺变形
        if y < -50:
            y *= 1.05
            z *= 0.85
        
        # 6. 颞叶下垂
        if abs(x) > 40 and z < 0:
            z -= 10
        
        new_points.InsertNextPoint(x, y, z)
        
        # 计算激活值（基于最近脑区）
        min_distance = float('inf')
        activation = 0.0
        
        for region_name, region_data in brain_regions.items():
            region_coords = region_data['coords']
            distance = np.sqrt((x - region_coords[0])**2 + 
                             (y - region_coords[1])**2 + 
                             (z - region_coords[2])**2)
            
            if distance < min_distance:
                min_distance = distance
                # 距离衰减
                decay = np.exp(-distance / 30.0)
                activation = region_data['activation'] * decay
        
        activation_values.InsertNextValue(activation)
    
    # 创建新的mesh
    brain_mesh = vtk.vtkPolyData()
    brain_mesh.SetPoints(new_points)
    brain_mesh.SetPolys(sphere_mesh.GetPolys())  # 使用原始球体的连接关系
    brain_mesh.GetPointData().SetScalars(activation_values)
    
    # 保存为VTK文件
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName("./paraview_data/simple_brain_surface.vtk")
    writer.SetInputData(brain_mesh)
    writer.Write()
    
    print("✅ Simple brain surface saved: ./paraview_data/simple_brain_surface.vtk")
    return brain_mesh

def create_test_script():
    """创建测试脚本"""
    
    script_content = '''
# Simple Brain Test Script for ParaView
from paraview.simple import *

print("Loading simple brain surface...")

# Create render view
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1200, 800]
renderView1.Background = [0.1, 0.1, 0.1]

# Load simple brain surface
try:
    brain_surface = LegacyVTKReader(FileNames=['./paraview_data/simple_brain_surface.vtk'])
    brain_display = Show(brain_surface, renderView1)
    brain_display.Representation = 'Surface'
    
    # Set coloring
    brain_display.ColorArrayName = ['POINTS', 'PainActivation']
    
    # Get color map
    lut = GetColorTransferFunction('PainActivation')
    lut.ApplyPreset('Cool to Warm', True)
    
    # Reset camera to fit data
    renderView1.ResetCamera()
    
    # Set a good viewing angle
    camera = GetActiveCamera()
    camera.SetPosition([150, -100, 100])
    camera.SetFocalPoint([0, 0, 0])
    camera.SetViewUp([0, 0, 1])
    
    Render()
    
    print("SUCCESS: Brain surface loaded and visible!")
    print("Use mouse to rotate and zoom")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Check if file exists and is readable")
'''
    
    with open('./paraview_data/test_brain_script.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Test script saved: ./paraview_data/test_brain_script.py")

def main():
    """主函数"""
    print("🔧 Creating test brain surface...")
    
    # 确保目录存在
    os.makedirs('./paraview_data', exist_ok=True)
    
    # 创建简单大脑表面
    create_simple_brain_surface()
    
    # 创建测试脚本
    create_test_script()
    
    print("\n🎯 Test files created!")
    print("📂 Files:")
    print("  • simple_brain_surface.vtk")
    print("  • test_brain_script.py")
    
    print("\n🚀 Now try this:")
    print("1. paraview")
    print("2. File → Open → simple_brain_surface.vtk")
    print("3. Click Apply")
    print("4. Properties → Coloring → PainActivation")
    print("5. Should see brain shape with colors!")

if __name__ == "__main__":
    main()