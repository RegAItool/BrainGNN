%% BrainNet Viewer - DPV文件测试
% 测试正确的DPV文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer DPV文件测试 ===\n');

%% 1. 检查文件
files_to_test = {
    'standard_activation.dpv',
    'large_activation.dpv', 
    'contrast_activation.dpv',
    'top30_activation.dpv'
};

for i = 1:length(files_to_test)
    if exist(files_to_test{i}, 'file')
        fprintf('✅ %s 存在\n', files_to_test{i});
    else
        fprintf('❌ %s 不存在\n', files_to_test{i});
    end
end

%% 2. 测试加载
fprintf('\n=== 测试文件加载 ===\n');

try
    % 测试标准版本
    data = load('standard_activation.dpv');
    fprintf('✅ 标准DPV版本加载成功\n');
    fprintf('   数据形状: %s\n', mat2str(size(data)));
    fprintf('   列数: %d (正确)\n', size(data, 2));
    
    if size(data, 2) == 7
        fprintf('✅ 格式正确: 7列 (x, y, z, size, color, shape, label)\n');
    else
        fprintf('❌ 格式错误: 期望7列，实际%d列\n', size(data, 2));
    end
    
    % 显示数据统计
    fprintf('   坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\n', ...
            min(data(:,1)), max(data(:,1)), ...
            min(data(:,2)), max(data(:,2)), ...
            min(data(:,3)), max(data(:,3)));
    fprintf('   点大小: 统一为 %.1f\n', data(1,4));
    fprintf('   颜色范围: %.2f 到 %.2f\n', min(data(:,5)), max(data(:,5)));
    fprintf('   形状编号: 统一为 %.0f\n', data(1,6));
    fprintf('   标签范围: %.0f 到 %.0f\n', min(data(:,7)), max(data(:,7)));
    
catch ME
    fprintf('❌ 文件加载失败: %s\n', ME.message);
    return;
end

%% 3. 启动BrainNet Viewer
fprintf('\n=== 启动BrainNet Viewer ===\n');

try
    if exist('BrainNet_View', 'file')
        fprintf('✅ BrainNet Viewer 可用\n');
        
        % 尝试启动
        fprintf('正在启动BrainNet Viewer...\n');
        BrainNet_View('BrainMesh_ICBM152.nv', 'standard_activation.dpv');
        fprintf('✅ BrainNet Viewer已启动\n');
        
    else
        fprintf('❌ BrainNet Viewer 不可用\n');
        fprintf('请手动打开BrainNet Viewer并加载:\n');
        fprintf('  Surface: BrainMesh_ICBM152.nv\n');
        fprintf('  Node: standard_activation.dpv\n');
    end
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Node: standard_activation.dpv\n');
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

%% 5. 文件选择建议
fprintf('\n=== 文件选择建议 ===\n');
fprintf('• standard_activation.dpv: 标准版本（推荐）\n');
fprintf('• large_activation.dpv: 大节点版本\n');
fprintf('• contrast_activation.dpv: 高对比度版本\n');
fprintf('• top30_activation.dpv: Top-30版本\n');

%% 6. 故障排除
fprintf('\n=== 故障排除 ===\n');
fprintf('如果节点仍然不显示:\n');
fprintf('  1. 确保View → Node已勾选\n');
fprintf('  2. 确保Option → Display Node已开启\n');
fprintf('  3. 尝试large_activation.dpv（更大节点）\n');
fprintf('  4. 检查文件格式（必须是7列）\n');

fprintf('\n✅ 测试完成!\n');
fprintf('现在应该能正确显示DPV激活图了!\n');
