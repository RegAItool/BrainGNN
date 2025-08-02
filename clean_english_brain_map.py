#!/usr/bin/env python3
"""
Clean English Brain Mapping - No Chinese Characters
Professional brain visualization without font issues
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

class CleanEnglishBrainMapper:
    """Clean English Brain Mapper"""
    
    def __init__(self):
        self.setup_brain_data()
        self.setup_color_schemes()
    
    def setup_brain_data(self):
        """Setup brain region data in English"""
        
        # Key brain regions from analysis results
        self.pain_regions = {
            # === Cerebellum Network (Strongest Enhancement) ===
            'Cerebelum_Crus1_R': {
                'pos': (60, -75), 'size': 25, 'activation': 0.601,
                'network': 'Cerebellum', 'importance': 0.022,
                'description': 'Primary sensorimotor integration'
            },
            'Cerebelum_Crus1_L': {
                'pos': (-60, -75), 'size': 20, 'activation': 0.438,
                'network': 'Cerebellum', 'importance': 0.016,
                'description': 'Bilateral cerebellar coordination'
            },
            'Cerebelum_Crus2_R': {
                'pos': (50, -65), 'size': 15, 'activation': 0.391,
                'network': 'Cerebellum', 'importance': 0.014,
                'description': 'Motor control regulation'
            },
            
            # === Visual-Spatial Network ===
            'Occipital_Mid_R': {
                'pos': (45, -90), 'size': 22, 'activation': 0.528,
                'network': 'Visual', 'importance': 0.022,
                'description': 'Spatial pain localization'
            },
            'Occipital_Sup_R': {
                'pos': (25, -95), 'size': 20, 'activation': 0.528,
                'network': 'Visual', 'importance': 0.022,
                'description': 'Visual attention enhancement'
            },
            'Occipital_Mid_L': {
                'pos': (-45, -90), 'size': 18, 'activation': 0.385,
                'network': 'Visual', 'importance': 0.016,
                'description': 'Bilateral visual processing'
            },
            
            # === Cognitive Control Network (Suppression) ===
            'Frontal_Sup_L': {
                'pos': (-35, 70), 'size': 20, 'activation': -0.512,
                'network': 'Frontal', 'importance': 0.015,
                'description': 'Top-down inhibitory control'
            },
            'Frontal_Mid_L': {
                'pos': (-50, 45), 'size': 18, 'activation': -0.498,
                'network': 'Frontal', 'importance': 0.014,
                'description': 'Executive function regulation'
            },
            'Frontal_Sup_R': {
                'pos': (35, 70), 'size': 16, 'activation': -0.394,
                'network': 'Frontal', 'importance': 0.011,
                'description': 'Bilateral cognitive control'
            },
            
            # === Sensorimotor Regulation Network ===
            'Precentral_L': {
                'pos': (-40, 25), 'size': 18, 'activation': -0.433,
                'network': 'Sensorimotor', 'importance': 0.013,
                'description': 'Motor cortex suppression'
            },
            'Postcentral_L': {
                'pos': (-40, -20), 'size': 17, 'activation': -0.431,
                'network': 'Sensorimotor', 'importance': 0.012,
                'description': 'Sensory cortex regulation'
            },
            'Rolandic_Oper_L': {
                'pos': (-55, 5), 'size': 16, 'activation': -0.401,
                'network': 'Sensorimotor', 'importance': 0.019,
                'description': 'Sensorimotor integration'
            },
            
            # === Limbic Emotional Network ===
            'Amygdala_R': {
                'pos': (25, -10), 'size': 14, 'activation': 0.080,
                'network': 'Limbic', 'importance': 0.015,
                'description': 'Pain emotional response'
            },
            'Cingulum_Ant_R': {
                'pos': (12, 40), 'size': 13, 'activation': 0.065,
                'network': 'Limbic', 'importance': 0.013,
                'description': 'Emotion-cognition integration'
            },
            'ParaHippocampal_L': {
                'pos': (-30, -35), 'size': 15, 'activation': 0.120,
                'network': 'Limbic', 'importance': 0.019,
                'description': 'Pain memory encoding'
            },
            
            # === Subcortical Modulation Network ===
            'Thalamus_L': {
                'pos': (-15, -15), 'size': 12, 'activation': 0.055,
                'network': 'Subcortical', 'importance': 0.011,
                'description': 'Pain signal relay'
            },
            'Putamen_R': {
                'pos': (25, 5), 'size': 11, 'activation': -0.386,
                'network': 'Subcortical', 'importance': 0.009,
                'description': 'Motor regulation suppression'
            }
        }
        
        # Network definitions
        self.networks = {
            'Cerebellum': {
                'color': '#FF4444',
                'description': 'Sensorimotor integration core'
            },
            'Visual': {
                'color': '#FF8844',
                'description': 'Spatial attention and localization'
            },
            'Frontal': {
                'color': '#4444FF',
                'description': 'Cognitive control and inhibition'
            },
            'Sensorimotor': {
                'color': '#6666FF',
                'description': 'Bidirectional sensorimotor regulation'
            },
            'Limbic': {
                'color': '#AA44AA',
                'description': 'Emotional processing and memory'
            },
            'Subcortical': {
                'color': '#44AA44',
                'description': 'Subcortical pain modulation'
            }
        }
    
    def setup_color_schemes(self):
        """Setup color schemes"""
        
        # Activation colormap
        self.activation_cmap = LinearSegmentedColormap.from_list(
            'pain_activation',
            ['#0066CC', '#FFFFFF', '#CC0000'],  # Blue-White-Red
            N=256
        )
    
    def create_clean_english_brain_map(self):
        """Create clean English brain map"""
        
        # Create figure
        fig = plt.figure(figsize=(20, 14))
        
        # Main brain map
        ax_main = plt.subplot2grid((4, 6), (0, 0), rowspan=3, colspan=4)
        
        # Network distribution
        ax_network = plt.subplot2grid((4, 6), (0, 4), rowspan=2, colspan=2)
        
        # Activation ranking
        ax_activation = plt.subplot2grid((4, 6), (2, 4), rowspan=2, colspan=2)
        
        # Summary statistics
        ax_summary = plt.subplot2grid((4, 6), (3, 0), rowspan=1, colspan=4)
        
        # === Draw main brain map ===
        self.draw_clean_brain(ax_main)
        
        # === Draw network distribution ===
        self.draw_network_distribution(ax_network)
        
        # === Draw activation ranking ===
        self.draw_activation_ranking(ax_activation)
        
        # === Draw summary ===
        self.draw_summary_statistics(ax_summary)
        
        # Set main title
        fig.suptitle('BrainGNN Pain Region Mapping: 98.7% Accuracy\n'
                    'Enhanced vs Suppressed Brain Activation in Pain Processing\n'
                    f'Analysis of {len(self.pain_regions)} Key Brain Regions', 
                    fontsize=16, fontweight='bold', y=0.96)
        
        plt.tight_layout()
        
        # Save figures
        plt.savefig('./figures/clean_english_brain_map.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.savefig('./figures/clean_english_brain_map.pdf', 
                   bbox_inches='tight', facecolor='white')
        
        print("✅ Clean English brain map saved:")
        print("  • ./figures/clean_english_brain_map.png")
        print("  • ./figures/clean_english_brain_map.pdf")
        
        return fig
    
    def draw_clean_brain(self, ax):
        """Draw clean brain outline and regions"""
        
        # Draw brain outline
        self.draw_brain_outline(ax)
        
        # Sort regions by activation strength
        sorted_regions = sorted(self.pain_regions.items(), 
                              key=lambda x: abs(x[1]['activation']), reverse=True)
        
        for region_name, region_info in sorted_regions:
            pos = region_info['pos']
            size = region_info['size']
            activation = region_info['activation']
            network = region_info['network']
            importance = region_info['importance']
            
            # Choose color based on network
            base_color = self.networks[network]['color']
            
            # Adjust color intensity based on activation
            if activation > 0:
                # Enhanced activation - warmer colors
                color_intensity = 0.4 + 0.6 * abs(activation)
                color = plt.cm.Reds(color_intensity)
            else:
                # Suppressed activation - cooler colors
                color_intensity = 0.4 + 0.6 * abs(activation)
                color = plt.cm.Blues(color_intensity)
            
            # Draw region circle
            circle = Circle(pos, size, color=color, alpha=0.8, 
                          edgecolor='white', linewidth=2)
            ax.add_patch(circle)
            
            # Add importance ring for key regions
            if importance > 0.015:
                importance_ring = Circle(pos, size + 3, fill=False,
                                       edgecolor='gold', linewidth=3, alpha=0.9)
                ax.add_patch(importance_ring)
            
            # Add activation value
            ax.text(pos[0], pos[1], f'{activation:+.2f}', 
                   ha='center', va='center', fontsize=9, fontweight='bold',
                   color='white' if abs(activation) > 0.3 else 'black')
            
            # Add region label
            label = region_name.split('_')[0]
            if len(region_name.split('_')) > 1:
                label += f"_{region_name.split('_')[-1]}"
            
            ax.annotate(label, pos, xytext=(0, size + 8), 
                       textcoords='offset points',
                       ha='center', va='bottom', fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
        
        ax.set_xlim(-80, 80)
        ax.set_ylim(-110, 90)
        ax.set_aspect('equal')
        ax.set_title('Brain Pain Region Mapping\n'
                    '(Circle size = Importance, Color = Activation strength, Gold ring = Key regions)', 
                    fontsize=12, fontweight='bold')
        ax.axis('off')
    
    def draw_brain_outline(self, ax):
        """Draw brain outline"""
        
        # Main brain outline
        brain_outline = Ellipse((0, -10), 150, 170, 
                              fill=False, color='darkgray', linewidth=2, alpha=0.6)
        ax.add_patch(brain_outline)
        
        # Cerebellum outline
        cerebellum = Circle((0, -75), 55, fill=False, color='gray', linewidth=2, alpha=0.4)
        ax.add_patch(cerebellum)
        
        # Brainstem
        brainstem = Ellipse((0, -45), 20, 50, fill=False, color='gray', linewidth=2, alpha=0.4)
        ax.add_patch(brainstem)
        
        # Add direction labels
        ax.text(-75, 75, 'L', fontsize=18, fontweight='bold', alpha=0.7,
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightblue', alpha=0.6))
        ax.text(70, 75, 'R', fontsize=18, fontweight='bold', alpha=0.7,
               bbox=dict(boxstyle="circle,pad=0.3", facecolor='lightcoral', alpha=0.6))
        
        ax.text(-70, -100, 'Anterior', fontsize=12, alpha=0.6)
        ax.text(50, -100, 'Posterior', fontsize=12, alpha=0.6)
    
    def draw_network_distribution(self, ax):
        """Draw network distribution"""
        
        # Count regions per network
        network_counts = {}
        for region_info in self.pain_regions.values():
            network = region_info['network']
            network_counts[network] = network_counts.get(network, 0) + 1
        
        # Create pie chart
        sizes = list(network_counts.values())
        labels = list(network_counts.keys())
        colors = [self.networks[net]['color'] for net in labels]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=90)
        
        ax.set_title('Network Distribution\n(by number of regions)', 
                    fontsize=12, fontweight='bold')
        
        # Add legend with descriptions
        legend_text = "Network Functions:\n"
        for network, info in self.networks.items():
            if network in network_counts:
                legend_text += f"• {network}: {info['description']}\n"
        
        ax.text(1.3, 0.5, legend_text, transform=ax.transAxes, fontsize=9,
               verticalalignment='center', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
    
    def draw_activation_ranking(self, ax):
        """Draw activation ranking"""
        
        # Prepare data
        regions = []
        activations = []
        networks = []
        importances = []
        
        for region_name, region_info in self.pain_regions.items():
            regions.append(region_name.replace('_', ' ')[:18])
            activations.append(region_info['activation'])
            networks.append(region_info['network'])
            importances.append(region_info['importance'])
        
        # Sort by activation strength
        sorted_data = sorted(zip(regions, activations, networks, importances), 
                           key=lambda x: abs(x[1]), reverse=True)
        
        regions_sorted = [x[0] for x in sorted_data]
        activations_sorted = [x[1] for x in sorted_data]
        networks_sorted = [x[2] for x in sorted_data]
        importances_sorted = [x[3] for x in sorted_data]
        
        # Choose colors based on network
        colors = [self.networks[net]['color'] for net in networks_sorted]
        
        # Create horizontal bar chart
        y_pos = np.arange(len(regions_sorted))
        bars = ax.barh(y_pos, activations_sorted, color=colors, alpha=0.8)
        
        # Highlight important regions
        for bar, importance in zip(bars, importances_sorted):
            bar.set_edgecolor('gold' if importance > 0.015 else 'black')
            bar.set_linewidth(3 if importance > 0.015 else 1)
        
        # Add value labels
        for i, (bar, activation, importance) in enumerate(zip(bars, activations_sorted, importances_sorted)):
            width = bar.get_width()
            label = f'{activation:+.3f}'
            if importance > 0.015:
                label += ' ★'
            ax.text(width + (0.02 if width > 0 else -0.02), 
                   bar.get_y() + bar.get_height()/2, 
                   label, ha='left' if width > 0 else 'right', 
                   va='center', fontsize=8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(regions_sorted, fontsize=9)
        ax.set_xlabel('Activation Difference (Pain - No Pain)', fontsize=11)
        ax.set_title('Brain Region Activation Ranking\n(★ = High importance regions)', 
                    fontsize=12, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax.grid(axis='x', alpha=0.3)
    
    def draw_summary_statistics(self, ax):
        """Draw summary statistics"""
        
        # Calculate statistics
        total_regions = len(self.pain_regions)
        enhanced_count = sum(1 for r in self.pain_regions.values() if r['activation'] > 0)
        suppressed_count = sum(1 for r in self.pain_regions.values() if r['activation'] < 0)
        
        enhanced_regions = [r for r in self.pain_regions.values() if r['activation'] > 0]
        suppressed_regions = [r for r in self.pain_regions.values() if r['activation'] < 0]
        
        avg_enhanced = np.mean([r['activation'] for r in enhanced_regions]) if enhanced_regions else 0
        avg_suppressed = np.mean([abs(r['activation']) for r in suppressed_regions]) if suppressed_regions else 0
        
        strongest_enhanced = max(enhanced_regions, key=lambda x: x['activation']) if enhanced_regions else None
        strongest_suppressed = min(self.pain_regions.values(), key=lambda x: x['activation'])
        
        # Create summary text
        summary_text = f"""
