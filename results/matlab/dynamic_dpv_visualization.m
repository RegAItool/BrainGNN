%% BrainNet Viewer - 动态状态DPV可视化
% 支持多状态动态显示的DPV文件可视化
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer 动态状态DPV可视化 ===
');

%% 1. 检查所有状态文件
states = {
    'normal', 'high_activation', 'low_activation', 
    'contrast', 'progressive', 'pulse'
};

fprintf('
=== 检查状态文件 ===
');
for i = 1:length(states)
    filename = sprintf('dpv_state_%s.dpv', states{i});
    if exist(filename, 'file')
        fprintf('✅ %s 存在
', filename);
    else
        fprintf('❌ %s 不存在
', filename);
    end
end

%% 2. 动态状态演示
fprintf('
=== 动态状态演示 ===
');

% 启动BrainNet Viewer
if exist('BrainNet_View', 'file')
    fprintf('正在启动BrainNet Viewer...
');
    
    % 循环显示不同状态
    for i = 1:length(states)
        state = states{i};
        filename = sprintf('dpv_state_%s.dpv', states{i});
        
        if exist(filename, 'file')
            fprintf('
--- 显示 %s 状态 ---
', state);
            
            % 启动BrainNet Viewer
            try
                BrainNet_View('BrainMesh_ICBM152.nv', filename);
                fprintf('✅ %s 状态已加载
', state);
                
                % 等待用户确认
                fprintf('按任意键继续下一个状态...
');
                pause;
                
            catch ME
                fprintf('❌ %s 状态加载失败: %s
', state, ME.message);
            end
        end
    end
    
    fprintf('
✅ 动态状态演示完成!
');
    
else
    fprintf('❌ BrainNet Viewer 不可用
');
    fprintf('请手动打开BrainNet Viewer并依次加载:
');
    for i = 1:length(states)
        filename = sprintf('dpv_state_%s.dpv', states{i});
        fprintf('  %s
', filename);
    end
end

%% 3. 状态对比分析
fprintf('
=== 状态对比分析 ===
');

for i = 1:length(states)
    filename = sprintf('dpv_state_%s.dpv', states{i});
    info_file = sprintf('dpv_state_%s_info.txt', states{i});
    
    if exist(filename, 'file')
        data = load(filename);
        fprintf('
%s 状态:
', states{i});
        fprintf('  节点数量: %d
', size(data, 1));
        fprintf('  平均大小: %.2f
', mean(data(:, 4)));
        fprintf('  平均颜色: %.2f
', mean(data(:, 5)));
        fprintf('  可见节点: %d
', sum(data(:, 6) > 0));
        
        if exist(info_file, 'file')
            fprintf('  详细信息: %s
', info_file);
        end
    end
end

%% 4. 推荐设置
fprintf('
=== 推荐设置 ===
');
fprintf('在BrainNet Viewer中:
');
fprintf('  • View → Node: 必须勾选
');
fprintf('  • Option → Display Node: 必须开启
');
fprintf('  • Node size scaling: 开启
');
fprintf('  • Node color: Custom
');
fprintf('  • Node shape: 球体
');
fprintf('  • Surface transparency: 0.3-0.5
');

%% 5. 状态说明
fprintf('
=== 状态说明 ===
');
fprintf('• normal: 正常状态 - 所有节点正常显示
');
fprintf('• high_activation: 高激活状态 - 重要节点突出显示
');
fprintf('• low_activation: 低激活状态 - 重要节点隐藏
');
fprintf('• contrast: 对比状态 - 左右半球对比显示
');
fprintf('• progressive: 渐进状态 - 按重要性逐步显示
');
fprintf('• pulse: 脉冲状态 - 重要节点闪烁效果
');

fprintf('
✅ 动态状态DPV可视化完成!
');
fprintf('现在您可以通过不同状态文件来展示不同的节点呈现效果!
');
