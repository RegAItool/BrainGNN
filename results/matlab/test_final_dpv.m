%% BrainNet Viewer - 最终DPV格式测试
% 测试正确格式的DPV文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer DPV格式测试 ===\n');

%% 1. 检查文件存在性
files_to_check = {'correct_activation.dpv', 'top30_activation.dpv'};
for i = 1:length(files_to_check)
    if exist(files_to_check{i}, 'file')
        fprintf('✅ %s 存在\n', files_to_check{i});
    else
        fprintf('❌ %s 不存在\n', files_to_check{i});
    end
end

%% 2. 加载并验证DPV数据
fprintf('\n=== 加载DPV数据 ===\n');

try
    % 加载完整版本
    dpv_data = load('correct_activation.dpv');
    fprintf('✅ 完整DPV文件加载成功\n');
    fprintf('   数据形状: %s\n', mat2str(size(dpv_data)));
    fprintf('   ROI数量: %d\n', size(dpv_data, 1));
    
    % 验证格式
    if size(dpv_data, 2) == 7
        fprintf('✅ 格式正确: 7列 (x, y, z, size, color, shape, label)\n');
    else
        fprintf('❌ 格式错误: 期望7列，实际%d列\n', size(dpv_data, 2));
    end
    
    % 显示数据统计
    fprintf('   坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\n', ...
            min(dpv_data(:,1)), max(dpv_data(:,1)), ...
            min(dpv_data(:,2)), max(dpv_data(:,2)), ...
            min(dpv_data(:,3)), max(dpv_data(:,3)));
    fprintf('   重要性范围: %.3f 到 %.3f\n', min(dpv_data(:,4)), max(dpv_data(:,4)));
    fprintf('   颜色范围: %.3f 到 %.3f\n', min(dpv_data(:,5)), max(dpv_data(:,5)));
    
catch ME
    fprintf('❌ DPV文件加载失败: %s\n', ME.message);
    return;
end

%% 3. 启动BrainNet Viewer
fprintf('\n=== 启动BrainNet Viewer ===\n');

try
    % 检查BrainNet Viewer是否可用
    if exist('BrainNet_View', 'file')
        fprintf('✅ BrainNet Viewer 可用\n');
        
        % 使用完整DPV文件启动
        fprintf('正在启动BrainNet Viewer...\n');
        BrainNet_View('BrainMesh_ICBM152.nv', 'correct_activation.dpv');
        fprintf('✅ BrainNet Viewer已启动\n');
        
    else
        fprintf('❌ BrainNet Viewer 不可用\n');
        fprintf('请手动打开BrainNet Viewer并加载:\n');
        fprintf('  Surface: BrainMesh_ICBM152.nv\n');
        fprintf('  Node: correct_activation.dpv\n');
    end
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Node: correct_activation.dpv\n');
end

%% 4. 推荐设置
fprintf('\n=== 推荐设置 ===\n');
fprintf('在BrainNet Viewer中:\n');
fprintf('  • Node size scaling: 开启\n');
fprintf('  • Node color: 根据第5列颜色值\n');
fprintf('  • Node shape: 球体\n');
fprintf('  • Node transparency: 0.8-1.0\n');
fprintf('  • Surface transparency: 0.3-0.5\n');
fprintf('  • Lighting: Phong\n');
fprintf('  • Color map: Jet 或 Hot\n');

%% 5. 文件选择建议
fprintf('\n=== 文件选择建议 ===\n');
fprintf('• correct_activation.dpv: 显示所有100个ROI (完整版本)\n');
fprintf('• top30_activation.dpv: 只显示最重要的30个ROI (推荐)\n');

%% 6. 故障排除
fprintf('\n=== 故障排除 ===\n');
fprintf('如果激活图不显示颜色:\n');
fprintf('  1. 检查Node color设置\n');
fprintf('  2. 调整颜色映射范围\n');
fprintf('  3. 确保Node size scaling开启\n');
fprintf('  4. 尝试不同的颜色映射 (Jet, Hot, Parula)\n');

fprintf('\n✅ 测试完成!\n');
fprintf('现在应该能看到彩色的脑区激活图了!\n'); 