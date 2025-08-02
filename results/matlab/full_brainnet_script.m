% 完整BrainNet Viewer脚本
% 用于本地MATLAB + BrainNet Viewer

fprintf('🧠 BrainNet Viewer 完整可视化脚本\n');
fprintf('================================\n');

% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 检查BrainNet Viewer
if ~exist('BrainNet.m', 'file')
    fprintf('❌ BrainNet Viewer未找到\n');
    fprintf('请确保BrainNet Viewer已正确安装\n');
    return;
end

fprintf('✅ BrainNet Viewer已加载\n');

% 设置文件路径
node_file = 'bridge_nodes.node';
edge_file = 'bridge_edges.edge';

% 检查文件
if ~exist(node_file, 'file')
    fprintf('❌ 节点文件不存在: %s\n', node_file);
    return;
end

if ~exist(edge_file, 'file')
    fprintf('❌ 边文件不存在: %s\n', edge_file);
    return;
end

fprintf('✅ 所有文件都存在\n');

% 加载数据
fprintf('\n📊 加载数据...\n');
nodes = load(node_file);
edges = load(edge_file);
fprintf('✅ 数据加载成功\n');

% 方法1: 使用BrainNet_MapCfg
fprintf('\n🎨 方法1: 使用BrainNet_MapCfg...\n');
try
    % 设置BrainNet Viewer参数
    cfg = struct();
    cfg.file = node_file;
    cfg.edge = edge_file;
    cfg.outfile = 'brainnet_professional.png';
    cfg.views = [0, 0, 1];  % 视角
    cfg.colorbar = 1;        % 显示颜色条
    cfg.node_size = 2;       % 节点大小
    cfg.edge_size = 1;       % 边大小
    cfg.node_color = 1;      % 节点颜色
    cfg.edge_color = 1;      % 边颜色
    cfg.title = 'BrainGNN ROI Importance - Professional View';
    
    % 调用BrainNet Viewer
    BrainNet_MapCfg(cfg);
    
    % 保存图像
    print(gcf, 'brainnet_professional.png', '-dpng', '-r300');
    fprintf('✅ 专业可视化完成\n');
    fprintf('💾 图像已保存: brainnet_professional.png\n');
    
catch ME
    fprintf('❌ BrainNet_MapCfg错误: %s\n', ME.message);
    fprintf('尝试方法2...\n');
end

% 方法2: 启动BrainNet GUI
fprintf('\n🎨 方法2: 启动BrainNet GUI...\n');
try
    fprintf('🔄 启动BrainNet GUI...\n');
    
    % 启动BrainNet GUI
    BrainNet;
    
    fprintf('✅ BrainNet GUI已启动\n');
    fprintf('📝 请在GUI中手动加载以下文件:\n');
    fprintf('   节点文件: %s\n', node_file);
    fprintf('   边文件: %s\n', edge_file);
    fprintf('\n🎯 GUI操作步骤:\n');
    fprintf('1. 点击 "File" -> "Load" -> "Node File"\n');
    fprintf('2. 选择: %s\n', node_file);
    fprintf('3. 点击 "File" -> "Load" -> "Edge File"\n');
    fprintf('4. 选择: %s\n', edge_file);
    fprintf('5. 调整可视化参数\n');
    fprintf('6. 保存图像\n');
    
catch ME2
    fprintf('❌ BrainNet GUI错误: %s\n', ME2.message);
end

% 方法3: 创建自定义可视化
fprintf('\n🎨 方法3: 创建自定义可视化...\n');

figure('Position', [100, 100, 1200, 800]);

% 3D大脑网络
subplot(2, 3, 1);
scatter3(nodes(:,1), nodes(:,2), nodes(:,3), nodes(:,4)*30, nodes(:,5), 'filled');
colormap('hot');
colorbar;
title('BrainGNN ROI Network - 3D View', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
grid on;

% 2D投影
subplot(2, 3, 2);
scatter(nodes(:,1), nodes(:,2), nodes(:,4)*20, nodes(:,5), 'filled');
colormap('hot');
colorbar;
title('BrainGNN ROI Network - 2D Projection', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('X (mm)');
ylabel('Y (mm)');
grid on;

% 重要性分布
subplot(2, 3, 3);
histogram(nodes(:,5), 20, 'FaceColor', 'skyblue', 'EdgeColor', 'black');
title('ROI Importance Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Importance Score');
ylabel('Frequency');
grid on;

% 连接强度分布
subplot(2, 3, 4);
histogram(edges(:,3), 20, 'FaceColor', 'lightgreen', 'EdgeColor', 'black');
title('Connection Strength Distribution', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Connection Strength');
ylabel('Frequency');
grid on;

% 重要性排序
subplot(2, 3, 5);
[sorted_importance, sorted_indices] = sort(nodes(:,5), 'descend');
bar(sorted_importance(1:10), 'FaceColor', 'orange');
title('Top 10 ROI Importance', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('ROI Rank');
ylabel('Importance Score');
grid on;

% 网络统计
subplot(2, 3, 6);
axis off;
stats_text = sprintf(['Network Statistics:\n\n' ...
                     'Nodes: %d\n' ...
                     'Edges: %d\n\n' ...
                     'ROI Importance:\n' ...
                     '• Average: %.3f\n' ...
                     '• Maximum: %.3f\n\n' ...
                     'Connection Strength:\n' ...
                     '• Average: %.3f\n' ...
                     '• Maximum: %.3f'], ...
                     size(nodes, 1), size(edges, 1), ...
                     mean(nodes(:,5)), max(nodes(:,5)), ...
                     mean(edges(:,3)), max(edges(:,3)));

text(0.1, 0.9, stats_text, 'Units', 'normalized', ...
     'FontSize', 10, 'VerticalAlignment', 'top', ...
     'BackgroundColor', 'lightblue', 'EdgeColor', 'black');

% 保存图像
saveas(gcf, 'brainnet_custom_visualization.png');
fprintf('✅ 自定义可视化完成\n');
fprintf('💾 图像已保存: brainnet_custom_visualization.png\n');

fprintf('\n🎉 完整BrainNet Viewer脚本执行完成！\n');
fprintf('📁 生成的文件:\n');
fprintf('   - brainnet_professional.png (专业可视化)\n');
fprintf('   - brainnet_custom_visualization.png (自定义可视化)\n'); 