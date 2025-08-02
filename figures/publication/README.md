# BrainGNN Publication Quality Brain Visualization

## Overview
High-impact journal publication visualization of BrainGNN pain state classification results.

## Model Performance
- **Accuracy**: 98.7%
- **Classification**: Binary (Pain vs No-Pain states)
- **Brain Regions**: 14 key areas analyzed
- **Networks**: 7 pain processing networks identified

## Generated Visualizations

### 1. ParaView 3D Visualization
- **Purpose**: High-resolution 3D brain surface mapping
- **Files**: `./paraview_data/`
- **Output**: 4K resolution images for main figures
- **Usage**: Run `paraview_brain_visualization.py` in ParaView

### 2. BrainNet Viewer Analysis
- **Purpose**: Standard neuroimaging publication format
- **Files**: `./results/node/`, `./results/edge/`, `./results/dpv/`
- **Output**: Multiple anatomical views (lateral, superior, anterior)
- **Usage**: Run `publication_brainnet_script.m` in MATLAB

### 3. 3D Publication Views
- **Purpose**: Multi-panel figure for publication
- **Files**: `./figures/publication/3d_brain_publication_views.png`
- **Features**: 4 standard anatomical views with activation mapping

## Key Findings
1. **Cerebellar Network**: Primary sensorimotor integration during pain
2. **Visual Network**: Enhanced spatial attention to pain stimuli  
3. **Executive Network**: Top-down cognitive control (suppressed during pain)
4. **Hemispheric Lateralization**: Left-dominant cognitive control

## Publication Recommendations
- Use ParaView images for main figures (high resolution)
- Include BrainNet multi-view panels for anatomical context
- Reference standard brain atlas coordinates (MNI space)
- Cite appropriate software packages

## File Structure
```
./paraview_data/          # ParaView VTK files
./results/node/           # BrainNet node files  
./results/edge/           # BrainNet edge files
./results/dpv/            # BrainNet surface files
./figures/publication/    # High-resolution outputs
```

## Software Requirements
- ParaView 5.9+ (for 3D surface visualization)
- MATLAB + BrainNet Viewer (for standard brain mapping)
- Python 3.8+ (for data processing)

## Citation
When using these visualizations, please cite:
- BrainGNN implementation: [Your paper]
- ParaView: Ahrens et al. (2005)  
- BrainNet Viewer: Xia et al. (2013)
