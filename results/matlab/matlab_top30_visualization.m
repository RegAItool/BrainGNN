%% BrainNet Viewer - Top-30重要节点可视化
% 基于BrainGNN模型在ABIDE数据上的ROI重要性分析
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

%% 1. 加载Top-30文件
fprintf('正在加载Top-30节点文件...\n');

% 加载节点和边文件
node = load('top30.node');
edge = load('top30.edge');

fprintf('节点文件形状: %s\n', mat2str(size(node)));
fprintf('边文件形状: %s\n', mat2str(size(edge)));

%% 2. 显示节点信息
fprintf('\n=== Top-30节点信息 ===\n');
fprintf('节点重要性范围: %.3f 到 %.3f\n', min(node(:,4)), max(node(:,4)));
fprintf('模块数量: %d\n', length(unique(node(:,6))));

% 显示模块分布
modules = unique(node(:,6));
fprintf('模块分布:\n');
for i = 1:length(modules)
    module_count = sum(node(:,6) == modules(i));
    fprintf('  模块 %d: %d个节点\n', modules(i), module_count);
end

%% 3. 显示边连接信息
fprintf('\n=== 边连接信息 ===\n');
non_zero_edges = edge(edge > 0);
fprintf('总边数: %d\n', numel(edge));
fprintf('非零边数: %d\n', length(non_zero_edges));
fprintf('边强度范围: %.6f 到 %.6f\n', min(non_zero_edges), max(non_zero_edges));

%% 4. 启动BrainNet Viewer
fprintf('\n=== 启动BrainNet Viewer ===\n');
fprintf('正在打开BrainNet Viewer...\n');

try
    % 方法1: 直接调用BrainNet Viewer
    BrainNet_View('BrainMesh_ICBM152.nv', 'top30.node', 'top30.edge');
    fprintf('✅ BrainNet Viewer已启动\n');
    
catch ME
    fprintf('❌ 自动启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载以下文件:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Node: top30.node\n');
    fprintf('  Edge: top30.edge\n');
end

%% 5. 推荐设置说明
fprintf('\n=== 推荐可视化设置 ===\n');
fprintf('在BrainNet Viewer GUI中建议设置:\n');
fprintf('  • Node size scaling: 开启 (根据第4列自动缩放)\n');
fprintf('  • Edge threshold: 0.1-0.3 (过滤弱连接)\n');
fprintf('  • Surface transparency: 0.3-0.5\n');
fprintf('  • Lighting: Phong\n');
fprintf('  • Color map: Jet 或 Hot\n');
fprintf('  • View: 选择Lateral/Medial/Full视角\n');

%% 6. 保存设置脚本（可选）
fprintf('\n=== 生成设置脚本 ===\n');

% 创建设置脚本
settings_script = sprintf([...
    '%% BrainNet Viewer 设置脚本\n',...
    '%% 运行此脚本来自动配置BrainNet Viewer\n\n',...
    '%% 设置节点显示\n',...
    'set(gcf, ''Color'', [1 1 1]);\n',...
    'h = findobj(gca, ''Type'', ''line'');\n',...
    'set(h, ''LineWidth'', 1.5);\n\n',...
    '%% 设置边显示\n',...
    'h = findobj(gca, ''Type'', ''surface'');\n',...
    'set(h, ''FaceAlpha'', 0.3);\n\n',...
    '%% 添加标题\n',...
    'title(''BrainGNN Top-30重要ROI网络 (ABIDE数据)'', ''FontSize'', 14);\n',...
    'fprintf(''✅ 设置完成\\n'');\n']);

% 保存设置脚本
fid = fopen('brainnet_settings.m', 'w');
fprintf(fid, '%s', settings_script);
fclose(fid);

fprintf('设置脚本已保存为: brainnet_settings.m\n');
fprintf('在BrainNet Viewer中运行此脚本来自动配置显示\n');

fprintf('\n✅ Top-30可视化准备完成!\n'); 