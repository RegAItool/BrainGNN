#!/usr/bin/env python3
"""
脑区重要性分析和疼痛-脑区映射
分析不同疼痛状态下的重要脑区，生成可视化结果
"""

import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from torch_geometric.loader import DataLoader
import warnings
warnings.filterwarnings('ignore')

from imports.PainGraphDataset import PainGraphDataset
from net.multitask_braingnn import MultiTaskBrainGNN

# AAL116 脑区名称映射
AAL_REGIONS = {
    1: "Precentral_L", 2: "Precentral_R", 3: "Frontal_Sup_L", 4: "Frontal_Sup_R",
    5: "Frontal_Sup_Orb_L", 6: "Frontal_Sup_Orb_R", 7: "Frontal_Mid_L", 8: "Frontal_Mid_R",
    9: "Frontal_Mid_Orb_L", 10: "Frontal_Mid_Orb_R", 11: "Frontal_Inf_Oper_L", 12: "Frontal_Inf_Oper_R",
    13: "Frontal_Inf_Tri_L", 14: "Frontal_Inf_Tri_R", 15: "Frontal_Inf_Orb_L", 16: "Frontal_Inf_Orb_R",
    17: "Rolandic_Oper_L", 18: "Rolandic_Oper_R", 19: "Supp_Motor_Area_L", 20: "Supp_Motor_Area_R",
    21: "Olfactory_L", 22: "Olfactory_R", 23: "Frontal_Sup_Medial_L", 24: "Frontal_Sup_Medial_R",
    25: "Frontal_Med_Orb_L", 26: "Frontal_Med_Orb_R", 27: "Rectus_L", 28: "Rectus_R",
    29: "Insula_L", 30: "Insula_R", 31: "Cingulum_Ant_L", 32: "Cingulum_Ant_R",
    33: "Cingulum_Mid_L", 34: "Cingulum_Mid_R", 35: "Cingulum_Post_L", 36: "Cingulum_Post_R",
    37: "Hippocampus_L", 38: "Hippocampus_R", 39: "ParaHippocampal_L", 40: "ParaHippocampal_R",
    41: "Amygdala_L", 42: "Amygdala_R", 43: "Calcarine_L", 44: "Calcarine_R",
    45: "Cuneus_L", 46: "Cuneus_R", 47: "Lingual_L", 48: "Lingual_R",
    49: "Occipital_Sup_L", 50: "Occipital_Sup_R", 51: "Occipital_Mid_L", 52: "Occipital_Mid_R",
    53: "Occipital_Inf_L", 54: "Occipital_Inf_R", 55: "Fusiform_L", 56: "Fusiform_R",
    57: "Postcentral_L", 58: "Postcentral_R", 59: "Parietal_Sup_L", 60: "Parietal_Sup_R",
    61: "Parietal_Inf_L", 62: "Parietal_Inf_R", 63: "SupraMarginal_L", 64: "SupraMarginal_R",
    65: "Angular_L", 66: "Angular_R", 67: "Precuneus_L", 68: "Precuneus_R",
    69: "Paracentral_Lobule_L", 70: "Paracentral_Lobule_R", 71: "Caudate_L", 72: "Caudate_R",
    73: "Putamen_L", 74: "Putamen_R", 75: "Pallidum_L", 76: "Pallidum_R",
    77: "Thalamus_L", 78: "Thalamus_R", 79: "Heschl_L", 80: "Heschl_R",
    81: "Temporal_Sup_L", 82: "Temporal_Sup_R", 83: "Temporal_Pole_Sup_L", 84: "Temporal_Pole_Sup_R",
    85: "Temporal_Mid_L", 86: "Temporal_Mid_R", 87: "Temporal_Pole_Mid_L", 88: "Temporal_Pole_Mid_R",
    89: "Temporal_Inf_L", 90: "Temporal_Inf_R", 91: "Cerebelum_Crus1_L", 92: "Cerebelum_Crus1_R",
    93: "Cerebelum_Crus2_L", 94: "Cerebelum_Crus2_R", 95: "Cerebelum_3_L", 96: "Cerebelum_3_R",
    97: "Cerebelum_4_5_L", 98: "Cerebelum_4_5_R", 99: "Cerebelum_6_L", 100: "Cerebelum_6_R",
    101: "Cerebelum_7b_L", 102: "Cerebelum_7b_R", 103: "Cerebelum_8_L", 104: "Cerebelum_8_R",
    105: "Cerebelum_9_L", 106: "Cerebelum_9_R", 107: "Cerebelum_10_L", 108: "Cerebelum_10_R",
    109: "Vermis_1_2", 110: "Vermis_3", 111: "Vermis_4_5", 112: "Vermis_6",
    113: "Vermis_7", 114: "Vermis_8", 115: "Vermis_9", 116: "Vermis_10"
}

