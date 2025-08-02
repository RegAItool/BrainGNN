
% Python-MATLAB桥接脚本
% 用于BrainNet Viewer可视化

% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 加载数据信息
if exist('brainnet_data_info.json', 'file')
    fid = fopen('brainnet_data_info.json', 'r');
    data_info = jsondecode(fread(fid, inf, 'char=>char'));
    fclose(fid);
    fprintf('📊 数据信息:\n');
    fprintf('ROI数量: %d\n', data_info.roi_count);
    fprintf('最大重要性: %.4f\n', data_info.max_importance);
    fprintf('平均重要性: %.4f\n', data_info.mean_importance);
end

% 设置文件路径
node_file = 'bridge_nodes.node';
edge_file = 'bridge_edges.edge';

% 检查文件是否存在
if ~exist(node_file, 'file')
    error('节点文件不存在: %s', node_file);
end

if ~exist(edge_file, 'file')
    error('边文件不存在: %s', edge_file);
end

% 加载数据
node_data = load(node_file);
edge_data = load(edge_file);

fprintf('✅ 数据加载成功\n');
fprintf('节点数据大小: %s\n', mat2str(size(node_data)));
fprintf('边数据大小: %s\n', mat2str(size(edge_data)));

% 创建可视化
try
    % 设置BrainNet Viewer参数
    cfg = struct();
    cfg.file = node_file;
    cfg.edge = edge_file;
    cfg.outfile = 'brainnet_bridge_visualization.png';
    cfg.views = [0, 0, 1];
    cfg.colorbar = 1;
    cfg.node_size = 2;
    cfg.edge_size = 1;
    cfg.node_color = 1;
    cfg.edge_color = 1;
    cfg.title = 'BrainGNN ROI Importance - BrainNet Viewer';
    
    % 调用BrainNet Viewer
    BrainNet_MapCfg(cfg);
    
    % 保存图像
    print(gcf, 'brainnet_bridge_visualization.png', '-dpng', '-r300');
    fprintf('✅ BrainNet Viewer可视化完成\n');
    fprintf('💾 图像已保存: brainnet_bridge_visualization.png\n');
    
catch ME
    fprintf('❌ BrainNet Viewer错误: %s\n', ME.message);
    fprintf('错误位置: %s\n', ME.stack(1).name);
end
