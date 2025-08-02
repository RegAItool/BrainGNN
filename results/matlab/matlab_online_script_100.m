% MATLAB在线版BrainNet Viewer脚本 - 100节点版本
% 专为MATLAB Online优化，使用真实的FC矩阵

fprintf('🧠 BrainNet Viewer - 100节点版本\\n');
fprintf('=====================================\\n');

% 检查当前目录
current_dir = pwd;
fprintf('当前目录: %s\\n', current_dir);

% 列出文件
fprintf('\\n📁 检查文件:\\n');
files = dir('*100.node');
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
    nodes = load('brainnet_nodes_100.node');
    edges = load('brainnet_edges_100.edge');
    fprintf('✅ 数据加载成功\\n');
    fprintf('   节点数: %d\\n', size(nodes, 1));
    fprintf('   边矩阵: %dx%d\\n', size(edges, 1), size(edges, 2));
catch ME
    fprintf('❌ 数据加载失败: %s\\n', ME.message);
    return;
end

% 创建可视化
fprintf('\\n🎨 创建可视化...\\n');

figure('Position', [100, 100, 1200, 800]);

% 1. 3D散点图
subplot(2, 3, 1);
scatter3(nodes(:, 1), nodes(:, 2), nodes(:, 3), nodes(:, 4)*2, nodes(:, 5), 'filled');
colormap(jet);
colorbar;
title('3D ROI Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
view(45, 30);

% 2. 连接矩阵热图
subplot(2, 3, 2);
imagesc(edges);
colormap(jet);
colorbar;
title('Functional Connectivity Matrix', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('ROI Index');
ylabel('ROI Index');
axis square;

% 3. 重要性分布直方图
subplot(2, 3, 3);
histogram(nodes(:, 5), 20, 'FaceColor', 'skyblue', 'EdgeColor', 'black');
title('ROI Importance Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Importance Score');
ylabel('Frequency');
grid on;

% 4. 2D投影图
subplot(2, 3, 4);
scatter(nodes(:, 1), nodes(:, 2), nodes(:, 4)*3, nodes(:, 5), 'filled');
colormap(jet);
colorbar;
title('2D ROI Projection (X-Y)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
axis equal;

% 5. 连接强度分布
subplot(2, 3, 5);
% 获取下三角矩阵的值（避免重复）
lower_tri = tril(edges, -1);
values = lower_tri(lower_tri ~= 0);
histogram(values, 30, 'FaceColor', 'lightgreen', 'EdgeColor', 'black');
title('Connection Strength Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Connection Strength');
ylabel('Frequency');
grid on;

% 6. 网络度分布
subplot(2, 3, 6);
degrees = sum(edges > 0, 2); % 计算每个节点的连接数
histogram(degrees, 15, 'FaceColor', 'orange', 'EdgeColor', 'black');
title('Node Degree Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Degree');
ylabel('Frequency');
grid on;

% 保存图像
fprintf('\\n💾 保存图像...\\n');
saveas(gcf, 'matlab_online_brainnet_100.png');
fprintf('✅ 图像已保存: matlab_online_brainnet_100.png\\n');

% 显示统计信息
fprintf('\\n📈 统计信息:\\n');
fprintf('   节点总数: %d\\n', size(nodes, 1));
fprintf('   最大重要性: %.4f\\n', max(nodes(:, 5)));
fprintf('   平均重要性: %.4f\\n', mean(nodes(:, 5)));
fprintf('   连接矩阵非零元素: %d\\n', nnz(edges));
fprintf('   连接强度范围: [%.6f, %.6f]\\n', min(edges(edges > 0)), max(edges(:)));
fprintf('   平均节点度: %.2f\\n', mean(degrees));

fprintf('\\n🎉 可视化完成！\\n');
fprintf('请下载 matlab_online_brainnet_100.png 文件\\n'); 