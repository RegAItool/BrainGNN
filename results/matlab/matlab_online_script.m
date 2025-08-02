% MATLAB在线版BrainNet Viewer脚本
% 专为MATLAB Online优化

fprintf('🧠 BrainNet Viewer - MATLAB Online版本\n');
fprintf('=====================================\n');

% 检查当前目录
current_dir = pwd;
fprintf('当前目录: %s\n', current_dir);

% 列出文件
fprintf('\n📁 检查文件:\n');
files = dir('*.node');
for i = 1:length(files)
    fprintf('   ✅ %s\n', files(i).name);
end

files = dir('*.edge');
for i = 1:length(files)
    fprintf('   ✅ %s\n', files(i).name);
end

% 加载数据
fprintf('\n📊 加载数据...\n');
try
    nodes = load('bridge_nodes.node');
    edges = load('bridge_edges.edge');
    fprintf('✅ 数据加载成功\n');
    fprintf('   节点数: %d\n', size(nodes, 1));
    fprintf('   边数: %d\n', size(edges, 1));
catch ME
    fprintf('❌ 数据加载失败: %s\n', ME.message);
    return;
end

% 创建简单的3D可视化
fprintf('\n🎨 创建3D可视化...\n');

figure('Position', [100, 100, 800, 600]);

% 3D散点图
subplot(2, 2, 1);
scatter3(nodes(:,1), nodes(:,2), nodes(:,3), nodes(:,4)*20, nodes(:,5), 'filled');
colormap('hot');
colorbar;
title('BrainGNN ROI Network - 3D View');
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');

% 2D投影
subplot(2, 2, 2);
scatter(nodes(:,1), nodes(:,2), nodes(:,4)*15, nodes(:,5), 'filled');
colormap('hot');
colorbar;
title('BrainGNN ROI Network - 2D Projection');
xlabel('X (mm)');
ylabel('Y (mm)');
grid on;

% 重要性分布
subplot(2, 2, 3);
histogram(nodes(:,5), 20, 'FaceColor', 'skyblue', 'EdgeColor', 'black');
title('ROI Importance Distribution');
xlabel('Importance Score');
ylabel('Frequency');
grid on;

% 连接强度
subplot(2, 2, 4);
histogram(edges(:,3), 20, 'FaceColor', 'lightgreen', 'EdgeColor', 'black');
title('Connection Strength Distribution');
xlabel('Connection Strength');
ylabel('Frequency');
grid on;

% 保存图像
fprintf('\n💾 保存图像...\n');
saveas(gcf, 'matlab_online_brainnet.png');
fprintf('✅ 图像已保存: matlab_online_brainnet.png\n');

% 显示统计信息
fprintf('\n📈 网络统计:\n');
fprintf('   平均重要性: %.3f\n', mean(nodes(:,5)));
fprintf('   最大重要性: %.3f\n', max(nodes(:,5)));
fprintf('   平均连接强度: %.3f\n', mean(edges(:,3)));
fprintf('   最大连接强度: %.3f\n', max(edges(:,3)));

fprintf('\n🎉 MATLAB在线版可视化完成！\n');
fprintf('📁 生成文件: matlab_online_brainnet.png\n'); 