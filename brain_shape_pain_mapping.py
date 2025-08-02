#!/usr/bin/env python3
"""
Brain Shape Pain Mapping - BrainGNN 2-Class Visualization
Pain vs No-Pain Brain State Analysis with Realistic Brain Shape
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

class BrainShapePainMapper:
    """Brain Shape Pain State Mapper"""
    
    def __init__(self):
        self.setup_brain_anatomy()
        self.setup_pain_regions()
        self.setup_colors()
    
    def setup_brain_anatomy(self):
        """Setup brain anatomical structure"""
        
        # Realistic brain outline coordinates
        self.brain_outline = {
            # Main cerebral cortex
            'cortex': np.array([
                [-75, 65], [-70, 75], [-60, 85], [-45, 90], [-25, 92], [0, 93], 
                [25, 92], [45, 90], [60, 85], [70, 75], [75, 65], [78, 50],
                [80, 30], [78, 10], [75, -10], [70, -30], [65, -45], [55, -60],
                [45, -70], [30, -75], [15, -78], [0, -80], [-15, -78], [-30, -75],
                [-45, -70], [-55, -60], [-65, -45], [-70, -30], [-75, -10], 
                [-78, 10], [-80, 30], [-78, 50], [-75, 65]
            ]),
            
            # Cerebellum
            'cerebellum': np.array([
                [-55, -75], [-45, -85], [-35, -90], [-20, -92], [0, -93],
                [20, -92], [35, -90], [45, -85], [55, -75], [50, -65],
                [40, -55], [25, -50], [0, -48], [-25, -50], [-40, -55],
                [-50, -65], [-55, -75]
            ]),
            
            # Brainstem
            'brainstem': np.array([
                [-8, -45], [-6, -55], [-4, -65], [-2, -70], [0, -72],
                [2, -70], [4, -65], [6, -55], [8, -45], [6, -35],
                [4, -30], [2, -28], [0, -27], [-2, -28], [-4, -30],
                [-6, -35], [-8, -45]
            ])
        }
    
    def setup_pain_regions(self):
        """Setup pain-related brain regions"""
        
        # Based on BrainGNN analysis results
        self.pain_regions = {
            # PAIN STATE - Enhanced activation during pain
            'pain_enhanced': {
                'Cerebelum_Crus1_R': {
                    'pos': (45, -75), 'size': 12, 'activation': 0.601,
                    'area': 'cerebellum', 'description': 'Sensorimotor integration'
                },
                'Cerebelum_Crus1_L': {
                    'pos': (-45, -75), 'size': 10, 'activation': 0.438,
                    'area': 'cerebellum', 'description': 'Bilateral coordination'
                },
                'Occipital_Mid_R': {
                    'pos': (35, -85), 'size': 11, 'activation': 0.528,
                    'area': 'occipital', 'description': 'Visual-spatial processing'
                },
                'Occipital_Sup_R': {
                    'pos': (25, -95), 'size': 10, 'activation': 0.528,
                    'area': 'occipital', 'description': 'Visual attention'
                },
                'Occipital_Mid_L': {
                    'pos': (-35, -85), 'size': 9, 'activation': 0.385,
                    'area': 'occipital', 'description': 'Visual processing'
                },
                'ParaHippocampal_L': {
                    'pos': (-30, -35), 'size': 8, 'activation': 0.120,
                    'area': 'temporal', 'description': 'Memory encoding'
                },
                'Amygdala_R': {
                    'pos': (25, -10), 'size': 7, 'activation': 0.080,
                    'area': 'temporal', 'description': 'Emotional response'
                }
            },
            
            # NO-PAIN STATE - Suppressed during pain (active during no-pain)
            'no_pain_active': {
                'Frontal_Sup_L': {
                    'pos': (-35, 70), 'size': 11, 'activation': -0.512,
                    'area': 'frontal', 'description': 'Cognitive control'
                },
                'Frontal_Mid_L': {
                    'pos': (-50, 45), 'size': 10, 'activation': -0.498,
                    'area': 'frontal', 'description': 'Executive function'
                },
                'Precentral_L': {
                    'pos': (-40, 25), 'size': 10, 'activation': -0.433,
                    'area': 'frontal', 'description': 'Motor control'
                },
                'Postcentral_L': {
                    'pos': (-40, -20), 'size': 9, 'activation': -0.431,
                    'area': 'parietal', 'description': 'Sensory processing'
                },
                'Rolandic_Oper_L': {
                    'pos': (-55, 5), 'size': 9, 'activation': -0.401,
                    'area': 'frontal', 'description': 'Sensorimotor integration'
                },
                'Frontal_Sup_R': {
                    'pos': (35, 70), 'size': 8, 'activation': -0.394,
                    'area': 'frontal', 'description': 'Bilateral control'
                },
                'Putamen_R': {
                    'pos': (25, 5), 'size': 7, 'activation': -0.386,
                    'area': 'subcortical', 'description': 'Motor regulation'
                }
            }
        }
    
    def setup_colors(self):
        """Setup color schemes"""
        
        self.pain_color = '#FF3333'      # Red for pain state
        self.no_pain_color = '#3333FF'   # Blue for no-pain state
        
        self.anatomy_colors = {
            'frontal': '#FFE6E6',
            'parietal': '#E6F2FF', 
            'temporal': '#E6FFE6',
            'occipital': '#FFFFE6',
            'cerebellum': '#F0E6FF',
            'subcortical': '#FFE6F2'
        }
    
    def create_brain_pain_comparison(self):
        """Create brain pain state comparison"""
        
        fig = plt.figure(figsize=(20, 14))
        
        # Main comparison brain
        ax_main = plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=2)
        
        # Pain state only
        ax_pain = plt.subplot2grid((3, 3), (0, 2), rowspan=1, colspan=1)
        
        # No-pain state only
        ax_no_pain = plt.subplot2grid((3, 3), (1, 2), rowspan=1, colspan=1)
        
        # Activation comparison
        ax_comparison = plt.subplot2grid((3, 3), (2, 0), rowspan=1, colspan=3)
        
        # Draw main comparison
        self.draw_brain_comparison(ax_main)
        
        # Draw individual states
        self.draw_single_state(ax_pain, 'pain_enhanced', 'Pain State', self.pain_color)
        self.draw_single_state(ax_no_pain, 'no_pain_active', 'No-Pain State', self.no_pain_color)
        
        # Draw comparison chart
        self.draw_activation_chart(ax_comparison)
        
        # Main title
        fig.suptitle('BrainGNN Brain Shape Pain State Mapping\\n'
                    'Binary Classification: Pain vs No-Pain (98.7% Accuracy)\\n'
                    f'Analysis of {len(self.pain_regions["pain_enhanced"]) + len(self.pain_regions["no_pain_active"])} Key Brain Regions', 
                    fontsize=16, fontweight='bold', y=0.95)
        
        plt.tight_layout()
        
        # Save figures
        plt.savefig('./figures/brain_shape_pain_mapping.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.savefig('./figures/brain_shape_pain_mapping.pdf', 
                   bbox_inches='tight', facecolor='white')
        
        print("Brain shape pain mapping saved:")
        print("  • ./figures/brain_shape_pain_mapping.png")
        print("  • ./figures/brain_shape_pain_mapping.pdf")
        
        return fig
    
    def draw_brain_comparison(self, ax):
        """Draw brain comparison with both states"""
        
        # Draw brain anatomy
        self.draw_brain_anatomy(ax)
        
        # Draw pain-enhanced regions (red)
        for region_name, region_info in self.pain_regions['pain_enhanced'].items():
            pos = region_info['pos']
            size = region_info['size']
            activation = region_info['activation']
            
            color_intensity = 0.4 + 0.6 * abs(activation)
            color = plt.cm.Reds(color_intensity)
            
            circle = Circle(pos, size, color=color, alpha=0.9, 
                          edgecolor='darkred', linewidth=2, zorder=10)
            ax.add_patch(circle)
            
            # Add activation value
            ax.text(pos[0], pos[1], f'+{activation:.2f}', 
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   color='white', zorder=11)
            
            # Add label
            label = region_name.split('_')[0]
            ax.annotate(label, pos, xytext=(0, size + 6), 
                       textcoords='offset points',
                       ha='center', va='bottom', fontsize=7, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='red', 
                               alpha=0.7, edgecolor='white'), zorder=12)
        
        # Draw no-pain active regions (blue)
        for region_name, region_info in self.pain_regions['no_pain_active'].items():
            pos = region_info['pos']
            size = region_info['size']
            activation = region_info['activation']
            
            color_intensity = 0.4 + 0.6 * abs(activation)
            color = plt.cm.Blues(color_intensity)
            
            circle = Circle(pos, size, color=color, alpha=0.9, 
                          edgecolor='darkblue', linewidth=2, zorder=10)
            ax.add_patch(circle)
            
            # Add activation value
            ax.text(pos[0], pos[1], f'{activation:.2f}', 
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   color='white', zorder=11)
            
            # Add label
            label = region_name.split('_')[0]
            ax.annotate(label, pos, xytext=(0, size + 6), 
                       textcoords='offset points',
                       ha='center', va='bottom', fontsize=7, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='blue', 
                               alpha=0.7, edgecolor='white'), zorder=12)
        
        ax.set_xlim(-100, 100)
        ax.set_ylim(-110, 110)
        ax.set_aspect('equal')
        ax.set_title('Pain vs No-Pain Brain States\\nRed=Pain Active, Blue=No-Pain Active', 
                    fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # Add orientation labels
        ax.text(-90, 95, 'L', fontsize=16, fontweight='bold', 
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightblue', alpha=0.8))
        ax.text(85, 95, 'R', fontsize=16, fontweight='bold',
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightcoral', alpha=0.8))
        
        # Add legend
        pain_patch = mpatches.Patch(color=self.pain_color, label='Pain State (Enhanced)')
        no_pain_patch = mpatches.Patch(color=self.no_pain_color, label='No-Pain State (Active)')
        ax.legend(handles=[pain_patch, no_pain_patch], loc='upper right', fontsize=10)
    
    def draw_brain_anatomy(self, ax):
        """Draw brain anatomical structure"""
        
        # Draw cerebral cortex
        cortex_polygon = Polygon(self.brain_outline['cortex'], 
                               fill=True, facecolor='lightgray', 
                               edgecolor='black', linewidth=2, alpha=0.3, zorder=1)
        ax.add_patch(cortex_polygon)
        
        # Draw cerebellum
        cerebellum_polygon = Polygon(self.brain_outline['cerebellum'], 
                                   fill=True, facecolor='lightsteelblue', 
                                   edgecolor='black', linewidth=1.5, alpha=0.4, zorder=2)
        ax.add_patch(cerebellum_polygon)
        
        # Draw brainstem
        brainstem_polygon = Polygon(self.brain_outline['brainstem'], 
                                  fill=True, facecolor='lightyellow', 
                                  edgecolor='black', linewidth=1.5, alpha=0.5, zorder=3)
        ax.add_patch(brainstem_polygon)
        
        # Add anatomical labels
        ax.text(0, 50, 'Cerebral Cortex', ha='center', va='center', 
               fontsize=12, fontweight='bold', alpha=0.6, zorder=4)
        ax.text(0, -75, 'Cerebellum', ha='center', va='center', 
               fontsize=10, fontweight='bold', alpha=0.7, zorder=4)
        ax.text(0, -45, 'Brainstem', ha='center', va='center', 
               fontsize=8, fontweight='bold', alpha=0.7, zorder=4)
    
    def draw_single_state(self, ax, state_key, title, color):
        """Draw single brain state"""
        
        # Simplified brain outline
        brain_circle = Circle((0, 0), 45, fill=True, facecolor='lightgray', 
                            edgecolor='black', linewidth=2, alpha=0.3)
        ax.add_patch(brain_circle)
        
        # Cerebellum
        cerebellum_circle = Circle((0, -35), 25, fill=True, facecolor='lightsteelblue', 
                                 edgecolor='black', linewidth=1, alpha=0.4)
        ax.add_patch(cerebellum_circle)
        
        # Draw regions for this state
        for region_name, region_info in self.pain_regions[state_key].items():
            # Scale position and size for smaller plot
            pos = (region_info['pos'][0] * 0.5, region_info['pos'][1] * 0.5)
            size = region_info['size'] * 0.6
            activation = region_info['activation']
            
            # Choose color based on state
            if state_key == 'pain_enhanced':
                color_intensity = 0.5 + 0.5 * abs(activation)
                region_color = plt.cm.Reds(color_intensity)
            else:
                color_intensity = 0.5 + 0.5 * abs(activation)
                region_color = plt.cm.Blues(color_intensity)
            
            circle = Circle(pos, size, color=region_color, alpha=0.8, 
                          edgecolor='white', linewidth=1)
            ax.add_patch(circle)
            
            # Add values for strongest regions
            if abs(activation) > 0.4:
                ax.text(pos[0], pos[1], f'{activation:+.1f}', 
                       ha='center', va='center', fontsize=6, fontweight='bold',
                       color='white')
        
        ax.set_xlim(-60, 60)
        ax.set_ylim(-70, 60)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=11, fontweight='bold', color=color)
        ax.axis('off')
    
    def draw_activation_chart(self, ax):
        """Draw activation comparison chart"""
        
        # Prepare data
        regions = []
        activations = []
        colors = []
        
        # Pain enhanced regions
        for region_name, region_info in self.pain_regions['pain_enhanced'].items():
            regions.append(region_name.replace('_', ' ')[:15])
            activations.append(region_info['activation'])
            colors.append(self.pain_color)
        
        # No-pain active regions
        for region_name, region_info in self.pain_regions['no_pain_active'].items():
            regions.append(region_name.replace('_', ' ')[:15])
            activations.append(region_info['activation'])
            colors.append(self.no_pain_color)
        
        # Sort by activation strength
        sorted_data = sorted(zip(regions, activations, colors), 
                           key=lambda x: abs(x[1]), reverse=True)
        
        regions_sorted = [x[0] for x in sorted_data]
        activations_sorted = [x[1] for x in sorted_data]
        colors_sorted = [x[2] for x in sorted_data]
        
        # Create horizontal bar chart
        y_pos = np.arange(len(regions_sorted))
        bars = ax.barh(y_pos, activations_sorted, color=colors_sorted, alpha=0.8, 
                      edgecolor='black', linewidth=1)
        
        # Add value labels
        for i, (bar, activation) in enumerate(zip(bars, activations_sorted)):
            width = bar.get_width()
            ax.text(width + (0.02 if width > 0 else -0.02), 
                   bar.get_y() + bar.get_height()/2, 
                   f'{activation:+.3f}', 
                   ha='left' if width > 0 else 'right', 
                   va='center', fontsize=9, fontweight='bold')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(regions_sorted, fontsize=9)
        ax.set_xlabel('Activation Difference (Pain - No Pain)', fontsize=11, fontweight='bold')
        ax.set_title('Brain Region Activation in Pain vs No-Pain States', fontsize=12, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.7, linewidth=2)
        ax.grid(axis='x', alpha=0.3)
        
        # Add summary statistics
        pain_count = len(self.pain_regions['pain_enhanced'])
        no_pain_count = len(self.pain_regions['no_pain_active'])
        pain_avg = np.mean([r['activation'] for r in self.pain_regions['pain_enhanced'].values()])
        no_pain_avg = np.mean([abs(r['activation']) for r in self.pain_regions['no_pain_active'].values()])
        
        summary_text = f"""PAIN STATE: {pain_count} regions (avg: +{pain_avg:.3f})
NO-PAIN STATE: {no_pain_count} regions (avg: -{no_pain_avg:.3f})
TOTAL REGIONS: {pain_count + no_pain_count}
MODEL ACCURACY: 98.7%"""
        
        ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
               fontsize=10, verticalalignment='top', fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.9))

def main():
    """Main function"""
    print("Creating brain shape pain state mapping...")
    print("BrainGNN Binary Classification: Pain vs No-Pain (98.7% Accuracy)")
    
    # Create brain shape mapper
    mapper = BrainShapePainMapper()
    
    # Generate brain mapping
    fig = mapper.create_brain_pain_comparison()
    
    print("\\nBrain shape pain mapping completed!")
    print("Analysis Summary:")
    print(f"  • Pain State Regions: {len(mapper.pain_regions['pain_enhanced'])} (Enhanced during pain)")
    print(f"  • No-Pain State Regions: {len(mapper.pain_regions['no_pain_active'])} (Active when no pain)")
    print(f"  • Total Key Regions: {len(mapper.pain_regions['pain_enhanced']) + len(mapper.pain_regions['no_pain_active'])}")
    print("  • Classification Type: Binary (Pain vs No-Pain)")
    print("  • Model Accuracy: 98.7%")

if __name__ == "__main__":
    main()