%% Professional Brain Mapping using MATLAB
% BrainGNN Pain Region Analysis - High Quality Visualization
% 98.7% Accuracy Model Results

clear; clc; close all;

%% Setup paths and data
fprintf('🧠 Starting MATLAB Professional Brain Mapping...\n');
fprintf('📊 BrainGNN Model Accuracy: 98.7%%\n\n');

% Create results directory
if ~exist('./matlab_figures', 'dir')
    mkdir('./matlab_figures');
end

%% Define brain regions with activation data
% Based on BrainGNN analysis results
regions = {
    % Region Name, X, Y, Z, Activation, Network, Importance
    'Cerebelum_Crus1_R', 60, -75, -20, 0.601, 'Cerebellum', 0.022;
    'Cerebelum_Crus1_L', -60, -75, -20, 0.438, 'Cerebellum', 0.016;
    'Cerebelum_Crus2_R', 50, -65, -15, 0.391, 'Cerebellum', 0.014;
    'Occipital_Mid_R', 45, -90, 5, 0.528, 'Visual', 0.022;
    'Occipital_Sup_R', 25, -95, 10, 0.528, 'Visual', 0.022;
    'Occipital_Mid_L', -45, -90, 5, 0.385, 'Visual', 0.016;
    'Frontal_Sup_L', -35, 70, 25, -0.512, 'Frontal', 0.015;
    'Frontal_Mid_L', -50, 45, 20, -0.498, 'Frontal', 0.014;
    'Frontal_Sup_R', 35, 70, 25, -0.394, 'Frontal', 0.011;
    'Precentral_L', -40, 25, 50, -0.433, 'Sensorimotor', 0.013;
    'Postcentral_L', -40, -20, 50, -0.431, 'Sensorimotor', 0.012;
    'Rolandic_Oper_L', -55, 5, 15, -0.401, 'Sensorimotor', 0.019;
    'Amygdala_R', 25, -10, -10, 0.080, 'Limbic', 0.015;
    'Cingulum_Ant_R', 12, 40, 25, 0.065, 'Limbic', 0.013;
    'ParaHippocampal_L', -30, -35, -15, 0.120, 'Limbic', 0.019;
    'Thalamus_L', -15, -15, 5, 0.055, 'Subcortical', 0.011;
    'Putamen_R', 25, 5, 0, -0.386, 'Subcortical', 0.009;
};

n_regions = size(regions, 1);

%% Extract coordinates and activation values
coords = cell2mat(regions(:, 2:4));
activations = cell2mat(regions(:, 5));
importances = cell2mat(regions(:, 7));
region_names = regions(:, 1);

%% Create comprehensive brain visualization
figure('Position', [100, 100, 1600, 1200], 'Color', 'white');

%% Main 3D brain plot
subplot(2, 3, [1, 2, 4, 5]);

% Create 3D scatter plot
scatter3(coords(:, 1), coords(:, 2), coords(:, 3), ...
         importances * 2000, activations, 'filled', 'MarkerEdgeColor', 'k', 'LineWidth', 1.5);

% Customize colormap for activation
colormap(gca, [linspace(0, 1, 128)' linspace(0, 1, 128)' ones(128, 1); ...  % Blue to white
               ones(128, 1) linspace(1, 0, 128)' linspace(1, 0, 128)']);      % White to red

% Add colorbar
cb = colorbar;
cb.Label.String = 'Activation Difference (Pain - No Pain)';
cb.Label.FontSize = 12;
cb.Label.FontWeight = 'bold';

% Set axis properties
xlabel('Left ← → Right (mm)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Posterior ← → Anterior (mm)', 'FontSize', 12, 'FontWeight', 'bold');
zlabel('Inferior ← → Superior (mm)', 'FontSize', 12, 'FontWeight', 'bold');

title({'BrainGNN 3D Pain Region Mapping (98.7% Accuracy)', ...
       'Circle Size = Importance | Color = Activation Strength'}, ...
      'FontSize', 14, 'FontWeight', 'bold');

% Add brain outline (simplified)
hold on;
[x, y, z] = sphere(20);
brain_surface = surf(x*80, y*80, z*60, 'FaceAlpha', 0.1, ...
                    'EdgeAlpha', 0.1, 'FaceColor', [0.5, 0.5, 0.5]);

