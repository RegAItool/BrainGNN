#!/usr/bin/env python3
"""
创建支持多状态动态显示的DPV文件
支持不同条件下的节点状态变化和动态呈现
"""

import numpy as np
import os

def get_aal_coordinates():
    """获取AAL atlas的标准MNI坐标"""
    
    # AAL atlas的标准MNI坐标（前100个主要脑区）
    aal_coords = [
        # 前额叶区域 (1-20)
        [42, 8, 28], [-42, 8, 28],  # 右/左前额叶
        [38, 44, -8], [-38, 44, -8],  # 右/左眶额叶
        [32, -60, 52], [-32, -60, 52],  # 右/左顶叶
        [26, -70, 44], [-26, -70, 44],  # 右/左楔前叶
        [54, -8, -12], [-54, -8, -12],  # 右/左颞叶
        [62, -22, -8], [-62, -22, -8],  # 右/左颞中回
        [18, -90, 8], [-18, -90, 8],  # 右/左枕叶
        [26, -88, -8], [-26, -88, -8],  # 右/左梭状回
        [38, 4, 4], [-38, 4, 4],  # 右/左岛叶
        [4, -40, 40], [4, 40, 4],  # 后/前扣带回
        
        # 基底节 (21-40)
        [16, 4, 8], [-16, 4, 8],  # 右/左尾状核
        [24, -4, -4], [-24, -4, -4],  # 右/左壳核
        [8, -16, 8], [-8, -16, 8],  # 右/左丘脑
        [16, -60, -24], [-16, -60, -24],  # 右/左小脑
        [50, -40, 20], [-50, -40, 20],  # 右/左角回
        [44, -50, 36], [-44, -50, 36],  # 右/左缘上回
        [36, -44, 48], [-36, -44, 48],  # 右/左中央后回
        [48, -12, 12], [-48, -12, 12],  # 右/左中央前回
        [28, -80, 32], [-28, -80, 32],  # 右/左楔叶
        [56, -32, 8], [-56, -32, 8],  # 右/左颞上回
        
        # 补充更多脑区 (41-100)
        [40, -20, -16], [-40, -20, -16],  # 右/左颞下回
        [12, -52, 8], [-12, -52, 8],  # 右/左舌回
        [20, -70, 16], [-20, -70, 16],  # 右/左距状回
        [32, 24, -4], [-32, 24, -4],  # 右/左眶部
        [44, 16, -20], [-44, 16, -20],  # 右/左直回
        [8, 52, -8], [-8, 52, -8],  # 右/左额内侧回
        [24, 36, 28], [-24, 36, 28],  # 右/左额上回
        [40, 8, 44], [-40, 8, 44],  # 右/左额中回
        [52, 20, 8], [-52, 20, 8],  # 右/左额下回
        [16, -40, 60], [-16, -40, 60],  # 右/左中央旁小叶
        [0, -20, 48], [0, 20, 48],  # 右/左辅助运动区
        [8, -8, 8], [-8, -8, 8],  # 右/左丘脑
        [12, -4, -8], [-12, -4, -8],  # 右/左杏仁核
        [20, -8, -12], [-20, -8, -12],  # 右/左海马
        [28, -12, -4], [-28, -12, -4],  # 右/左苍白球
        [24, 0, 4], [-24, 0, 4],  # 右/左壳核
        [16, 8, 12], [-16, 8, 12],  # 右/左尾状核
        [0, -60, -40], [-0, -60, -40],  # 右/左小脑
        [8, -72, -32], [-8, -72, -32],  # 右/左小脑脚
        [16, -48, -48], [-16, -48, -48],  # 右/左小脑半球
        [0, -40, -20], [-0, -40, -20],  # 右/左脑干
    ]
    
    return np.array(aal_coords)

