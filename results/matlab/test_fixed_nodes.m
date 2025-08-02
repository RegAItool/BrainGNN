%% BrainNet Viewer - 修复版本测试
% 测试修复后的节点文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer 修复版本测试 ===\n');

%% 1. 检查文件
files_to_test = {
    'fixed_activation.node',
    'simple_activation.node', 
    'large_activation.node',
    'contrast_activation.node'
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
    data = load('fixed_activation.node');
    fprintf('✅ 标准版本加载成功\n');
    fprintf('   数据形状: %s\n', mat2str(size(data)));
    fprintf('   大小范围: %.2f 到 %.2f\n', min(data(:,4)), max(data(:,4)));
    fprintf('   颜色范围: %.2f 到 %.2f\n', min(data(:,5)), max(data(:,5)));
    
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
        BrainNet_View('BrainMesh_ICBM152.nv', 'fixed_activation.node');
        fprintf('✅ BrainNet Viewer已启动\n');
        
    else
        fprintf('❌ BrainNet Viewer 不可用\n');
        fprintf('请手动打开BrainNet Viewer并加载:\n');
        fprintf('  Surface: BrainMesh_ICBM152.nv\n');
        fprintf('  Node: fixed_activation.node\n');
    end
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Node: fixed_activation.node\n');
end

%% 4. 推荐设置
fprintf('\n=== 推荐设置 ===\n');
fprintf('在BrainNet Viewer中:\n');
fprintf('  • Node size scaling: 开启\n');
fprintf('  • Node color: Custom\n');
fprintf('  • Node shape: 球体\n');
fprintf('  • Surface transparency: 0.3-0.5\n');
fprintf('  • Color map: Jet 或 Hot\n');

%% 5. 文件选择建议
fprintf('\n=== 文件选择建议 ===\n');
fprintf('• fixed_activation.node: 标准版本\n');
fprintf('• simple_activation.node: 简化版本（6列）\n');
fprintf('• large_activation.node: 大节点版本\n');
fprintf('• contrast_activation.node: 高对比度版本\n');

%% 6. 故障排除
fprintf('\n=== 故障排除 ===\n');
fprintf('如果节点仍然不显示:\n');
fprintf('  1. 确保View → Node已勾选\n');
fprintf('  2. 确保Option → Display Node已开启\n');
fprintf('  3. 尝试不同的节点文件\n');
fprintf('  4. 调整Node size scaling参数\n');

fprintf('\n✅ 测试完成!\n');
