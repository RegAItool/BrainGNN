% 简单BrainNet Viewer脚本
% 用于绘制BrainGNN ROI重要性

% 添加BrainNet Viewer路径
addpath('./imports/BrainNetViewer_20191031');

% 检查BrainNet Viewer是否可用
if ~exist('BrainNet.m', 'file')
    error('BrainNet Viewer未找到，请检查路径');
end

fprintf('🧠 BrainNet Viewer可视化开始...\n');

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
    % 方法1: 使用BrainNet_MapCfg
    fprintf('🎨 创建BrainNet Viewer可视化...\n');
    
    % 设置BrainNet Viewer参数
    cfg = struct();
    cfg.file = node_file;
    cfg.edge = edge_file;
    cfg.outfile = 'brainnet_simple_visualization.png';
    cfg.views = [0, 0, 1];  % 视角
    cfg.colorbar = 1;        % 显示颜色条
    cfg.node_size = 2;       % 节点大小
    cfg.edge_size = 1;       % 边大小
    cfg.node_color = 1;      % 节点颜色
    cfg.edge_color = 1;      % 边颜色
    cfg.title = 'BrainGNN ROI Importance - BrainNet Viewer';
    
    % 调用BrainNet Viewer
    BrainNet_MapCfg(cfg);
    
    % 保存图像
    print(gcf, 'brainnet_simple_visualization.png', '-dpng', '-r300');
    fprintf('✅ BrainNet Viewer可视化完成\n');
    fprintf('💾 图像已保存: brainnet_simple_visualization.png\n');
    
catch ME
    fprintf('❌ BrainNet_MapCfg错误: %s\n', ME.message);
    
    % 方法2: 直接使用BrainNet GUI
    try
        fprintf('🔄 尝试使用BrainNet GUI...\n');
        
        % 启动BrainNet GUI
        BrainNet;
        
        fprintf('✅ BrainNet GUI已启动\n');
        fprintf('📝 请在GUI中手动加载以下文件:\n');
        fprintf('   节点文件: %s\n', node_file);
        fprintf('   边文件: %s\n', edge_file);
        
    catch ME2
        fprintf('❌ BrainNet GUI错误: %s\n', ME2.message);
    end
end

% 创建3D散点图作为备选方案
try
    fprintf('📊 创建3D散点图...\n');
    
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
    print(gcf, 'brainnet_3d_scatter.png', '-dpng', '-r300');
    fprintf('✅ 3D散点图完成\n');
    fprintf('💾 图像已保存: brainnet_3d_scatter.png\n');
    
catch ME
    fprintf('❌ 3D散点图错误: %s\n', ME.message);
end

fprintf('🎉 可视化脚本执行完成！\n');
fprintf('📁 生成的文件:\n');
fprintf('   - brainnet_simple_visualization.png (BrainNet可视化)\n');
fprintf('   - brainnet_3d_scatter.png (3D散点图)\n'); 