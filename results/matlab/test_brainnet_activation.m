%% BrainNet Viewer - 修复版激活图测试
% 测试多种文件格式的加载
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

%% 1. 测试数据加载
fprintf('=== 测试激活数据加载 ===\n');

% 尝试加载不同格式的文件
files_to_test = {
    'fixed_activation.dpv',
    'fixed_activation.txt', 
    'fixed_activation.csv',
    'test_activation.dpv'
};

for i = 1:length(files_to_test)
    file = files_to_test{i};
    try
        data = load(file);
        fprintf('✅ %s 加载成功, 形状: %s, 范围: %.3f-%.3f\n', ...
                file, mat2str(size(data)), min(data), max(data));
    catch ME
        fprintf('❌ %s 加载失败: %s\n', file, ME.message);
    end
end

%% 2. 测试BrainNet Viewer加载
fprintf('\n=== 测试BrainNet Viewer加载 ===\n');

% 测试文件列表
test_files = {
    'fixed_activation.dpv',
    'test_activation.dpv'
};

for i = 1:length(test_files)
    file = test_files{i};
    fprintf('\n尝试加载: %s\n', file);
    
    try
        % 尝试启动BrainNet Viewer
        BrainNet_View('BrainMesh_ICBM152.nv', file);
        fprintf('✅ %s 加载成功!\n', file);
        
        % 等待用户确认
        input('按回车键继续测试下一个文件...');
        close all;
        
    catch ME
        fprintf('❌ %s 加载失败: %s\n', file, ME.message);
    end
end

%% 3. 手动加载说明
fprintf('\n=== 手动加载说明 ===\n');
fprintf('如果自动加载失败，请手动在BrainNet Viewer中:\n');
fprintf('1. 打开BrainNet Viewer\n');
fprintf('2. 加载Surface: BrainMesh_ICBM152.nv\n');
fprintf('3. 加载Data: fixed_activation.dpv\n');
fprintf('4. 调整设置:\n');
fprintf('   - Color map: Jet\n');
fprintf('   - Threshold: 0.1\n');
fprintf('   - Transparency: 0.5\n');

fprintf('\n✅ 测试完成!\n');