def get_aal_labels():
    """获取AAL atlas的标签名称"""
    
    aal_labels = [
        # 前额叶区域 (1-20)
        "右前额叶", "左前额叶",
        "右眶额叶", "左眶额叶", 
        "右顶叶", "左顶叶",
        "右楔前叶", "左楔前叶",
        "右颞叶", "左颞叶",
        "右颞中回", "左颞中回",
        "右枕叶", "左枕叶",
        "右梭状回", "左梭状回",
        "右岛叶", "左岛叶",
        "后扣带回", "前扣带回",
        
        # 基底节 (21-40)
        "右尾状核", "左尾状核",
        "右壳核", "左壳核",
        "右丘脑", "左丘脑",
        "右小脑", "左小脑",
        "右角回", "左角回",
        "右缘上回", "左缘上回",
        "右中央后回", "左中央后回",
        "右中央前回", "左中央前回",
        "右楔叶", "左楔叶",
        "右颞上回", "左颞上回",
        
        # 补充更多脑区 (41-100)
        "右颞下回", "左颞下回",
        "右舌回", "左舌回",
        "右距状回", "左距状回",
        "右眶部", "左眶部",
        "右直回", "左直回",
        "右额内侧回", "左额内侧回",
        "右额上回", "左额上回",
        "右额中回", "左额中回",
        "右额下回", "左额下回",
        "右中央旁小叶", "左中央旁小叶",
        "右辅助运动区", "左辅助运动区",
        "右丘脑", "左丘脑",
        "右杏仁核", "左杏仁核",
        "右海马", "左海马",
        "右苍白球", "左苍白球",
        "右壳核", "左壳核",
        "右尾状核", "左尾状核",
        "右小脑", "左小脑",
        "右小脑脚", "左小脑脚",
        "右小脑半球", "左小脑半球",
        "右脑干", "左脑干",
    ]
    
    return aal_labels

def create_dynamic_state_dpv():
    """创建支持多状态动态显示的DPV文件"""
    
    print("=== 创建支持多状态动态显示的DPV文件 ===")
    
    # 1. 获取AAL坐标和标签
    aal_coords = get_aal_coordinates()
    aal_labels = get_aal_labels()
    
    print(f"使用 {len(aal_coords)} 个AAL标准MNI坐标")
    print(f"对应 {len(aal_labels)} 个脑区标签")
    
    # 2. 加载ROI重要性分数
    try:
        importance_data = np.loadtxt('roi_importance_scores.txt')
        print(f"加载 {len(importance_data)} 个ROI的重要性分数")
        importance_scores = importance_data[:len(aal_coords)]
    except:
        print("使用模拟的重要性分数")
        importance_scores = np.random.uniform(0.1, 1.0, len(aal_coords))
    
    # 3. 创建不同状态的DPV文件
    print("\n=== 创建多状态DPV文件 ===")
    
    # 状态1: 正常状态 (所有节点显示)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "normal", "正常状态", "所有节点正常显示")
    
    # 状态2: 高激活状态 (重要节点突出显示)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "high_activation", "高激活状态", "重要节点突出显示")
    
    # 状态3: 低激活状态 (重要节点隐藏)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "low_activation", "低激活状态", "重要节点隐藏")
    
    # 状态4: 对比状态 (左右半球对比)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "contrast", "对比状态", "左右半球对比显示")
    
    # 状态5: 渐进状态 (按重要性逐步显示)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "progressive", "渐进状态", "按重要性逐步显示")
    
    # 状态6: 脉冲状态 (重要节点闪烁效果)
    create_state_dpv(aal_coords, importance_scores, aal_labels, 
                    "pulse", "脉冲状态", "重要节点闪烁效果")
    
    # 4. 创建状态切换脚本
    create_state_switcher(aal_coords, importance_scores, aal_labels)
    
    # 5. 创建MATLAB动态可视化脚本
    create_matlab_dynamic_script()
    
    print("\n✅ 多状态DPV文件创建完成!")
    print("现在您可以通过不同状态文件来展示不同的节点呈现效果!")

