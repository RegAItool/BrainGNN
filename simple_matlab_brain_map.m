%% Simple Professional Brain Mapping using MATLAB
% BrainGNN Pain Region Analysis - Clean Visualization
% 98.7% Accuracy Model Results

clear; clc; close all;

%% Setup
fprintf('🧠 Creating Simple MATLAB Brain Mapping...\n');
fprintf('📊 BrainGNN Model Accuracy: 98.7%%\n\n');

% Create results directory
if ~exist('./matlab_figures', 'dir')
    mkdir('./matlab_figures');
end

%% Define brain regions with activation data
coords = [
    60, -75, -20;   % Cerebelum_Crus1_R
    -60, -75, -20;  % Cerebelum_Crus1_L
    50, -65, -15;   % Cerebelum_Crus2_R
    45, -90, 5;     % Occipital_Mid_R
    25, -95, 10;    % Occipital_Sup_R
    -45, -90, 5;    % Occipital_Mid_L
    -35, 70, 25;    % Frontal_Sup_L
    -50, 45, 20;    % Frontal_Mid_L
    35, 70, 25;     % Frontal_Sup_R
    -40, 25, 50;    % Precentral_L
    -40, -20, 50;   % Postcentral_L
    -55, 5, 15;     % Rolandic_Oper_L
    25, -10, -10;   % Amygdala_R
    12, 40, 25;     % Cingulum_Ant_R
    -30, -35, -15;  % ParaHippocampal_L
    -15, -15, 5;    % Thalamus_L
    25, 5, 0;       % Putamen_R
];

activations = [0.601; 0.438; 0.391; 0.528; 0.528; 0.385; -0.512; -0.498; -0.394; -0.433; -0.431; -0.401; 0.080; 0.065; 0.120; 0.055; -0.386];
importances = [0.022; 0.016; 0.014; 0.022; 0.022; 0.016; 0.015; 0.014; 0.011; 0.013; 0.012; 0.019; 0.015; 0.013; 0.019; 0.011; 0.009];

region_names = {
    'Cerebelum Crus1 R';
    'Cerebelum Crus1 L';
    'Cerebelum Crus2 R';
    'Occipital Mid R';
    'Occipital Sup R';
    'Occipital Mid L';
    'Frontal Sup L';
    'Frontal Mid L';
    'Frontal Sup R';
    'Precentral L';
    'Postcentral L';
    'Rolandic Oper L';
    'Amygdala R';
    'Cingulum Ant R';
    'ParaHippocampal L';
    'Thalamus L';
    'Putamen R';
};

n_regions = length(activations);

%% Create main figure
figure('Position', [100, 100, 1400, 1000], 'Color', 'white');

%% Main 3D brain plot
subplot(2, 2, [1, 3]);

% Create scatter plot with size based on importance
scatter3(coords(:, 1), coords(:, 2), coords(:, 3), ...
         importances * 2000, activations, 'filled', ...
         'MarkerEdgeColor', 'black', 'LineWidth', 1.5);

% Set colormap
colormap(jet);
caxis([-0.6, 0.6]);

% Add colorbar
cb = colorbar;
cb.Label.String = 'Activation Difference (Pain - No Pain)';
cb.Label.FontSize = 12;

% Labels and title
xlabel('Left <- -> Right (mm)', 'FontSize', 12);
ylabel('Posterior <- -> Anterior (mm)', 'FontSize', 12);
zlabel('Inferior <- -> Superior (mm)', 'FontSize', 12);
title({'BrainGNN 3D Pain Region Mapping (98.7% Accuracy)', ...
       'Size = Importance | Color = Activation'}, 'FontSize', 14);

% Add brain outline
hold on;
[x, y, z] = sphere(20);
surf(x*80, y*80, z*60, 'FaceAlpha', 0.1, 'EdgeAlpha', 0.05, 'FaceColor', [0.7, 0.7, 0.7]);

% Add labels for important regions
for i = 1:n_regions
    if importances(i) > 0.015
        text(coords(i, 1) + 5, coords(i, 2) + 5, coords(i, 3) + 5, ...
             region_names{i}, 'FontSize', 8, 'FontWeight', 'normal');
    end
end

grid on;
view(45, 15);

%% Activation ranking
subplot(2, 2, 2);

