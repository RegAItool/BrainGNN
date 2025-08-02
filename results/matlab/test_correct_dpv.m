%% BrainNet Viewer - 正确DPV格式测试
% 测试正确格式的DPV文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

%% 1. 加载DPV数据
fprintf('=== 加载正确格式的DPV文件 ===\n');

try
    % 加载DPV文件
    dpv_data = load('correct_activation.dpv');
    fprintf('✅ DPV文件加载成功\n');
    fprintf('DPV数据形状: %s\n', mat2str(size(dpv_data)));
    fprintf('坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\n', ...
            min(dpv_data(:,1)), max(dpv_data(:,1)), ...
            min(dpv_data(:,2)), max(dpv_data(:,2)), ...
            min(dpv_data(:,3)), max(dpv_data(:,3)));
    fprintf('重要性范围: %.3f 到 %.3f\n', min(dpv_data(:,4)), max(dpv_data(:,4)));
    
catch ME
    fprintf('❌ DPV文件加载失败: %s\n', ME.message);
    return;
end

%% 2. 启动BrainNet Viewer
fprintf('\n=== 启动BrainNet Viewer ===\n');

try
    % 使用DPV文件启动BrainNet Viewer
    BrainNet_View('BrainMesh_ICBM152.nv', 'correct_activation.dpv');
    fprintf('✅ BrainNet Viewer已启动\n');
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Node: correct_activation.dpv\n');
end

%% 3. 推荐设置
fprintf('\n=== 推荐设置 ===\n');
fprintf('在BrainNet Viewer中:\n');
fprintf('  • Node size scaling: 开启\n');
fprintf('  • Node color: 根据第5列\n');
fprintf('  • Node shape: 球体\n');
fprintf('  • Surface transparency: 0.3-0.5\n');
fprintf('  • Lighting: Phong\n');

fprintf('\n✅ 测试完成!\n');
