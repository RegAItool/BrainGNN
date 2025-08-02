#!/usr/bin/env python3
"""
DPV状态切换器
用于在不同状态之间切换显示
"""

import numpy as np
import time
import os

def switch_dpv_state(state_name):
    """切换到指定状态的DPV文件"""
    
    states = {
        'normal': 'dpv_state_normal.dpv',
        'high': 'dpv_state_high_activation.dpv', 
        'low': 'dpv_state_low_activation.dpv',
        'contrast': 'dpv_state_contrast.dpv',
        'progressive': 'dpv_state_progressive.dpv',
        'pulse': 'dpv_state_pulse.dpv'
    }
    
    if state_name not in states:
        print(f"❌ 未知状态: {state_name}")
        print(f"可用状态: {list(states.keys())}")
        return False
    
    filename = states[state_name]
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return False
    
    print(f"✅ 切换到状态: {state_name}")
    print(f"文件: {filename}")
    
    # 读取并显示状态信息
    info_file = f'dpv_state_{state_name}_info.txt'
    if os.path.exists(info_file):
        with open(info_file, 'r', encoding='utf-8') as f:
            print("
状态信息:")
            print(f.read())
    
    return True

def demo_state_transitions():
    """演示状态转换"""
    
    print("=== DPV状态转换演示 ===")
    
    states = ['normal', 'high', 'low', 'contrast', 'progressive', 'pulse']
    
    for state in states:
        print("
--- 切换到 {} 状态 ---".format(state))
        if switch_dpv_state(state):
            print("状态切换成功!")
            time.sleep(2)  # 等待2秒
        else:
            print("状态切换失败!")
    
    print("
✅ 状态转换演示完成!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行参数指定状态
        state = sys.argv[1]
        switch_dpv_state(state)
    else:
        # 交互式选择
        print("DPV状态切换器")
        print("可用状态:")
        print("  normal      - 正常状态")
        print("  high        - 高激活状态") 
        print("  low         - 低激活状态")
        print("  contrast    - 对比状态")
        print("  progressive - 渐进状态")
        print("  pulse       - 脉冲状态")
        print("  demo        - 演示所有状态")
        
        choice = input("
请选择状态 (或输入 'demo' 进行演示): ").strip()
        
        if choice == 'demo':
            demo_state_transitions()
        else:
            switch_dpv_state(choice)
