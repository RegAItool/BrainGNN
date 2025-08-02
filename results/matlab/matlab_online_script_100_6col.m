% MATLAB在线版BrainNet Viewer脚本 - 100节点6列格式版本
% 专为MATLAB Online优化，使用标准的6列.node文件格式

fprintf('🧠 BrainNet Viewer - 100节点6列格式版本\\n');
fprintf('============================================\\n');

% 检查当前目录
current_dir = pwd;
fprintf('当前目录: %s\\n', current_dir);

% 列出文件
fprintf('\\n📁 检查文件:\\n');
files = dir('*6col.node');
for i = 1:length(files)
    fprintf('   ✅ %s\\n', files(i).name);
end

files = dir('*100.edge');
for i = 1:length(files)
    fprintf('   ✅ %s\\n', files(i).name);
end

% 加载数据
fprintf('\\n📊 加载数据...\\n');
try
    nodes = load('brainnet_nodes_100_6col.node');
    edges = load('brainnet_edges_100.edge');
    fprintf('✅ 数据加载成功\\n');
    fprintf('   节点数: %d\\n', size(nodes, 1));
    fprintf('   节点列数: %d\\n', size(nodes, 2));
    fprintf('   边矩阵: %dx%d\\n', size(edges, 1), size(edges, 2));
catch ME
    fprintf('❌ 数据加载失败: %s\\n', ME.message);
    return;
end

% 创建可视化
fprintf('\\n🎨 创建可视化...\\n');

figure('Position', [100, 100, 1400, 900]);

% 1. 3D散点图（按模块着色）
subplot(2, 4, 1);
modules = nodes(:, 6);
colors = jet(6); % 6种颜色对应6个模块
for i = 1:6
    idx = modules == i;
    if any(idx)
        scatter3(nodes(idx, 1), nodes(idx, 2), nodes(idx, 3), ...
                nodes(idx, 4)*2, colors(i, :), 'filled', 'DisplayName', sprintf('Module %d', i));
        hold on;
    end
end
title('3D ROI Distribution (by Module)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
view(45, 30);
legend('Location', 'best');

% 2. 连接矩阵热图
subplot(2, 4, 2);
imagesc(edges);
colormap(jet);
colorbar;
title('Functional Connectivity Matrix', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('ROI Index');
ylabel('ROI Index');
axis square;

% 3. 重要性分布直方图
subplot(2, 4, 3);
histogram(nodes(:, 5), 20, 'FaceColor', 'skyblue', 'EdgeColor', 'black');
title('ROI Importance Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Importance Score');
ylabel('Frequency');
grid on;

% 4. 模块分布饼图
subplot(2, 4, 4);
module_counts = histcounts(modules, 1:7);
pie(module_counts, {'Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5', 'Module 6'});
title('Module Distribution', 'FontSize', 12, 'FontWeight', 'bold');

% 5. 2D投影图（按重要性着色）
subplot(2, 4, 5);
scatter(nodes(:, 1), nodes(:, 2), nodes(:, 4)*3, nodes(:, 5), 'filled');
colormap(jet);
colorbar;
title('2D ROI Projection (X-Y, by Importance)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
axis equal;

% 6. 连接强度分布
subplot(2, 4, 6);
% 获取下三角矩阵的值（避免重复）
lower_tri = tril(edges, -1);
values = lower_tri(lower_tri ~= 0);
histogram(values, 30, 'FaceColor', 'lightgreen', 'EdgeColor', 'black');
title('Connection Strength Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Connection Strength');
ylabel('Frequency');
grid on;

% 7. 节点大小分布
subplot(2, 4, 7);
histogram(nodes(:, 4), 15, 'FaceColor', 'orange', 'EdgeColor', 'black');
title('Node Size Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Node Size');
ylabel('Frequency');
grid on;

% 8. 模块内连接强度
subplot(2, 4, 8);
module_avg_connections = zeros(6, 1);
for i = 1:6
    module_nodes = find(modules == i);
    if length(module_nodes) > 1
        module_edges = edges(module_nodes, module_nodes);
        module_avg_connections(i) = mean(module_edges(module_edges > 0));
    end
end
bar(1:6, module_avg_connections, 'FaceColor', 'purple');
title('Average Connection Strength by Module', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Module');
ylabel('Avg Connection Strength');
grid on;

% 保存图像
fprintf('\\n💾 保存图像...\\n');
saveas(gcf, 'matlab_online_brainnet_100_6col.png');
fprintf('✅ 图像已保存: matlab_online_brainnet_100_6col.png\\n');

% 显示统计信息
fprintf('\\n📈 统计信息:\\n');
fprintf('   节点总数: %d\\n', size(nodes, 1));
fprintf('   最大重要性: %.4f\\n', max(nodes(:, 5)));
fprintf('   平均重要性: %.4f\\n', mean(nodes(:, 5)));
fprintf('   节点大小范围: [%.3f, %.3f]\\n', min(nodes(:, 4)), max(nodes(:, 4)));
fprintf('   模块分布: %s\\n', mat2str(module_counts));
fprintf('   连接矩阵非零元素: %d\\n', nnz(edges));
fprintf('   连接强度范围: [%.6f, %.6f]\\n', min(edges(edges > 0)), max(edges(:)));

fprintf('\\n🎉 可视化完成！\\n');
fprintf('请下载 matlab_online_brainnet_100_6col.png 文件\\n');
fprintf('\\n📋 文件格式说明:\\n');
fprintf('Node文件格式: x\\ty\\tz\\tsize\\tcolor\\tmodule\\n');
fprintf('  - x, y, z: MNI坐标 (mm)\\n');
fprintf('  - size: 节点大小 (5-20)\\n');
fprintf('  - color: 颜色值 (0-1, 基于重要性)\\n');
fprintf('  - module: 模块编号 (1-6, 基于FC相似性聚类)\\n'); 