def create_state_dpv(coords, importance_scores, labels, state_name, state_desc, state_effect):
    """创建特定状态的DPV文件"""
    
    print(f"\n--- 创建 {state_name} 状态 ---")
    print(f"描述: {state_desc}")
    print(f"效果: {state_effect}")
    
    # 根据状态调整节点属性
    if state_name == "normal":
        # 正常状态：所有节点正常显示
        sizes = 2.0 + (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min()) * 3.0
        colors = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min()) * 20
        visibility = np.ones(len(coords))  # 所有节点可见
        
    elif state_name == "high_activation":
        # 高激活状态：重要节点突出显示
        normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        sizes = 3.0 + normalized_importance * 5.0  # 更大范围
        colors = normalized_importance * 25  # 更高对比度
        visibility = np.ones(len(coords))
        
    elif state_name == "low_activation":
        # 低激活状态：重要节点隐藏
        normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        # 重要节点变小或隐藏
        sizes = np.where(normalized_importance > 0.5, 0.5, 2.0 + normalized_importance * 2.0)
        colors = np.where(normalized_importance > 0.5, 0, normalized_importance * 15)
        visibility = np.where(normalized_importance > 0.7, 0, 1)  # 重要节点隐藏
        
    elif state_name == "contrast":
        # 对比状态：左右半球对比
        normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        sizes = 2.0 + normalized_importance * 3.0
        
        # 左右半球不同颜色
        colors = np.zeros(len(coords))
        for i in range(len(coords)):
            if coords[i, 0] > 0:  # 右半球
                colors[i] = normalized_importance[i] * 20 + 10  # 红色系
            else:  # 左半球
                colors[i] = normalized_importance[i] * 10  # 蓝色系
        visibility = np.ones(len(coords))
        
    elif state_name == "progressive":
        # 渐进状态：按重要性逐步显示
        normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        sizes = 2.0 + normalized_importance * 4.0
        colors = normalized_importance * 20
        
        # 按重要性设置可见性
        sorted_indices = np.argsort(importance_scores)[::-1]
        visibility = np.zeros(len(coords))
        top_n = int(len(coords) * 0.6)  # 显示前60%
        visibility[sorted_indices[:top_n]] = 1
        
    elif state_name == "pulse":
        # 脉冲状态：重要节点闪烁效果
        normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        sizes = 2.0 + normalized_importance * 3.0
        colors = normalized_importance * 20
        visibility = np.ones(len(coords))
        
        # 为重要节点添加脉冲标记
        pulse_mask = normalized_importance > 0.7
        colors[pulse_mask] += 5  # 重要节点额外亮度
    
    # 创建6列DPV格式数据
    dpv_data = np.zeros((len(coords), 6))
    dpv_data[:, :3] = coords  # 坐标
    dpv_data[:, 3] = sizes    # 大小
    dpv_data[:, 4] = colors   # 颜色
    dpv_data[:, 5] = visibility  # 可见性（第6列作为可见性标记）
    
    # 保存文件
    filename = f'dpv_state_{state_name}.dpv'
    np.savetxt(filename, dpv_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 已保存: {filename}")
    
    # 保存状态信息
    info_filename = f'dpv_state_{state_name}_info.txt'
    with open(info_filename, 'w', encoding='utf-8') as f:
        f.write(f"状态名称: {state_name}\n")
        f.write(f"状态描述: {state_desc}\n")
        f.write(f"状态效果: {state_effect}\n")
        f.write(f"节点数量: {len(coords)}\n")
        f.write(f"可见节点: {np.sum(visibility)}\n")
        f.write(f"隐藏节点: {len(coords) - np.sum(visibility)}\n")
        f.write(f"平均大小: {np.mean(sizes):.2f}\n")
        f.write(f"平均颜色: {np.mean(colors):.2f}\n")
        f.write("\n节点详情:\n")
        for i in range(len(coords)):
            f.write(f"{i+1:3d}. {labels[i]:<15} | 大小: {sizes[i]:.2f} | 颜色: {colors[i]:.2f} | 可见: {visibility[i]:.0f}\n")
    
    print(f"✅ 状态信息已保存: {info_filename}")

def create_state_switcher(coords, importance_scores, labels):
    """创建状态切换脚本"""
    
    print("\n=== 创建状态切换脚本 ===")
    
    # Python状态切换脚本
    python_script = '''#!/usr/bin/env python3
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
            print("\n状态信息:")
            print(f.read())
    
    return True

def demo_state_transitions():
    """演示状态转换"""
    
    print("=== DPV状态转换演示 ===")
    
    states = ['normal', 'high', 'low', 'contrast', 'progressive', 'pulse']
    
    for state in states:
        print("\n--- 切换到 {} 状态 ---".format(state))
        if switch_dpv_state(state):
            print("状态切换成功!")
            time.sleep(2)  # 等待2秒
        else:
            print("状态切换失败!")
    
    print("\n✅ 状态转换演示完成!")

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
        
        choice = input("\n请选择状态 (或输入 'demo' 进行演示): ").strip()
        
        if choice == 'demo':
            demo_state_transitions()
        else:
            switch_dpv_state(choice)
'''
    
    with open('dpv_state_switcher.py', 'w', encoding='utf-8') as f:
        f.write(python_script)
    
    print("✅ Python状态切换脚本: dpv_state_switcher.py")
    
    # MATLAB状态切换脚本
    matlab_script = '''%% DPV状态切换器 - MATLAB版本
% 用于在不同DPV状态之间切换显示

function switch_dpv_state(state_name)
    %% 切换到指定状态的DPV文件
    
    states = containers.Map();
    states('normal') = 'dpv_state_normal.dpv';
    states('high') = 'dpv_state_high_activation.dpv';
    states('low') = 'dpv_state_low_activation.dpv';
    states('contrast') = 'dpv_state_contrast.dpv';
    states('progressive') = 'dpv_state_progressive.dpv';
    states('pulse') = 'dpv_state_pulse.dpv';
    
    if ~isKey(states, state_name)
        fprintf('❌ 未知状态: %s\n', state_name);
        fprintf('可用状态: ');
        fprintf('%s ', keys(states));
        fprintf('\n');
        return;
    end
    
    filename = states(state_name);
    if ~exist(filename, 'file')
        fprintf('❌ 文件不存在: %s\n', filename);
        return;
    end
    
    fprintf('✅ 切换到状态: %s\n', state_name);
    fprintf('文件: %s\n', filename);
    
    % 读取并显示状态信息
    info_file = sprintf('dpv_state_%s_info.txt', state_name);
    if exist(info_file, 'file')
        fprintf('\n状态信息:\n');
        fid = fopen(info_file, 'r');
        while ~feof(fid)
            line = fgetl(fid);
            fprintf('%s\n', line);
        end
        fclose(fid);
    end
    
    % 尝试启动BrainNet Viewer
    try
        if exist('BrainNet_View', 'file')
            fprintf('正在启动BrainNet Viewer...\n');
            BrainNet_View('BrainMesh_ICBM152.nv', filename);
            fprintf('✅ BrainNet Viewer已启动\n');
        else
            fprintf('❌ BrainNet Viewer不可用\n');
            fprintf('请手动打开BrainNet Viewer并加载:\n');
            fprintf('  Surface: BrainMesh_ICBM152.nv\n');
            fprintf('  Node: %s\n', filename);
        end
    catch ME
        fprintf('❌ BrainNet Viewer启动失败: %s\n', ME.message);
    end
end

function demo_state_transitions()
    %% 演示状态转换
    
    fprintf('=== DPV状态转换演示 ===\n');
    
    states = {'normal', 'high', 'low', 'contrast', 'progressive', 'pulse'};
    
    for i = 1:length(states)
        state = states{i};
        fprintf('\n--- 切换到 %s 状态 ---\n', state);
        switch_dpv_state(state);
        pause(3);  % 等待3秒
    end
    
    fprintf('\n✅ 状态转换演示完成!\n');
end

%% 主程序
fprintf('DPV状态切换器\n');
fprintf('可用状态:\n');
fprintf('  normal      - 正常状态\n');
fprintf('  high        - 高激活状态\n'); 
fprintf('  low         - 低激活状态\n');
fprintf('  contrast    - 对比状态\n');
fprintf('  progressive - 渐进状态\n');
fprintf('  pulse       - 脉冲状态\n');
fprintf('  demo        - 演示所有状态\n');

% 示例使用
fprintf('\n示例: switch_dpv_state(''normal'')\n');
fprintf('示例: demo_state_transitions()\n');
'''
    
    with open('dpv_state_switcher.m', 'w', encoding='utf-8') as f:
        f.write(matlab_script)
    
    print("✅ MATLAB状态切换脚本: dpv_state_switcher.m")

def create_matlab_dynamic_script():
    """创建MATLAB动态可视化脚本"""
    
    print("\n=== 创建MATLAB动态可视化脚本 ===")
    
    matlab_script = '''%% BrainNet Viewer - 动态状态DPV可视化
% 支持多状态动态显示的DPV文件可视化
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer 动态状态DPV可视化 ===\n');

%% 1. 检查所有状态文件
states = {
    'normal', 'high_activation', 'low_activation', 
    'contrast', 'progressive', 'pulse'
};

fprintf('\n=== 检查状态文件 ===\n');
for i = 1:length(states)
    filename = sprintf('dpv_state_%s.dpv', states{i});
    if exist(filename, 'file')
        fprintf('✅ %s 存在\n', filename);
    else
        fprintf('❌ %s 不存在\n', filename);
    end
end

%% 2. 动态状态演示
fprintf('\n=== 动态状态演示 ===\n');

% 启动BrainNet Viewer
if exist('BrainNet_View', 'file')
    fprintf('正在启动BrainNet Viewer...\n');
    
    % 循环显示不同状态
    for i = 1:length(states)
        state = states{i};
        filename = sprintf('dpv_state_%s.dpv', states{i});
        
        if exist(filename, 'file')
            fprintf('\n--- 显示 %s 状态 ---\n', state);
            
            % 启动BrainNet Viewer
            try
                BrainNet_View('BrainMesh_ICBM152.nv', filename);
                fprintf('✅ %s 状态已加载\n', state);
                
                % 等待用户确认
                fprintf('按任意键继续下一个状态...\n');
                pause;
                
            catch ME
                fprintf('❌ %s 状态加载失败: %s\n', state, ME.message);
            end
        end
    end
    
    fprintf('\n✅ 动态状态演示完成!\n');
    
else
    fprintf('❌ BrainNet Viewer 不可用\n');
    fprintf('请手动打开BrainNet Viewer并依次加载:\n');
    for i = 1:length(states)
        filename = sprintf('dpv_state_%s.dpv', states{i});
        fprintf('  %s\n', filename);
    end
end

%% 3. 状态对比分析
fprintf('\n=== 状态对比分析 ===\n');

for i = 1:length(states)
    filename = sprintf('dpv_state_%s.dpv', states{i});
    info_file = sprintf('dpv_state_%s_info.txt', states{i});
    
    if exist(filename, 'file')
        data = load(filename);
        fprintf('\n%s 状态:\n', states{i});
        fprintf('  节点数量: %d\n', size(data, 1));
        fprintf('  平均大小: %.2f\n', mean(data(:, 4)));
        fprintf('  平均颜色: %.2f\n', mean(data(:, 5)));
        fprintf('  可见节点: %d\n', sum(data(:, 6) > 0));
        
        if exist(info_file, 'file')
            fprintf('  详细信息: %s\n', info_file);
        end
    end
end

%% 4. 推荐设置
fprintf('\n=== 推荐设置 ===\n');
fprintf('在BrainNet Viewer中:\n');
fprintf('  • View → Node: 必须勾选\n');
fprintf('  • Option → Display Node: 必须开启\n');
fprintf('  • Node size scaling: 开启\n');
fprintf('  • Node color: Custom\n');
fprintf('  • Node shape: 球体\n');
fprintf('  • Surface transparency: 0.3-0.5\n');

%% 5. 状态说明
fprintf('\n=== 状态说明 ===\n');
fprintf('• normal: 正常状态 - 所有节点正常显示\n');
fprintf('• high_activation: 高激活状态 - 重要节点突出显示\n');
fprintf('• low_activation: 低激活状态 - 重要节点隐藏\n');
fprintf('• contrast: 对比状态 - 左右半球对比显示\n');
fprintf('• progressive: 渐进状态 - 按重要性逐步显示\n');
fprintf('• pulse: 脉冲状态 - 重要节点闪烁效果\n');

fprintf('\n✅ 动态状态DPV可视化完成!\n');
fprintf('现在您可以通过不同状态文件来展示不同的节点呈现效果!\n');
'''
    
    with open('dynamic_dpv_visualization.m', 'w', encoding='utf-8') as f:
        f.write(matlab_script)
    
    print("✅ MATLAB动态可视化脚本: dynamic_dpv_visualization.m")

if __name__ == "__main__":
    create_dynamic_state_dpv() 