MODEL PERFORMANCE: 98.7% Accuracy | F1-Score: 98.1% | Target: 80%+ ✓

BRAIN NETWORK ANALYSIS:
• Total Key Regions: {total_regions}
• Enhanced Activation: {enhanced_count} regions (avg: +{avg_enhanced:.3f})
• Suppressed Activation: {suppressed_count} regions (avg: -{avg_suppressed:.3f})
• Pain Processing Networks: {len(self.networks)}

KEY FINDINGS:
• Strongest Enhancement: {list(self.pain_regions.keys())[list(self.pain_regions.values()).index(strongest_enhanced)]} (+{strongest_enhanced['activation']:.3f})
• Strongest Suppression: {list(self.pain_regions.keys())[list(self.pain_regions.values()).index(strongest_suppressed)]} ({strongest_suppressed['activation']:.3f})
• Primary Network: Cerebellum sensorimotor integration
• Control Mechanism: Frontal cognitive inhibition

CLINICAL IMPLICATIONS:
• Multi-layer neural networks process pain signals
• Different pain types activate specific brain region combinations  
• Deep-surface brain coordination is key to pain perception
• Provides neural network targets for personalized pain treatment
        """
        
        ax.text(0.02, 0.98, summary_text.strip(), transform=ax.transAxes, 
               fontsize=10, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan", alpha=0.8))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

def main():
    """Main function"""
    print("🎨 Creating clean English brain mapping...")
    print("🧠 Generating professional visualization without font issues...")
    
    # Create clean mapper
    mapper = CleanEnglishBrainMapper()
    
    # Generate clean brain map
    fig = mapper.create_clean_english_brain_map()
    
    print("\n✨ Clean English brain map completed!")
    print("📂 Generated files:")
    print("  • clean_english_brain_map.png")
    print("  • clean_english_brain_map.pdf")

if __name__ == "__main__":
    main()