[~, sort_idx] = sort(abs(activations), 'descend');
sorted_names = region_names(sort_idx);
sorted_values = activations(sort_idx);

% Create colors based on positive/negative activation
colors = zeros(length(sorted_values), 3);
for i = 1:length(sorted_values)
    if sorted_values(i) > 0
        colors(i, :) = [1, 0.3, 0.3];  % Red
    else
        colors(i, :) = [0.3, 0.3, 1];  % Blue
    end
end

% Horizontal bar chart
for i = 1:length(sorted_values)
    barh(i, sorted_values(i), 'FaceColor', colors(i, :), 'EdgeColor', 'black');
    hold on;
end

yticks(1:length(sorted_names));
yticklabels(sorted_names);
xlabel('Activation Difference');
title('Brain Region Activation Ranking');
grid on;

% Add zero line
line([0, 0], [0.5, length(sorted_values) + 0.5], 'Color', 'black', 'LineWidth', 2);

%% Network distribution
subplot(2, 2, 4);

% Define networks
networks = {
    'Cerebellum'; 'Cerebellum'; 'Cerebellum';
    'Visual'; 'Visual'; 'Visual';
    'Frontal'; 'Frontal'; 'Frontal';
    'Sensorimotor'; 'Sensorimotor'; 'Sensorimotor';
    'Limbic'; 'Limbic'; 'Limbic';
    'Subcortical'; 'Subcortical';
};

unique_networks = unique(networks);
network_counts = zeros(length(unique_networks), 1);

for i = 1:length(unique_networks)
    network_counts(i) = sum(strcmp(networks, unique_networks{i}));
end

pie(network_counts);
legend(unique_networks, 'Location', 'eastoutside');
title('Pain Processing Networks');

%% Save figures
fprintf('💾 Saving MATLAB brain visualization...\n');

% Save as PNG
print('./matlab_figures/simple_matlab_brain_map', '-dpng', '-r300');

% Save as PDF
print('./matlab_figures/simple_matlab_brain_map', '-dpdf');

% Save as MATLAB figure
saveas(gcf, './matlab_figures/simple_matlab_brain_map.fig');

%% Create clean presentation figure
figure('Position', [150, 150, 1200, 800], 'Color', 'white');

% Large 3D scatter plot
scatter3(coords(:, 1), coords(:, 2), coords(:, 3), ...
         importances * 3000, activations, 'filled', ...
         'MarkerEdgeColor', 'black', 'LineWidth', 2);

% Enhanced colormap
colormap(jet);
caxis([-0.6, 0.6]);

% Brain surface
hold on;
[x, y, z] = sphere(25);
surf(x*85, y*85, z*65, 'FaceAlpha', 0.05, 'EdgeAlpha', 0.02, 'FaceColor', [0.8, 0.8, 0.8]);

% Labels
for i = 1:n_regions
    text(coords(i, 1) + 8, coords(i, 2) + 8, coords(i, 3) + 8, ...
         region_names{i}, 'FontSize', 9, 'FontWeight', 'bold');
end

% Colorbar
cb = colorbar;
cb.Label.String = 'Pain Activation Difference';
cb.Label.FontSize = 14;

% Styling
xlabel('Left <- -> Right (mm)', 'FontSize', 14);
ylabel('Posterior <- -> Anterior (mm)', 'FontSize', 14);
zlabel('Inferior <- -> Superior (mm)', 'FontSize', 14);

title({'Enhanced 3D Brain Pain Mapping - BrainGNN Analysis', ...
       'Model Accuracy: 98.7% | 17 Key Pain Processing Regions'}, ...
      'FontSize', 16);

grid on;
view(30, 20);

% Save presentation figure
print('./matlab_figures/presentation_brain_3d', '-dpng', '-r300');
print('./matlab_figures/presentation_brain_3d', '-dpdf');
saveas(gcf, './matlab_figures/presentation_brain_3d.fig');

%% Summary
fprintf('✅ MATLAB brain mapping completed!\n');
fprintf('📂 Generated files:\n');
fprintf('  • simple_matlab_brain_map.png/pdf/fig\n');
fprintf('  • presentation_brain_3d.png/pdf/fig\n');
fprintf('🧠 Analysis of %d key pain processing regions\n', n_regions);
fprintf('📊 Model achieved 98.7%% accuracy\n');
fprintf('🎯 Clean visualizations without font issues\n\n');