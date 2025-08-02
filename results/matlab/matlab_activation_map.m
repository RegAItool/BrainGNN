%% BrainNet Viewer - 脑区激活图可视化
% 基于BrainGNN模型的重要性分数
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

%% 1. 加载激活数据
fprintf('正在加载脑区激活数据...\n');

% 加载激活数据
activation_data = load('brain_activation.txt');
dpv_data = load('brain_activation.dpv');

fprintf('激活数据形状: %s\n', mat2str(size(activation_data)));
fprintf('DPV数据形状: %s\n', mat2str(size(dpv_data)));
fprintf('激活强度范围: %.3f 到 %.3f\n', min(activation_data), max(activation_data));

%% 2. 启动BrainNet Viewer进行激活图可视化
fprintf('\n=== 启动BrainNet Viewer激活图 ===\n');

try
    % 方法1: 使用mesh + dpv格式
    BrainNet_View('BrainMesh_ICBM152.nv', 'brain_activation.dpv');
    fprintf('✅ BrainNet Viewer激活图已启动\n');
    
catch ME
    fprintf('❌ 自动启动失败: %s\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载以下文件:\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\n');
    fprintf('  Data: brain_activation.dpv\n');
end

%% 3. 推荐设置说明
fprintf('\n=== 推荐激活图设置 ===\n');
fprintf('在BrainNet Viewer GUI中建议设置:\n');
fprintf('  • Color map: Jet 或 Hot (适合激活图)\n');
fprintf('  • Threshold: 0.1-0.3 (显示显著激活)\n');
fprintf('  • Transparency: 0.3-0.5\n');
fprintf('  • Lighting: Phong\n');
fprintf('  • View: 选择Lateral/Medial/Full视角\n');

%% 4. 保存设置脚本
fprintf('\n=== 生成激活图设置脚本 ===\n');

% 创建设置脚本
settings_script = sprintf([...
    '%% BrainNet Viewer 激活图设置脚本\n',...
    '%% 运行此脚本来自动配置激活图显示\n\n',...
    '%% 设置激活图显示\n',...
    'set(gcf, ''Color'', [1 1 1]);\n',...
    'h = findobj(gca, ''Type'', ''surface'');\n',...
    'set(h, ''FaceAlpha'', 0.8);\n\n',...
    '%% 设置颜色映射\n',...
    'colormap(jet);\n',...
    'colorbar;\n\n',...
    '%% 添加标题\n',...
    'title(''BrainGNN ROI重要性激活图 (ABIDE数据)'', ''FontSize'', 14);\n',...
    'fprintf(''✅ 激活图设置完成\n'');\n']);

% 保存设置脚本
fid = fopen('activation_map_settings.m', 'w');
fprintf(fid, '%s', settings_script);
fclose(fid);

fprintf('设置脚本已保存为: activation_map_settings.m\n');
fprintf('在BrainNet Viewer中运行此脚本来自动配置激活图显示\n');

fprintf('\n✅ 脑区激活图准备完成!\n');
