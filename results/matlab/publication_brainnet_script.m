
%% BrainNet Viewer Script for Publication Quality Pain Brain Mapping
%% BrainGNN Results: Pain vs No-Pain Classification (98.7% Accuracy)

% Add BrainNet Viewer to path
addpath('./imports/BrainNetViewer_20191031');

%% Configuration
% Input files
node_file = './results/node/brain_pain_nodes.node';
edge_file = './results/edge/brain_pain_edges.edge';
dpv_file = './results/dpv/brain_pain_activation.dpv';

% Surface template
surf_file = './imports/BrainNetViewer_20191031/Data/SurfTemplate/BrainMesh_ICBM152_smoothed.nv';

% Output directory
output_dir = './figures/publication/';
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

%% Generate Multiple Views for Publication

% 1. Lateral view (left hemisphere)
fprintf('Generating lateral view (left hemisphere)...\n');
BrainNet_MapCfg('BrainMesh_ICBM152_smoothed.nv', dpv_file, node_file, ...
    [output_dir 'brainnet_lateral_left.jpg'], ...
    'NodeSize', 'On', 'EdgeSize', 'Off', 'Colorbar', 'On', ...
    'ViewAngle', [-90 0]);

% 2. Lateral view (right hemisphere)  
fprintf('Generating lateral view (right hemisphere)...\n');
BrainNet_MapCfg('BrainMesh_ICBM152_smoothed.nv', dpv_file, node_file, ...
    [output_dir 'brainnet_lateral_right.jpg'], ...
    'NodeSize', 'On', 'EdgeSize', 'Off', 'Colorbar', 'On', ...
    'ViewAngle', [90 0]);

% 3. Superior view
fprintf('Generating superior view...\n');
BrainNet_MapCfg('BrainMesh_ICBM152_smoothed.nv', dpv_file, node_file, ...
    [output_dir 'brainnet_superior.jpg'], ...
    'NodeSize', 'On', 'EdgeSize', 'Off', 'Colorbar', 'On', ...
    'ViewAngle', [0 90]);

% 4. Anterior view
fprintf('Generating anterior view...\n');
BrainNet_MapCfg('BrainMesh_ICBM152_smoothed.nv', dpv_file, node_file, ...
    [output_dir 'brainnet_anterior.jpg'], ...
    'NodeSize', 'On', 'EdgeSize', 'Off', 'Colorbar', 'On', ...
    'ViewAngle', [0 0]);

% 5. Connectivity network view
fprintf('Generating connectivity network view...\n');
BrainNet_MapCfg('BrainMesh_ICBM152_smoothed.nv', [], node_file, ...
    [output_dir 'brainnet_connectivity.jpg'], ...
    'EdgeFile', edge_file, ...
    'NodeSize', 'On', 'EdgeSize', 'On', 'Colorbar', 'On', ...
    'ViewAngle', [-45 15]);

%% High-Resolution Export Settings
% For publication quality, use these additional options:
% 'Resolution', [1200 900]  % Higher resolution
% 'ImageFormat', 'tiff'     % Lossless format

fprintf('\n✅ BrainNet Viewer visualization completed!\n');
fprintf('📂 Images saved in: %s\n', output_dir);

%% Display Summary
fprintf('\n📊 BrainGNN Pain Analysis Summary:\n');
fprintf('   • Model Accuracy: 98.7%%\n');
fprintf('   • Brain Regions: %d key areas\n', 14);
fprintf('   • Classification: Pain vs No-Pain states\n');
fprintf('   • Visualization: Multiple publication-ready views\n');
