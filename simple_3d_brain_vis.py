#!/usr/bin/env python3
"""
Simple 3D Brain Visualization from VTK Data
Alternative to ParaView for viewing brain regions
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

def load_brain_data():
    """Load brain data from JSON metadata"""
    
    print("📊 Loading brain data from metadata...")
    
    with open('./paraview_data/brain_analysis_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Extract data
    regions = metadata['regions']
    
    points = np.array([r['mni_coords'] for r in regions])
    activation_diff = np.array([r['activation_diff'] for r in regions])
    importance = np.array([r['combined_importance'] for r in regions])
    is_top_k = np.array([r['is_top_k'] for r in regions])
    names = [r['name'] for r in regions]
    networks = [r['network'] for r in regions]
    activation_types = [r['activation_type'] for r in regions]
    
    return {
        'points': points,
        'activation_diff': activation_diff,
        'importance': importance,
        'is_top_k': is_top_k,
        'names': names,
        'networks': networks,
        'activation_types': activation_types,
        'metadata': metadata
    }

def create_3d_visualization():
    """Create comprehensive 3D brain visualization"""
    
    data = load_brain_data()
    points = data['points']
    activation_diff = data['activation_diff']
    importance = data['importance']
    is_top_k = data['is_top_k']
    names = data['names']
    
    # Create figure with multiple 3D views
    fig = plt.figure(figsize=(24, 16))
    
    # === Main 3D View: Activation Differences ===
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    
    # Size based on importance (normalized)
    sizes = 50 + 400 * (importance - importance.min()) / (importance.max() - importance.min() + 1e-8)
    
    # Color based on activation
    scatter1 = ax1.scatter(points[:, 0], points[:, 1], points[:, 2], 
                          c=activation_diff, s=sizes, 
                          cmap='RdBu_r', alpha=0.8, 
                          edgecolors='black', linewidth=1)
    
    # Add labels for top regions
    for i, is_top in enumerate(is_top_k):
        if is_top and abs(activation_diff[i]) > 0.0001:  # Only significant activations
            ax1.text(points[i, 0], points[i, 1], points[i, 2] + 10, 
                    names[i].split('_')[0], fontsize=8, fontweight='bold')
    
    ax1.set_xlabel('Left ← → Right (mm)')
    ax1.set_ylabel('Posterior ← → Anterior (mm)')
    ax1.set_zlabel('Inferior ← → Superior (mm)')
    ax1.set_title('Pain Activation Differences\\n(Red=Enhanced, Blue=Suppressed)', fontsize=12)
    ax1.view_init(elev=20, azim=45)
    
    # Colorbar
    cbar1 = plt.colorbar(scatter1, ax=ax1, shrink=0.6, pad=0.1)
    cbar1.set_label('Activation Difference')
    
    # === View 2: Top-K Regions Only ===
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    
    # Filter top-K regions
    top_k_indices = np.where(is_top_k)[0]
    top_k_points = points[top_k_indices]
    top_k_activation = activation_diff[top_k_indices]
    top_k_importance = importance[top_k_indices]
    top_k_names = [names[i] for i in top_k_indices]
    
    # Size based on importance
    top_k_sizes = 100 + 500 * (top_k_importance - top_k_importance.min()) / (top_k_importance.max() - top_k_importance.min() + 1e-8)
    
    scatter2 = ax2.scatter(top_k_points[:, 0], top_k_points[:, 1], top_k_points[:, 2], 
                          c=top_k_activation, s=top_k_sizes, 
                          cmap='RdBu_r', alpha=0.9, 
                          edgecolors='gold', linewidth=2)
    
    # Add all top-K labels
    for i, (point, name) in enumerate(zip(top_k_points, top_k_names)):
        ax2.text(point[0], point[1], point[2] + 10, 
                name.split('_')[0], fontsize=9, fontweight='bold', ha='center')
    
    ax2.set_xlabel('Left ← → Right (mm)')
    ax2.set_ylabel('Posterior ← → Anterior (mm)')
    ax2.set_zlabel('Inferior ← → Superior (mm)')
    ax2.set_title(f'Top-{len(top_k_indices)} Most Important Regions\\n(Size ∝ Importance)', fontsize=12)
    ax2.view_init(elev=20, azim=135)
    
    # === View 3: Network Connectivity ===
    ax3 = fig.add_subplot(2, 3, 3, projection='3d')
    
    # Show all regions with transparency
    ax3.scatter(points[:, 0], points[:, 1], points[:, 2], 
               c='lightgray', s=50, alpha=0.3)
    
    # Highlight top-K with network colors
    network_colors = {
        'cognitive_control': 'blue',
        'sensorimotor': 'green', 
        'visual': 'orange',
        'cerebellar': 'red',
        'limbic': 'purple',
        'subcortical': 'brown',
        'attention': 'pink',
        'auditory': 'cyan',
        'semantic': 'yellow'
    }
    
    for i in top_k_indices:
        network = data['networks'][i]
        color = network_colors.get(network, 'gray')
        
        ax3.scatter(points[i, 0], points[i, 1], points[i, 2], 
                   c=color, s=200, alpha=0.9, 
                   edgecolors='black', linewidth=2)
    
    # Draw connections between regions in same network
    for i, idx1 in enumerate(top_k_indices):
        for j, idx2 in enumerate(top_k_indices[i+1:], i+1):
            if data['networks'][idx1] == data['networks'][idx2]:
                ax3.plot([points[idx1, 0], points[idx2, 0]], 
                        [points[idx1, 1], points[idx2, 1]], 
                        [points[idx1, 2], points[idx2, 2]], 
                        network_colors.get(data['networks'][idx1], 'gray'), 
                        alpha=0.4, linewidth=2)
    
    ax3.set_xlabel('Left ← → Right (mm)')
    ax3.set_ylabel('Posterior ← → Anterior (mm)')
    ax3.set_zlabel('Inferior ← → Superior (mm)')
    ax3.set_title('Brain Network Connectivity\\n(Colors = Networks)', fontsize=12)
    ax3.view_init(elev=30, azim=60)
    
    # === 2D Views ===
    
    # Sagittal view (side)
    ax4 = fig.add_subplot(2, 3, 4)
    scatter4 = ax4.scatter(points[:, 1], points[:, 2], 
                          c=activation_diff, s=sizes/3, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    ax4.set_xlabel('Posterior ← → Anterior (mm)')
    ax4.set_ylabel('Inferior ← → Superior (mm)')
    ax4.set_title('Sagittal View (Side)', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')
    
    # Coronal view (front)
    ax5 = fig.add_subplot(2, 3, 5)
    scatter5 = ax5.scatter(points[:, 0], points[:, 2], 
                          c=activation_diff, s=sizes/3, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    ax5.set_xlabel('Left ← → Right (mm)')
    ax5.set_ylabel('Inferior ← → Superior (mm)')
    ax5.set_title('Coronal View (Front)', fontsize=12)
    ax5.grid(True, alpha=0.3)
    ax5.set_aspect('equal')
    
    # Axial view (top)
    ax6 = fig.add_subplot(2, 3, 6)
    scatter6 = ax6.scatter(points[:, 0], points[:, 1], 
                          c=activation_diff, s=sizes/3, 
                          cmap='RdBu_r', alpha=0.8, edgecolors='black', linewidth=0.5)
    ax6.set_xlabel('Left ← → Right (mm)')
    ax6.set_ylabel('Posterior ← → Anterior (mm)')
    ax6.set_title('Axial View (Top)', fontsize=12)
    ax6.grid(True, alpha=0.3)
    ax6.set_aspect('equal')
    
    # Main title
    fig.suptitle('3D Brain Pain Processing Visualization\\n'
                'FC+GNN Analysis: ParaView Data Alternative\\n'
                f'{len(points)} Brain Regions | Top-{len(top_k_indices)} Selected', 
                fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig('./figures/3d_brain_paraview_alternative.png', dpi=300, bbox_inches='tight')
    plt.savefig('./figures/3d_brain_paraview_alternative.pdf', bbox_inches='tight')
    
    print("✅ 3D brain visualization saved to ./figures/3d_brain_paraview_alternative.png/pdf")
    
    return fig, data

def print_analysis_summary(data):
    """Print analysis summary"""
    
    metadata = data['metadata']
    top_k_regions = [r for r in metadata['regions'] if r['is_top_k']]
    
    print("\\n🧠 3D Brain Pain Analysis Summary:")
    print("=" * 60)
    print(f"Total Brain Regions: {len(data['points'])}")
    print(f"Top-K Selected: {len(top_k_regions)}")
    print(f"Networks Involved: {len(set(data['networks']))}")
    
    print("\\n📊 Top-5 Most Important Regions:")
    print("-" * 40)
    
    # Sort by importance
    sorted_regions = sorted(enumerate(data['importance']), key=lambda x: x[1], reverse=True)
    
    for i, (idx, importance) in enumerate(sorted_regions[:5]):
        name = data['names'][idx]
        activation = data['activation_diff'][idx]
        network = data['networks'][idx]
        act_type = data['activation_types'][idx]
        
        print(f"{i+1}. {name}")
        print(f"   • Importance: {importance:.3f}")
        print(f"   • Activation: {activation:+.6f} ({act_type})")
        print(f"   • Network: {network}")
        print(f"   • MNI: {data['points'][idx]}")
    
    print("\\n🎨 ParaView Files Generated:")
    print("-" * 40)
    print("• brain_regions_pain.vtk (3D brain regions)")
    print("• brain_connectivity_network.vtk (network connections)")
    print("• brain_analysis_metadata.json (analysis data)")
    print("• paraview_brain_visualization.py (auto script)")
    
    print("\\n💡 To Use ParaView:")
    print("-" * 40)
    print("1. Install ParaView: https://www.paraview.org/download/")
    print("2. Open ParaView")
    print("3. File → Open → brain_regions_pain.vtk")
    print("4. Add Glyph filter (sphere representation)")
    print("5. Color by 'activation_diff' or 'combined_importance'")
    print("6. For automation: Tools → Python Shell → Run Script")

def main():
    """Main function"""
    
    print("🎨 Creating 3D Brain Visualization (ParaView Alternative)")
    print("📊 Loading data from FC+GNN analysis results...")
    
    try:
        fig, data = create_3d_visualization()
        print_analysis_summary(data)
        
        print("\\n✨ 3D Brain Visualization Complete!")
        print("\\n📁 Generated Alternative Visualization:")
        print("  • ./figures/3d_brain_paraview_alternative.png/pdf")
        
        print("\\n🔍 Key Features Visualized:")
        print("  • 3D spatial brain region mapping")
        print("  • Pain activation vs suppression patterns")
        print("  • Top-K region importance ranking")
        print("  • Brain network connectivity")
        print("  • Multiple anatomical views (3D + 2D projections)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()