% Add region labels for key regions
for i = 1:n_regions
    if importances(i) > 0.015  % Only label high-importance regions
        text(coords(i, 1) + 5, coords(i, 2) + 5, coords(i, 3) + 5, ...
             strrep(region_names{i}, '_', ' '), ...
             'FontSize', 8, 'FontWeight', 'bold', ...
             'BackgroundColor', 'white', 'EdgeColor', 'black', ...
             'Margin', 2);
    end
end

grid on;
axis equal;
view(45, 15);

%% Network distribution pie chart
subplot(2, 3, 3);

networks = regions(:, 6);
unique_networks = unique(networks);
network_counts = zeros(length(unique_networks), 1);

for i = 1:length(unique_networks)
    network_counts(i) = sum(strcmp(networks, unique_networks{i}));
end

% Define colors for networks
network_colors = [
    1, 0.27, 0.27;    % Cerebellum - Red
    1, 0.53, 0.27;    % Visual - Orange
    0.27, 0.27, 1;    % Frontal - Blue
    0.4, 0.4, 1;      % Sensorimotor - Light Blue
    0.67, 0.27, 0.67; % Limbic - Purple
    0.27, 0.67, 0.27; % Subcortical - Green
];

pie(network_counts, unique_networks);
colormap(gca, network_colors);
title('Pain Processing Networks', 'FontSize', 12, 'FontWeight', 'bold');

%% Activation ranking bar chart
subplot(2, 3, 6);

[sorted_activations, sort_idx] = sort(abs(activations), 'descend');
sorted_names = region_names(sort_idx);
sorted_values = activations(sort_idx);
sorted_importance = importances(sort_idx);

% Create horizontal bar chart
barh_colors = zeros(length(sorted_values), 3);
for i = 1:length(sorted_values)
    if sorted_values(i) > 0
        barh_colors(i, :) = [1, 0.2, 0.2];  % Red for enhancement
    else
        barh_colors(i, :) = [0.2, 0.2, 1];  % Blue for suppression
    end
end

b = barh(1:length(sorted_values), sorted_values);
b.FaceColor = 'flat';
b.CData = barh_colors;

% Highlight important regions
hold on;
for i = 1:length(sorted_values)
    if sorted_importance(i) > 0.015
        barh(i, sorted_values(i), 'EdgeColor', [1, 0.84, 0], 'LineWidth', 3);
    end
end

yticks(1:length(sorted_names));
yticklabels(strrep(sorted_names, '_', ' '));
xlabel('Activation Difference', 'FontSize', 11, 'FontWeight', 'bold');
title({'Brain Region Activation Ranking', '(Gold border = Key regions)'}, ...
      'FontSize', 12, 'FontWeight', 'bold');
grid on;

% Add vertical line at zero
line([0, 0], [0.5, length(sorted_values) + 0.5], 'Color', 'black', 'LineWidth', 1);

%% Add overall statistics
annotation('textbox', [0.02, 0.02, 0.4, 0.15], ...
    'String', {
        'MODEL PERFORMANCE:', ...
        sprintf('• Accuracy: 98.7%% (Target: 80%%+) ✓'), ...
        sprintf('• F1-Score: 98.1%%'), ...
        sprintf('• Key Regions: %d', n_regions), ...
        '', ...
        'KEY FINDINGS:', ...
        sprintf('• Strongest Enhancement: %s (+%.3f)', ...
                strrep(region_names{activations == max(activations)}, '_', ' '), max(activations)), ...
        sprintf('• Strongest Suppression: %s (%.3f)', ...
                strrep(region_names{activations == min(activations)}, '_', ' '), min(activations)), ...
        '• Primary Network: Cerebellum sensorimotor integration', ...
        '• Control Mechanism: Frontal cognitive inhibition'
    }, ...
    'FontSize', 10, 'FontWeight', 'bold', ...
    'BackgroundColor', [0.88, 1, 1], 'EdgeColor', 'black', ...
    'VerticalAlignment', 'top');

%% Save figures
fprintf('💾 Saving MATLAB brain visualization...\n');

% Save as high-resolution PNG
print('./matlab_figures/matlab_professional_brain_map', '-dpng', '-r300');

% Save as PDF
print('./matlab_figures/matlab_professional_brain_map', '-dpdf', '-r300');

