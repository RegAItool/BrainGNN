%% DPV状态切换器 - MATLAB版本
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
        fprintf('❌ 未知状态: %s
', state_name);
        fprintf('可用状态: ');
        fprintf('%s ', keys(states));
        fprintf('
');
        return;
    end
    
    filename = states(state_name);
    if ~exist(filename, 'file')
        fprintf('❌ 文件不存在: %s
', filename);
        return;
    end
    
    fprintf('✅ 切换到状态: %s
', state_name);
    fprintf('文件: %s
', filename);
    
    % 读取并显示状态信息
    info_file = sprintf('dpv_state_%s_info.txt', state_name);
    if exist(info_file, 'file')
        fprintf('
状态信息:
');
        fid = fopen(info_file, 'r');
        while ~feof(fid)
            line = fgetl(fid);
            fprintf('%s
', line);
        end
        fclose(fid);
    end
    
    % 尝试启动BrainNet Viewer
    try
        if exist('BrainNet_View', 'file')
            fprintf('正在启动BrainNet Viewer...
');
            BrainNet_View('BrainMesh_ICBM152.nv', filename);
            fprintf('✅ BrainNet Viewer已启动
');
        else
            fprintf('❌ BrainNet Viewer不可用
');
            fprintf('请手动打开BrainNet Viewer并加载:
');
            fprintf('  Surface: BrainMesh_ICBM152.nv
');
            fprintf('  Node: %s
', filename);
        end
    catch ME
        fprintf('❌ BrainNet Viewer启动失败: %s
', ME.message);
    end
end

function demo_state_transitions()
    %% 演示状态转换
    
    fprintf('=== DPV状态转换演示 ===
');
    
    states = {'normal', 'high', 'low', 'contrast', 'progressive', 'pulse'};
    
    for i = 1:length(states)
        state = states{i};
        fprintf('
--- 切换到 %s 状态 ---
', state);
        switch_dpv_state(state);
        pause(3);  % 等待3秒
    end
    
    fprintf('
✅ 状态转换演示完成!
');
end

%% 主程序
fprintf('DPV状态切换器
');
fprintf('可用状态:
');
fprintf('  normal      - 正常状态
');
fprintf('  high        - 高激活状态
'); 
fprintf('  low         - 低激活状态
');
fprintf('  contrast    - 对比状态
');
fprintf('  progressive - 渐进状态
');
fprintf('  pulse       - 脉冲状态
');
fprintf('  demo        - 演示所有状态
');

% 示例使用
fprintf('
示例: switch_dpv_state(''normal'')
');
fprintf('示例: demo_state_transitions()
');