class BrainRegionAnalyzer:
    """脑区重要性分析器"""
    
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.dataset = None
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """加载训练好的模型"""
        self.model = MultiTaskBrainGNN(in_dim=1, n_roi=116).to(self.device)
        try:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            print(f"✅ 模型加载成功: {model_path}")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            # 尝试加载优化后的模型
            try:
                from intelligent_optimization import ImprovedBrainGNN
                self.model = ImprovedBrainGNN(in_dim=1, n_roi=116).to(self.device)
                self.model.load_state_dict(torch.load('./model/optimized_brain_model.pth', map_location=self.device))
                self.model.eval()
                print("✅ 优化模型加载成功")
            except:
                print("❌ 无法加载任何模型，将使用随机初始化模型")
    
    def load_data(self, data_path='./data/pain_data/all_graphs/'):
        """加载数据集"""
        self.dataset = PainGraphDataset(data_path)
        
        # 过滤有效数据
        self.valid_data = []
        for i in range(len(self.dataset)):
            try:
                data = self.dataset[i]
                if data.x.shape == (116, 1):
                    self.valid_data.append(data)
            except:
                continue
        
        print(f"✅ 加载数据: {len(self.valid_data)} 个有效样本")
    
    def extract_features_and_labels(self):
        """提取特征和标签"""
        features = []
        labels = []
        
        print("🔍 提取脑网络特征...")
        for data in self.valid_data[:1000]:  # 限制样本数量以加快分析
            try:
                # 使用原始脑区活动作为特征
                feature_vector = data.x.flatten().detach().numpy()
                
                features.append(feature_vector)
                labels.append(int(data.y.item()))
            except Exception as e:
                print(f"处理数据时出错: {e}")
                continue
        
        return np.array(features), np.array(labels)
    
    def analyze_region_importance_rf(self):
        """使用随机森林分析脑区重要性"""
        features, labels = self.extract_features_and_labels()
        
        if len(features) == 0:
            print("❌ 没有有效特征数据")
            return None
        
        print("🧠 训练随机森林进行脑区重要性分析...")
        
        # 训练随机森林
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(features[:, :116], labels)  # 只使用前116个特征（脑区活动）
        
        # 获取特征重要性
        importance_scores = rf.feature_importances_
        
        # 排序获取最重要的脑区
        sorted_indices = np.argsort(importance_scores)[::-1]
        
        results = []
        for i, idx in enumerate(sorted_indices[:20]):  # 取前20个重要脑区
            region_name = AAL_REGIONS.get(idx + 1, f"Region_{idx + 1}")
            results.append({
                'rank': i + 1,
                'region_id': idx + 1,
                'region_name': region_name,
                'importance_score': float(importance_scores[idx]),
                'hemisphere': 'Left' if 'L' in region_name else 'Right' if 'R' in region_name else 'Bilateral'
            })
        
        return results
    
    def analyze_pain_vs_nopain_activation(self):
        """分析疼痛vs非疼痛状态的脑区激活差异"""
        print("⚡ 分析疼痛状态脑区激活差异...")
        
        pain_activations = []
        nopain_activations = []
        
        for data in self.valid_data[:1000]:
            try:
                activation = data.x.flatten().detach().numpy()
                if int(data.y.item()) == 1:  # 疼痛状态
                    pain_activations.append(activation)
                else:  # 非疼痛状态
                    nopain_activations.append(activation)
            except Exception as e:
                continue
        
        if len(pain_activations) == 0 or len(nopain_activations) == 0:
            print("❌ 数据不足以进行对比分析")
            return None
        
        pain_mean = np.mean(pain_activations, axis=0)
        nopain_mean = np.mean(nopain_activations, axis=0)
        
        # 计算激活差异
        activation_diff = pain_mean - nopain_mean
        
        # 获取差异最大的脑区
        sorted_indices = np.argsort(np.abs(activation_diff))[::-1]
        
        results = []
        for i, idx in enumerate(sorted_indices[:20]):
            region_name = AAL_REGIONS.get(idx + 1, f"Region_{idx + 1}")
            results.append({
                'rank': i + 1,
                'region_id': idx + 1,
                'region_name': region_name,
                'activation_diff': float(activation_diff[idx]),
                'pain_activation': float(pain_mean[idx]),
                'nopain_activation': float(nopain_mean[idx]),
                'effect_type': 'Increased' if activation_diff[idx] > 0 else 'Decreased'
            })
        
        return results
    
    def visualize_brain_regions(self, importance_results, diff_results):
        """可视化脑区分析结果"""
        print("🎨 生成可视化图表...")
        
        # 设置图表样式
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('🧠 Brain Region Analysis for Pain Perception', fontsize=20, fontweight='bold')
        
        # 1. 脑区重要性排名
        if importance_results:
            ax1 = axes[0, 0]
            regions = [r['region_name'].replace('_', ' ') for r in importance_results[:10]]
            scores = [r['importance_score'] for r in importance_results[:10]]
            
            bars = ax1.barh(regions, scores, color='steelblue', alpha=0.8)
            ax1.set_xlabel('Importance Score', fontsize=12)
            ax1.set_title('Top 10 Important Brain Regions', fontsize=14, fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
            
            # 添加数值标签
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax1.text(width + 0.001, bar.get_y() + bar.get_height()/2, 
                        f'{scores[i]:.3f}', ha='left', va='center')
        
        # 2. 半球分布
        if importance_results:
            ax2 = axes[0, 1]
            hemisphere_counts = {'Left': 0, 'Right': 0, 'Bilateral': 0}
            for r in importance_results[:20]:
                hemisphere_counts[r['hemisphere']] += 1
            
            colors = ['lightcoral', 'lightblue', 'lightgreen']
            wedges, texts, autotexts = ax2.pie(hemisphere_counts.values(), 
                                             labels=hemisphere_counts.keys(),
                                             colors=colors, autopct='%1.1f%%',
                                             startangle=90)
            ax2.set_title('Hemisphere Distribution of Important Regions', fontsize=14, fontweight='bold')
        
        # 3. 疼痛激活差异
        if diff_results:
            ax3 = axes[1, 0]
            regions = [r['region_name'].replace('_', ' ') for r in diff_results[:10]]
            diffs = [r['activation_diff'] for r in diff_results[:10]]
            
            colors = ['red' if d > 0 else 'blue' for d in diffs]
            bars = ax3.barh(regions, diffs, color=colors, alpha=0.7)
            ax3.set_xlabel('Activation Difference (Pain - No Pain)', fontsize=12)
            ax3.set_title('Brain Activation Changes in Pain State', fontsize=14, fontweight='bold')
            ax3.axvline(x=0, color='black', linestyle='--', alpha=0.5)
            ax3.grid(axis='x', alpha=0.3)
        
        # 4. 激活水平对比
        if diff_results:
            ax4 = axes[1, 1]
            regions = [r['region_name'].replace('_', ' ') for r in diff_results[:8]]
            pain_vals = [r['pain_activation'] for r in diff_results[:8]]
            nopain_vals = [r['nopain_activation'] for r in diff_results[:8]]
            
            x = np.arange(len(regions))
            width = 0.35
            
            ax4.bar(x - width/2, pain_vals, width, label='Pain State', 
                   color='red', alpha=0.7)
            ax4.bar(x + width/2, nopain_vals, width, label='No Pain State', 
                   color='blue', alpha=0.7)
            
            ax4.set_xlabel('Brain Regions', fontsize=12)
            ax4.set_ylabel('Activation Level', fontsize=12)
            ax4.set_title('Pain vs No-Pain Activation Comparison', fontsize=14, fontweight='bold')
            ax4.set_xticks(x)
            ax4.set_xticklabels(regions, rotation=45, ha='right')
            ax4.legend()
            ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('./figures/brain_region_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ 保存可视化结果: ./figures/brain_region_analysis.png")
        
        return fig
    
    def generate_pain_brain_mapping_report(self, importance_results, diff_results):
        """生成疼痛-脑区映射报告"""
        print("📊 生成疼痛-脑区映射报告...")
        
        report = {
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'summary': {
                'total_regions_analyzed': 116,
                'top_important_regions': len(importance_results) if importance_results else 0,
                'differential_activation_regions': len(diff_results) if diff_results else 0
            },
            'key_findings': [],
            'important_regions': importance_results if importance_results else [],
            'activation_differences': diff_results if diff_results else []
        }
        
        # 分析关键发现
        if importance_results:
            top_region = importance_results[0]
            report['key_findings'].append(
                f"最重要的疼痛相关脑区: {top_region['region_name']} (重要性分数: {top_region['importance_score']:.3f})"
            )
        
        if diff_results:
            max_increase = max(diff_results, key=lambda x: x['activation_diff'] if x['activation_diff'] > 0 else -1)
            max_decrease = min(diff_results, key=lambda x: x['activation_diff'] if x['activation_diff'] < 0 else 1)
            
            if max_increase['activation_diff'] > 0:
                report['key_findings'].append(
                    f"疼痛状态下激活最强的脑区: {max_increase['region_name']} (增加 {max_increase['activation_diff']:.3f})"
                )
            
            if max_decrease['activation_diff'] < 0:
                report['key_findings'].append(
                    f"疼痛状态下抑制最强的脑区: {max_decrease['region_name']} (减少 {abs(max_decrease['activation_diff']):.3f})"
                )
        
        # 保存报告
        os.makedirs('./results', exist_ok=True)
        # 确保所有数值都是JSON可序列化的
        def convert_to_json_serializable(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_json_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_json_serializable(v) for v in obj]
            return obj
        
        report = convert_to_json_serializable(report)
        with open('./results/pain_brain_mapping_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 生成CSV格式的详细结果
        if importance_results:
            importance_df = pd.DataFrame(importance_results)
            importance_df.to_csv('./results/brain_region_importance.csv', index=False)
        
        if diff_results:
            diff_df = pd.DataFrame(diff_results)
            diff_df.to_csv('./results/pain_activation_differences.csv', index=False)
        
        print("✅ 报告保存完成:")
        print("  - ./results/pain_brain_mapping_report.json")
        print("  - ./results/brain_region_importance.csv")
        print("  - ./results/pain_activation_differences.csv")
        
        return report

def main():
    """主函数"""
    print("🧠 启动脑区重要性分析...")
    
    # 创建分析器
    analyzer = BrainRegionAnalyzer()
    
    # 尝试加载模型
    model_paths = [
        './model/optimized_brain_model.pth',
        './model/best_pain_model.pth',
        './model/best_pain_model_113.pth'
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            analyzer.load_model(path)
            break
    
    # 加载数据
    analyzer.load_data()
    
    # 进行分析
    importance_results = analyzer.analyze_region_importance_rf()
    diff_results = analyzer.analyze_pain_vs_nopain_activation()
    
    # 生成可视化
    if importance_results or diff_results:
        os.makedirs('./figures', exist_ok=True)
        analyzer.visualize_brain_regions(importance_results, diff_results)
        
        # 生成报告
        report = analyzer.generate_pain_brain_mapping_report(importance_results, diff_results)
        
        # 打印关键发现
        print("\n" + "="*60)
        print("🎯 关键发现:")
        for finding in report['key_findings']:
            print(f"  • {finding}")
        print("="*60)
        
        # 显示TOP疼痛相关脑区
        if importance_results:
            print("\n🏆 TOP 10 疼痛相关脑区:")
            for i, region in enumerate(importance_results[:10], 1):
                print(f"  {i:2d}. {region['region_name']:25s} (重要性: {region['importance_score']:.3f})")
    
    else:
        print("❌ 分析失败，请检查数据和模型")

if __name__ == "__main__":
    import os
    main()