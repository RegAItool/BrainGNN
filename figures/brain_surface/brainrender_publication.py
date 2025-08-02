
#!/usr/bin/env python3
"""
Brainrender 3D Visualization for BrainGNN Pain Analysis
High-quality 3D brain rendering for publications
"""

import numpy as np
from brainrender import Scene
from brainrender.actors import Points, Spheres
import pandas as pd

def create_publication_brainrender():
    """创建发表质量的Brainrender可视化"""
    
    # 创建场景
    scene = Scene(
        title="BrainGNN Pain State Analysis (98.7% Accuracy)",
        atlas_name="allen_mouse_25um",  # 或者使用人脑图谱
        root=True,
        add_root=True,
    )
    
    # BrainGNN脑区数据
    pain_regions = {
        'Cerebelum_Crus1_R': {'coords': [28, -77, -33], 'activation': 0.601, 'network': 'sensorimotor'},
        'Cerebelum_Crus1_L': {'coords': [-28, -77, -33], 'activation': 0.438, 'network': 'sensorimotor'},
        'Occipital_Mid_R': {'coords': [31, -87, 11], 'activation': 0.528, 'network': 'visual'},
        'Occipital_Sup_R': {'coords': [20, -93, 15], 'activation': 0.528, 'network': 'visual'},
        'Occipital_Mid_L': {'coords': [-31, -87, 11], 'activation': 0.385, 'network': 'visual'},
        'ParaHippocampal_L': {'coords': [-24, -7, -21], 'activation': 0.120, 'network': 'limbic'},
        'Amygdala_R': {'coords': [25, -1, -20], 'activation': 0.080, 'network': 'limbic'},
        'Frontal_Sup_L': {'coords': [-15, 26, 56], 'activation': -0.512, 'network': 'executive'},
        'Frontal_Mid_L': {'coords': [-30, 47, 28], 'activation': -0.498, 'network': 'executive'},
        'Precentral_L': {'coords': [-39, -6, 52], 'activation': -0.433, 'network': 'motor'},
        'Postcentral_L': {'coords': [-43, -25, 49], 'activation': -0.431, 'network': 'somatosensory'},
        'Rolandic_Oper_L': {'coords': [-50, 0, 9], 'activation': -0.401, 'network': 'sensorimotor'},
        'Frontal_Sup_R': {'coords': [15, 26, 56], 'activation': -0.394, 'network': 'executive'},
        'Putamen_R': {'coords': [26, 6, 0], 'activation': -0.386, 'network': 'subcortical'}
    }
    
    # 网络颜色
    network_colors = {
        'sensorimotor': 'red',
        'visual': 'orange', 
        'executive': 'blue',
        'motor': 'lightblue',
        'somatosensory': 'cyan',
        'limbic': 'purple',
        'subcortical': 'green'
    }
    
    # 添加脑区球体
    for region_name, region_data in pain_regions.items():
        coords = region_data['coords']
        activation = region_data['activation']
        network = region_data['network']
        
        # 球体大小基于激活强度
        radius = max(2, abs(activation) * 8)
        
        # 颜色基于网络类型和激活方向
        if activation > 0:
            color = 'red'  # 疼痛激活
            alpha = 0.8
        else:
            color = 'blue'  # 疼痛抑制  
            alpha = 0.8
        
        # 添加球体
        sphere = scene.add_sphere_at_point(
            pos=coords,
            radius=radius,
            color=color,
            alpha=alpha
        )
    
    # 设置相机视角
    scene.render(
        camera='sagittal',  # 矢状面视角
        zoom=1.5,
        interactive=False
    )
    
    # 保存高分辨率图像
    scene.screenshot(
        name='./figures/publication/brainrender_3d_pain_mapping.png',
        scale=4  # 4倍分辨率
    )
    
    print("✅ Brainrender 3D visualization completed!")
    print("📸 High-resolution 3D image saved!")

if __name__ == "__main__":
    create_publication_brainrender()
