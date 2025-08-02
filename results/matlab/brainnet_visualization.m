
% BrainNet Viewer 可视化脚本
% 用于绘制BrainGNN ROI重要性

% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 设置文件路径
node_file = 'brainnet_nodes.node';
edge_file = 'brainnet_edges.edge';

% 加载节点和边数据
node_data = load(node_file);
edge_data = load(edge_file);

% 设置BrainNet Viewer参数
cfg = struct();
cfg.file = node_file;
cfg.edge = edge_file;
cfg.outfile = 'brainnet_visualization.png';
cfg.views = [0, 0, 1];  % 视角设置
cfg.colorbar = 1;        % 显示颜色条
cfg.node_size = 1;       % 节点大小
cfg.edge_size = 1;       % 边大小
cfg.node_color = 1;      % 节点颜色
cfg.edge_color = 1;      % 边颜色

% 调用BrainNet Viewer
try
    BrainNet_MapCfg(cfg);
    fprintf('✅ BrainNet Viewer可视化完成\n');
catch ME
    fprintf('❌ BrainNet Viewer错误: %s\n', ME.message);
end

% 保存图像
print(gcf, 'brainnet_visualization.png', '-dpng', '-r300');
fprintf('💾 图像已保存: brainnet_visualization.png\n');
