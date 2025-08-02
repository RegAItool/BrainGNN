%% 快速测试DPV文件
% 测试新创建的DPV文件

clear; clc;

fprintf('=== 快速测试DPV文件 ===\n');

% 测试文件列表
files = {
    'standard_activation.dpv',
    'large_activation.dpv',
    'contrast_activation.dpv',
    'top30_activation.dpv'
};

for i = 1:length(files)
    if exist(files{i}, 'file')
        data = load(files{i});
        fprintf('✅ %s: %d行 x %d列\n', files{i}, size(data,1), size(data,2));
        
        if size(data, 2) == 7
            fprintf('   格式正确: 7列DPV格式\n');
            fprintf('   坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\n', ...
                min(data(:,1)), max(data(:,1)), ...
                min(data(:,2)), max(data(:,2)), ...
                min(data(:,3)), max(data(:,3)));
            fprintf('   点大小: %.1f\n', data(1,4));
            fprintf('   颜色范围: %.2f到%.2f\n', min(data(:,5)), max(data(:,5)));
        else
            fprintf('   ❌ 格式错误: %d列\n', size(data, 2));
        end
    else
        fprintf('❌ %s: 文件不存在\n', files{i});
    end
    fprintf('\n');
end

fprintf('=== 推荐使用 ===\n');
fprintf('• standard_activation.dpv - 标准版本\n');
fprintf('• large_activation.dpv - 大节点版本\n');
fprintf('• contrast_activation.dpv - 高对比度版本\n');
fprintf('• top30_activation.dpv - Top-30版本\n');

fprintf('\n=== 在BrainNet Viewer中使用 ===\n');
fprintf('1. 打开BrainNet Viewer\n');
fprintf('2. 加载Surface: BrainMesh_ICBM152.nv\n');
fprintf('3. 加载Node: standard_activation.dpv\n');
fprintf('4. 确保View → Node已勾选\n');
fprintf('5. 确保Option → Display Node已开启\n');

fprintf('\n✅ DPV文件测试完成!\n'); 