% Save as MATLAB figure
saveas(gcf, './matlab_figures/matlab_professional_brain_map.fig');

fprintf('✅ MATLAB brain mapping completed!\n');
fprintf('📂 Saved files:\n');
fprintf('  • matlab_professional_brain_map.png\n');
fprintf('  • matlab_professional_brain_map.pdf\n');
fprintf('  • matlab_professional_brain_map.fig\n\n');

%% Create enhanced 3D visualization for presentation
figure('Position', [150, 150, 1200, 800], 'Color', 'white');

% Enhanced 3D scatter with better lighting
scatter3(coords(:, 1), coords(:, 2), coords(:, 3), ...
         importances * 3000, activations, 'filled', ...
         'MarkerEdgeColor', 'k', 'LineWidth', 2, 'MarkerFaceAlpha', 0.8);

% Enhanced colormap
colormap([0, 0, 1; 0, 0.5, 1; 0.5, 0.8, 1; 1, 1, 1; 1, 0.8, 0.5; 1, 0.5, 0; 1, 0, 0]);

% Add enhanced brain surface
hold on;
[x, y, z] = sphere(30);
brain_surface = surf(x*85, y*85, z*65, ...
                    'FaceAlpha', 0.05, 'EdgeAlpha', 0.02, ...
                    'FaceColor', [0.8, 0.8, 0.8]);

% Enhanced lighting
light('Position', [100, 100, 100], 'Style', 'local');
light('Position', [-100, -100, 100], 'Style', 'local');
lighting gouraud;

% Enhanced labels for all regions
for i = 1:n_regions
    region_label = strrep(region_names{i}, '_', ' ');
    if length(region_label) > 15
        region_label = region_label(1:15);
    end
    
    text(coords(i, 1) + 8, coords(i, 2) + 8, coords(i, 3) + 8, ...
         region_label, 'FontSize', 9, 'FontWeight', 'bold', ...
         'BackgroundColor', 'white', 'EdgeColor', 'black', ...
         'Margin', 3, 'Rotation', 0);
end

% Enhanced colorbar
cb = colorbar('Location', 'eastoutside');
cb.Label.String = 'Pain Activation Difference';
cb.Label.FontSize = 14;
cb.Label.FontWeight = 'bold';
cb.FontSize = 12;

% Enhanced axis properties
xlabel('Left ← → Right (mm)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('Posterior ← → Anterior (mm)', 'FontSize', 14, 'FontWeight', 'bold');
zlabel('Inferior ← → Superior (mm)', 'FontSize', 14, 'FontWeight', 'bold');

title({'Enhanced 3D Brain Pain Mapping - BrainGNN Analysis', ...
       'Model Accuracy: 98.7% | 17 Key Pain Processing Regions', ...
       'Red = Enhanced Activation | Blue = Suppressed Activation'}, ...
      'FontSize', 16, 'FontWeight', 'bold');

grid on;
axis equal;
view(30, 20);

% Save enhanced version
print('./matlab_figures/enhanced_3d_brain_matlab', '-dpng', '-r300');
print('./matlab_figures/enhanced_3d_brain_matlab', '-dpdf', '-r300');
saveas(gcf, './matlab_figures/enhanced_3d_brain_matlab.fig');

fprintf('✅ Enhanced 3D visualization completed!\n');
fprintf('📂 Additional files saved:\n');
fprintf('  • enhanced_3d_brain_matlab.png\n');
fprintf('  • enhanced_3d_brain_matlab.pdf\n');
fprintf('  • enhanced_3d_brain_matlab.fig\n\n');

%% Summary
fprintf('🎉 MATLAB Brain Mapping Summary:\n');
fprintf('   • Created professional 3D brain visualizations\n');
fprintf('   • No font encoding issues\n');
fprintf('   • High-resolution outputs (300 DPI)\n');
fprintf('   • Multiple formats: PNG, PDF, FIG\n');
fprintf('   • Based on 98.7%% accuracy BrainGNN model\n');
fprintf('   • Analysis of %d key pain processing regions\n\n', n_regions);

fprintf('🧠 Use these visualizations for:\n');
fprintf('   • Scientific presentations\n');
fprintf('   • Research publications\n');
fprintf('   • Clinical applications\n');
fprintf('   • Educational materials\n\n');