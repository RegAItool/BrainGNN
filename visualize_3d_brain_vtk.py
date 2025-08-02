#!/usr/bin/env python3
"""
3D Brain Visualization from VTK Files
Alternative visualization using matplotlib 3D and vtk data
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

def read_vtk_points(vtk_file):
    """Read points and scalars from VTK file"""
    
    points = []
    scalars = {}
    current_scalar = None
    
    with open(vtk_file, 'r') as f:
        lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Find POINTS section
            if line.startswith('POINTS'):
                num_points = int(line.split()[1])
                i += 1
                for j in range(num_points):
                    coords = lines[i + j].strip().split()
                    points.append([float(x) for x in coords])
                i += num_points
                
            # Find SCALARS sections
            elif line.startswith('SCALARS'):
                scalar_name = line.split()[1]
                scalars[scalar_name] = []
                current_scalar = scalar_name
                i += 2  # Skip LOOKUP_TABLE line
                
            elif current_scalar and line and not line.startswith('SCALARS') and not line.startswith('LOOKUP_TABLE'):
                try:
                    if line.strip():  # Skip empty lines
                        scalars[current_scalar].append(float(line.strip()))
                except:
                    pass
                    
            i += 1
    
    return np.array(points), scalars

def create_3d_brain_visualization():
    """Create 3D brain visualization from VTK data"""
    
    print("📊 Loading VTK brain data...")
    
    # Read VTK data
    points, scalars = read_vtk_points('./paraview_data/brain_regions_pain.vtk')
    
    # Read metadata
    with open('./paraview_data/brain_analysis_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Create figure with multiple views
    fig = plt.figure(figsize=(20, 15))
    
    # === View 1: Activation Difference ===
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    
    # Get activation differences
    activation_diff = np.array(scalars['activation_diff'])
    
    # Color mapping
    colors = plt.cm.RdBu_r((activation_diff - activation_diff.min()) / 
                          (activation_diff.max() - activation_diff.min()))
    
    # Size based on importance
    importance = np.array(scalars['combined_importance'])
    sizes = 50 + 200 * (importance - importance.min()) / (importance.max() - importance.min())
    
    # Plot brain regions
    scatter1 = ax1.scatter(points[:, 0], points[:, 1], points[:, 2], 
                          c=activation_diff, s=sizes, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=1)
    
    ax1.set_xlabel('Left ← → Right (mm)')
    ax1.set_ylabel('Posterior ← → Anterior (mm)')
    ax1.set_zlabel('Inferior ← → Superior (mm)')
    ax1.set_title('Pain Activation Differences\n(Red=Enhanced, Blue=Suppressed)', fontsize=12)
    
    # Add colorbar
    cbar1 = plt.colorbar(scatter1, ax=ax1, shrink=0.6, pad=0.1)
    cbar1.set_label('Activation Difference')
    
    # === View 2: Combined Importance ===
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    
    # Top-K indicator
    top_k = np.array(scalars['top_k_indicator'])
    colors_topk = ['gold' if tk == 1 else 'lightgray' for tk in top_k]
    sizes_topk = [300 if tk == 1 else 100 for tk in top_k]
    
    scatter2 = ax2.scatter(points[:, 0], points[:, 1], points[:, 2], 
                          c=colors_topk, s=sizes_topk, 
                          alpha=0.8, edgecolors='black', linewidth=1)
    
    ax2.set_xlabel('Left ← → Right (mm)')
    ax2.set_ylabel('Posterior ← → Anterior (mm)')
    ax2.set_zlabel('Inferior ← → Superior (mm)')
    ax2.set_title('Top-15 Important Brain Regions\n(Gold=Top-K, Gray=Others)', fontsize=12)
    
    # === View 3: Statistical Significance ===
    ax3 = fig.add_subplot(2, 3, 3, projection='3d')
    
    # P-values
    p_values = np.array(scalars['p_value'])
    
    # Color by significance
    sig_colors = []
    for p in p_values:
        if p < 0.001:
            sig_colors.append('darkred')
        elif p < 0.01:
            sig_colors.append('red')
        elif p < 0.05:
            sig_colors.append('orange')
        else:
            sig_colors.append('gray')
    
    scatter3 = ax3.scatter(points[:, 0], points[:, 1], points[:, 2], 
                          c=sig_colors, s=150, 
                          alpha=0.8, edgecolors='black', linewidth=1)
    
    ax3.set_xlabel('Left ← → Right (mm)')
    ax3.set_ylabel('Posterior ← → Anterior (mm)')
    ax3.set_zlabel('Inferior ← → Superior (mm)')
    ax3.set_title('Statistical Significance\n(Red=p<0.001, Orange=p<0.05, Gray=n.s.)', fontsize=12)
    
    # === View 4: Sagittal View (Side) ===
    ax4 = fig.add_subplot(2, 3, 4)
    
    scatter4 = ax4.scatter(points[:, 1], points[:, 2], 
                          c=activation_diff, s=sizes/2, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    ax4.set_xlabel('Posterior ← → Anterior (mm)')
    ax4.set_ylabel('Inferior ← → Superior (mm)')
    ax4.set_title('Sagittal View (Side)', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')
    
    # === View 5: Coronal View (Front) ===
    ax5 = fig.add_subplot(2, 3, 5)
    
    scatter5 = ax5.scatter(points[:, 0], points[:, 2], 
                          c=activation_diff, s=sizes/2, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    ax5.set_xlabel('Left ← → Right (mm)')
    ax5.set_ylabel('Inferior ← → Superior (mm)')
    ax5.set_title('Coronal View (Front)', fontsize=12)
    ax5.grid(True, alpha=0.3)
    ax5.set_aspect('equal')
    
    # === View 6: Axial View (Top) ===
    ax6 = fig.add_subplot(2, 3, 6)
    
    scatter6 = ax6.scatter(points[:, 0], points[:, 1], 
                          c=activation_diff, s=sizes/2, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    
    ax6.set_xlabel('Left ← → Right (mm)')
    ax6.set_ylabel('Posterior ← → Anterior (mm)')
    ax6.set_title('Axial View (Top)', fontsize=12)
    ax6.grid(True, alpha=0.3)
    ax6.set_aspect('equal')
    
    # Main title
    fig.suptitle('3D Brain Pain Processing Visualization from ParaView VTK Data\n'
                'FC+GNN Analysis: Top-K Selection & Structural Attention\n'
                f'{len(points)} Brain Regions Analyzed', 
                fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig('./figures/3d_brain_vtk_visualization.png', dpi=300, bbox_inches='tight')
    plt.savefig('./figures/3d_brain_vtk_visualization.pdf', bbox_inches='tight')
    
    print("✅ 3D brain visualization saved to ./figures/3d_brain_vtk_visualization.png/pdf")
    
    # === Create Network Visualization ===
    create_network_visualization(points, scalars, metadata)
    
    return fig

def create_network_visualization(points, scalars, metadata):
    """Create brain network visualization"""
    
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get top-K regions
    top_k_indices = np.where(np.array(scalars['top_k_indicator']) == 1)[0]
    
    # Plot all regions with transparency
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
              c='lightgray', s=50, alpha=0.3)
    
    # Highlight top-K regions
    activation_diff = np.array(scalars['activation_diff'])
    importance = np.array(scalars['combined_importance'])
    
    for idx in top_k_indices:
        # Region color based on activation
        if activation_diff[idx] > 0:
            color = 'red'
        else:
            color = 'blue'
        
        # Size based on importance
        size = 100 + 500 * importance[idx] / importance.max()
        
        ax.scatter(points[idx, 0], points[idx, 1], points[idx, 2], 
                  c=color, s=size, alpha=0.9, edgecolors='black', linewidth=2)
        
        # Add region label
        region_info = metadata['regions'][idx]
        ax.text(points[idx, 0], points[idx, 1], points[idx, 2] + 10, 
               region_info['name'].split('_')[0], 
               fontsize=8, fontweight='bold', ha='center')
    
    # Draw connections between top-K regions
    for i, idx1 in enumerate(top_k_indices):
        for j, idx2 in enumerate(top_k_indices[i+1:], i+1):
            # Only draw strong connections
            if importance[idx1] > 0.5 and importance[idx2] > 0.5:
                ax.plot([points[idx1, 0], points[idx2, 0]], 
                       [points[idx1, 1], points[idx2, 1]], 
                       [points[idx1, 2], points[idx2, 2]], 
                       'gray', alpha=0.3, linewidth=1)
    
    ax.set_xlabel('Left ← → Right (mm)')
    ax.set_ylabel('Posterior ← → Anterior (mm)')
    ax.set_zlabel('Inferior ← → Superior (mm)')
    ax.set_title('Top-K Brain Network Connectivity\n'
                '(Red=Pain Enhanced, Blue=Pain Suppressed)', fontsize=14)
    
    # Set viewing angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    
    plt.savefig('./figures/3d_brain_network_visualization.png', dpi=300, bbox_inches='tight')
    plt.savefig('./figures/3d_brain_network_visualization.pdf', bbox_inches='tight')
    
    print("✅ 3D brain network saved to ./figures/3d_brain_network_visualization.png/pdf")

def print_top_regions_info():
    """Print information about top brain regions"""
    
    # Read metadata
    with open('./paraview_data/brain_analysis_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print("\n🧠 Top-K Brain Regions Analysis Summary:")
    print("=" * 60)
    
    top_k_regions = [r for r in metadata['regions'] if r['is_top_k']]
    
    print(f"\nTotal regions analyzed: {metadata['dataset_info']['num_regions']}")
    print(f"Top-K regions selected: {metadata['dataset_info']['num_top_k']}")
    print(f"\nBrain Networks Involved: {', '.join(metadata['networks'])}")
    
    print("\n📊 Top-K Regions Details:")
    print("-" * 60)
    
    # Sort by importance
    top_k_regions.sort(key=lambda x: x['combined_importance'], reverse=True)
    
    for i, region in enumerate(top_k_regions, 1):
        print(f"\n{i}. {region['name']}:")
        print(f"   • Activation: {region['activation_diff']:+.3f} ({region['activation_type']})")
        print(f"   • Importance: {region['combined_importance']:.3f}")
        print(f"   • Network: {region['network']}")
        print(f"   • MNI coords: {region['mni_coords']}")

def main():
    """Main function"""
    
    print("🎨 Creating 3D Brain Visualization from ParaView VTK Data...")
    print("📊 This is an alternative to ParaView software visualization")
    
    try:
        # Create visualizations
        fig = create_3d_brain_visualization()
        
        # Print region information
        print_top_regions_info()
        
        print("\n✨ 3D Brain Visualization Complete!")
        print("\n📁 Generated Files:")
        print("  • ./figures/3d_brain_vtk_visualization.png/pdf")
        print("  • ./figures/3d_brain_network_visualization.png/pdf")
        
        print("\n💡 To use ParaView software:")
        print("  1. Install ParaView from https://www.paraview.org/download/")
        print("  2. Open ParaView")
        print("  3. File → Open → Select brain_regions_pain.vtk")
        print("  4. Tools → Python Shell → Run Script → paraview_brain_visualization.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()