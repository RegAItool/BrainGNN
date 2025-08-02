
% 高级BrainNet Viewer可视化脚本
% BrainGNN ROI重要性可视化

% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 设置文件路径
node_file = 'advanced_nodes.node';
edge_file = 'advanced_edges.edge';

% 加载数据
node_data = load(node_file);
edge_data = load(edge_file);

% 创建多个视角的可视化
views = {[0, 0, 1], [1, 0, 0], [0, 1, 0]};  % 不同视角
view_names = {'Dorsal', 'Lateral', 'Frontal'};

for i = 1:length(views)
    % 设置参数
    cfg = struct();
    cfg.file = node_file;
    cfg.edge = edge_file;
    cfg.outfile = sprintf('brainnet_view_%d.png', i);
    cfg.views = views{i};
    cfg.colorbar = 1;
    cfg.node_size = 2;
    cfg.edge_size = 1;
    cfg.node_color = 1;
    cfg.edge_color = 1;
    cfg.title = sprintf('BrainGNN ROI Importance - %s View', view_names{i});
    
    % 调用BrainNet Viewer
    try
        BrainNet_MapCfg(cfg);
        print(gcf, sprintf('brainnet_view_%d.png', i), '-dpng', '-r300');
        fprintf('✅ %s视图完成\n', view_names{i});
    catch ME
        fprintf('❌ %s视图错误: %s\n', view_names{i}, ME.message);
    end
end

% 创建3D可视化
try
    figure('Position', [100, 100, 800, 600]);
    
    % 绘制3D散点图
    scatter3(node_data(:,1), node_data(:,2), node_data(:,3), ...
             node_data(:,4)*10, node_data(:,5), 'filled');
    
    % 设置颜色映射
    colormap('hot');
    colorbar;
    
    % 设置标签
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    title('BrainGNN ROI Importance - 3D Visualization');
    
    % 保存3D图
    print(gcf, 'brainnet_3d_visualization.png', '-dpng', '-r300');
    fprintf('✅ 3D可视化完成\n');
catch ME
    fprintf('❌ 3D可视化错误: %s\n', ME.message);
end

fprintf('🎉 所有可视化完成！\n');
