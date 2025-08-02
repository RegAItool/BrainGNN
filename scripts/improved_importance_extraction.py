#!/usr/bin/env python3
"""
改进的ROI重要性分数提取
使用多种方法来计算更准确的ROI重要性分数
"""

import torch
import numpy as np
import os
import pickle
import argparse
from torch_geometric.data import DataLoader
from net.braingnn import Network
from imports.PainGraphDataset import PainGraphDataset
from imports.utils import train_val_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import glob
import shutil

def load_trained_model(model_path, args):
    """加载训练好的模型"""
    model = Network(args.indim, args.ratio, args.nclass)
    
    if os.path.exists(model_path):
        checkpoint = torch.load(model_path, map_location='cpu')
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        print(f"✅ 成功加载模型: {model_path}")
        return model
    else:
        print(f"❌ 模型文件不存在: {model_path}")
        return None

def extract_gradient_based_importance(model, dataloader, device='cpu'):
    """基于梯度的重要性分数提取"""
    print("🔍 提取基于梯度的重要性分数...")
    model.eval()
    gradient_importance = []
    
    for batch in dataloader:
        batch = batch.to(device)
        batch.x.requires_grad_(True)
        
        output, _, _, score1, score2 = model(batch.x, batch.edge_index, 
                                            batch.batch, batch.edge_attr, batch.pos)
        
        # 计算损失
        loss = torch.nn.functional.nll_loss(output, batch.y)
        loss.backward()
        
        # 计算输入特征的梯度
        grad_x = batch.x.grad
        if grad_x is not None:
            # 使用梯度的绝对值作为重要性
            importance = torch.abs(grad_x).mean(dim=0)
            gradient_importance.append(importance.detach().cpu().numpy())
        
        batch.x.requires_grad_(False)
    
    if gradient_importance:
        return np.mean(gradient_importance, axis=0)
    else:
        return None

def extract_attention_based_importance(model, dataloader, device='cpu'):
    """基于注意力权重的重要性分数提取"""
    print("🔍 提取基于注意力权重的重要性分数...")
    model.eval()
    all_attention_scores = []
    
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            
            # 前向传播获取pooling分数
            output, _, _, score1, score2 = model(batch.x, batch.edge_index, 
                                                batch.batch, batch.edge_attr, batch.pos)
            
            # 使用第一层的pooling分数作为注意力权重
            attention_scores = torch.sigmoid(score1).mean(dim=0)
            all_attention_scores.append(attention_scores.cpu().numpy())
    
    return np.mean(all_attention_scores, axis=0)

def extract_statistical_importance(model, dataloader, device='cpu'):
    """基于统计方法的重要性分数提取"""
    print("🔍 提取基于统计方法的重要性分数...")
    model.eval()
    all_scores = []
    all_predictions = []
    all_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            
            output, _, _, score1, score2 = model(batch.x, batch.edge_index, 
                                                batch.batch, batch.edge_attr, batch.pos)
            
            all_scores.append(score1.cpu().numpy())
            pred = output.argmax(dim=1)
            all_predictions.append(pred.cpu().numpy())
            all_labels.append(batch.y.cpu().numpy())
    
    scores = np.concatenate(all_scores, axis=0)
    predictions = np.concatenate(all_predictions, axis=0)
    labels = np.concatenate(all_labels, axis=0)
    
    # 只使用正确预测的样本
    correct_mask = (predictions == labels)
    
    if np.sum(correct_mask) > 0:
        # 计算每个ROI的重要性
        roi_importance = np.mean(scores[correct_mask], axis=0)
        
        # 计算置信度加权的重要性
        confidence = np.max(scores[correct_mask], axis=1)
        weights = confidence / np.sum(confidence)
        weighted_importance = np.average(scores[correct_mask], axis=0, weights=weights)
        
        # 计算最大激活的重要性
        max_importance = np.max(scores[correct_mask], axis=0)
        
        return roi_importance, weighted_importance, max_importance
    else:
        return None, None, None

def extract_feature_importance(model, dataloader, device='cpu'):
    """基于特征重要性分析"""
    print("🔍 提取基于特征重要性分析...")
    model.eval()
    feature_importance = []
    
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            
            # 获取中间层特征
            output, _, _, score1, score2 = model(batch.x, batch.edge_index, 
                                                batch.batch, batch.edge_attr, batch.pos)
            
            # 使用输入特征的方差作为重要性指标
            feature_var = torch.var(batch.x, dim=0)
            feature_importance.append(feature_var.cpu().numpy())
    
    return np.mean(feature_importance, axis=0)

def calculate_ensemble_importance(methods_results):
    """集成多种方法的重要性分数"""
    print("🔍 计算集成重要性分数...")

    valid_results = []
    shapes = []
    for method_name, result in methods_results.items():
        if result is not None:
            if isinstance(result, tuple):
                arr = result[0]
            else:
                arr = result
            valid_results.append(arr)
            shapes.append(arr.shape)

    # 只保留 shape 完全一致的结果
    shape_counts = Counter(shapes)
    if not shape_counts:
        print("[警告] 没有可用的结果用于集成！")
        return None
    # 取出现次数最多的 shape
    target_shape = shape_counts.most_common(1)[0][0]
    filtered_results = [arr for arr in valid_results if arr.shape == target_shape]

    if filtered_results:
        normalized_results = []
        for result in filtered_results:
            if result.std() > 0:
                normalized = (result - result.mean()) / result.std()
            else:
                normalized = result
            normalized_results.append(normalized)
        ensemble_importance = np.mean(normalized_results, axis=0)
        return ensemble_importance
    else:
        print("[警告] 没有 shape 一致的结果用于集成！")
        return None

def save_improved_importance_scores(results, save_dir='./importance_scores_improved'):
    """保存改进的重要性分数"""
    os.makedirs(save_dir, exist_ok=True)
    
    for method_name, importance in results.items():
        if importance is not None:
            np.save(os.path.join(save_dir, f'{method_name}_importance.npy'), importance)
            
            # 保存统计信息
            stats = {
                'method': method_name,
                'shape': importance.shape,
                'mean': float(np.mean(importance)),
                'std': float(np.std(importance)),
                'min': float(np.min(importance)),
                'max': float(np.max(importance)),
                'median': float(np.median(importance))
            }
            
            with open(os.path.join(save_dir, f'{method_name}_stats.pkl'), 'wb') as f:
                pickle.dump(stats, f)
    
    print(f"💾 改进的重要性分数已保存到: {save_dir}")

def visualize_importance_comparison(results, save_dir='./importance_scores_improved'):
    """可视化不同方法的重要性分数比较"""
    print("📊 创建重要性分数比较图...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 不同方法的分数分布
    ax1 = axes[0, 0]
    for method_name, importance in results.items():
        if importance is not None:
            ax1.hist(importance, bins=30, alpha=0.6, label=method_name)
    ax1.set_xlabel('Importance Score')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of ROI Importance Scores')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 前20个最重要ROI的比较
    ax2 = axes[0, 1]
    top_indices = {}
    for method_name, importance in results.items():
        if importance is not None:
            top_indices[method_name] = np.argsort(importance)[-20:][::-1]
    
    # 计算重叠度
    if len(top_indices) > 1:
        methods = list(top_indices.keys())
        overlap_matrix = np.zeros((len(methods), len(methods)))
        for i, method1 in enumerate(methods):
            for j, method2 in enumerate(methods):
                overlap = len(set(top_indices[method1][:10]) & set(top_indices[method2][:10]))
                overlap_matrix[i, j] = overlap
        
        im = ax2.imshow(overlap_matrix, cmap='Blues', aspect='auto')
        ax2.set_xticks(range(len(methods)))
        ax2.set_yticks(range(len(methods)))
        ax2.set_xticklabels(methods, rotation=45)
        ax2.set_yticklabels(methods)
        ax2.set_title('Top-10 ROI Overlap Between Methods')
        plt.colorbar(im, ax=ax2)
    
    # 3. 重要性分数排序
    ax3 = axes[1, 0]
    for method_name, importance in results.items():
        if importance is not None:
            sorted_scores = np.sort(importance)[::-1]
            ax3.plot(range(1, len(sorted_scores) + 1), sorted_scores, 
                    label=method_name, linewidth=2)
    ax3.set_xlabel('ROI Rank')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('ROI Importance Scores (Ranked)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 统计信息表格
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    info_text = "Importance Score Statistics:\n\n"
    for method_name, importance in results.items():
        if importance is not None:
            info_text += f"{method_name}:\n"
            info_text += f"  Mean: {np.mean(importance):.4f}\n"
            info_text += f"  Std: {np.std(importance):.4f}\n"
            info_text += f"  Max: {np.max(importance):.4f}\n"
            info_text += f"  Min: {np.min(importance):.4f}\n\n"
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'importance_comparison.png'), dpi=300, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='改进的ROI重要性分数提取')
    parser.add_argument('--model_path', type=str, default='./model_improved/best_model_fold0.pth',
                       help='训练好的模型路径')
    parser.add_argument('--data_path', type=str, default='./data/ABIDE_pcp/cpac/filt_noglobal',
                       help='数据路径')
    parser.add_argument('--save_dir', type=str, default='./importance_scores_improved',
                       help='保存重要性分数的目录')
    parser.add_argument('--batch_size', type=int, default=64,
                       help='批处理大小')
    parser.add_argument('--device', type=str, default='cpu',
                       help='设备 (cpu/cuda)')
    
    # 模型参数
    parser.add_argument('--indim', type=int, default=200, help='输入维度')
    parser.add_argument('--ratio', type=float, default=0.6, help='pooling比例')
    parser.add_argument('--nclass', type=int, default=2, help='类别数')
    parser.add_argument('--k', type=int, default=8, help='k (community num)')
    parser.add_argument('--nroi', type=int, default=116, help='ROI数 (R)')
    
    args = parser.parse_args()

    # === 自动推断 indim, k, nroi ===
    if os.path.exists(args.model_path):
        checkpoint = torch.load(args.model_path, map_location='cpu')
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        else:
            state_dict = checkpoint
        # 尝试从 Linear 层或 conv 层权重自动推断 indim, k, nroi
        indim_auto = None
        k_auto = None
        nroi_auto = None
        # 推断 indim
        for k, v in state_dict.items():
            if ('.weight' in k) and (len(v.shape) == 2):
                indim_auto = v.shape[1]
                break
        # 推断 k 和 nroi (R) 从 n1.0.weight: [k, R]
        if 'n1.0.weight' in state_dict:
            k_auto = state_dict['n1.0.weight'].shape[0]
            nroi_auto = state_dict['n1.0.weight'].shape[1]
        # 自动修正
        if indim_auto is not None:
            if hasattr(args, 'indim') and args.indim != indim_auto:
                print(f"[自动修正] 检测到权重文件输入特征维度为 {indim_auto}，覆盖命令行参数 indim={args.indim}")
            args.indim = indim_auto
            print(f"[自动推断] 使用权重文件推断的输入特征维度 indim={args.indim}")
        if k_auto is not None:
            if hasattr(args, 'k') and args.k != k_auto:
                print(f"[自动修正] 检测到权重文件 k={k_auto}，覆盖命令行参数 k={args.k}")
            args.k = k_auto
            print(f"[自动推断] 使用权重文件推断的 k={args.k}")
        if nroi_auto is not None:
            if hasattr(args, 'nroi') and args.nroi != nroi_auto:
                print(f"[自动修正] 检测到权重文件 nroi={nroi_auto}，覆盖命令行参数 nroi={args.nroi}")
            args.nroi = nroi_auto
            print(f"[自动推断] 使用权重文件推断的 nroi={args.nroi}")
        if indim_auto is None or k_auto is None or nroi_auto is None:
            print("[警告] 未能从权重文件自动推断全部参数，请确保 --indim --k --nroi 参数正确！")
    else:
        print(f"[警告] 权重文件 {args.model_path} 不存在，无法自动推断参数。")

    print("�� 开始改进的重要性分数提取...")
    
    # 1. 加载数据
    print("📂 加载数据...")
    dataset = ABIDEDataset(args.data_path, 'ABIDE')
    dataset.data.y = dataset.data.y.squeeze()
    dataset.data.x[dataset.data.x == float('inf')] = 0
    
    # 获取数据分割
    tr_index, val_index, te_index = train_val_test_split(fold=0)
    train_dataset = dataset[tr_index]
    val_dataset = dataset[val_index]
    test_dataset = dataset[te_index]
    
    # 2. 创建数据加载器
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    # 3. 加载模型
    model = Network(args.indim, args.ratio, args.nclass, k=args.k, R=args.nroi)
    if os.path.exists(args.model_path):
        checkpoint = torch.load(args.model_path, map_location='cpu')
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        print(f"✅ 成功加载模型: {args.model_path}")
    else:
        print(f"❌ 模型文件不存在: {args.model_path}")
        return
    model = model.to(args.device)
    
    # 4. 提取不同方法的重要性分数
    results = {}
    
    # 统计方法
    stat_importance, weighted_importance, max_importance = extract_statistical_importance(
        model, test_loader, args.device)
    results['statistical'] = stat_importance
    results['weighted'] = weighted_importance
    results['max_activation'] = max_importance
    
    # 注意力方法
    attention_importance = extract_attention_based_importance(model, test_loader, args.device)
    results['attention'] = attention_importance
    
    # 特征重要性
    feature_importance = extract_feature_importance(model, test_loader, args.device)
    results['feature'] = feature_importance
    
    # 梯度方法
    gradient_importance = extract_gradient_based_importance(model, test_loader, args.device)
    results['gradient'] = gradient_importance
    
    # 5. 计算集成重要性
    ensemble_importance = calculate_ensemble_importance(results)
    results['ensemble'] = ensemble_importance
    
    # 6. 保存结果
    save_improved_importance_scores(results, args.save_dir)
    
    # 7. 可视化比较
    visualize_importance_comparison(results, args.save_dir)
    
    print("✅ 改进的重要性分数提取完成！")
    print(f"📊 提取的方法:")
    for method_name, importance in results.items():
        if importance is not None:
            print(f"   - {method_name}: 均值={np.mean(importance):.4f}, 标准差={np.std(importance):.4f}")
    
    # 推荐使用的方法
    if ensemble_importance is not None:
        print(f"🎯 推荐使用集成方法的重要性分数")
        print(f"   文件位置: {args.save_dir}/ensemble_importance.npy")

    # === 自动输出脑区名称表 ===
    import json
    import pandas as pd
    from scipy.stats import spearmanr

    # === 自动生成 AAL116 ROI 名称映射 json（如不存在） ===
    aal116_names = [
        "Precentral_L", "Precentral_R", "Frontal_Sup_L", "Frontal_Sup_R",
        "Frontal_Sup_Orb_L", "Frontal_Sup_Orb_R", "Frontal_Mid_L", "Frontal_Mid_R",
        "Frontal_Mid_Orb_L", "Frontal_Mid_Orb_R", "Frontal_Inf_Oper_L", "Frontal_Inf_Oper_R",
        "Frontal_Inf_Tri_L", "Frontal_Inf_Tri_R", "Frontal_Inf_Orb_L", "Frontal_Inf_Orb_R",
        "Rolandic_Oper_L", "Rolandic_Oper_R", "Supp_Motor_Area_L", "Supp_Motor_Area_R",
        "Olfactory_L", "Olfactory_R", "Frontal_Sup_Medial_L", "Frontal_Sup_Medial_R",
        "Frontal_Med_Orb_L", "Frontal_Med_Orb_R", "Rectus_L", "Rectus_R",
        "Insula_L", "Insula_R", "Cingulum_Ant_L", "Cingulum_Ant_R",
        "Cingulum_Mid_L", "Cingulum_Mid_R", "Cingulum_Post_L", "Cingulum_Post_R",
        "Hippocampus_L", "Hippocampus_R", "ParaHippocampal_L", "ParaHippocampal_R",
        "Amygdala_L", "Amygdala_R", "Calcarine_L", "Calcarine_R",
        "Cuneus_L", "Cuneus_R", "Lingual_L", "Lingual_R",
        "Occipital_Sup_L", "Occipital_Sup_R", "Occipital_Mid_L", "Occipital_Mid_R",
        "Occipital_Inf_L", "Occipital_Inf_R", "Fusiform_L", "Fusiform_R",
        "Postcentral_L", "Postcentral_R", "Parietal_Sup_L", "Parietal_Sup_R",
        "Parietal_Inf_L", "Parietal_Inf_R", "SupraMarginal_L", "SupraMarginal_R",
        "Angular_L", "Angular_R", "Precuneus_L", "Precuneus_R",
        "Paracentral_Lobule_L", "Paracentral_Lobule_R", "Caudate_L", "Caudate_R",
        "Putamen_L", "Putamen_R", "Pallidum_L", "Pallidum_R",
        "Thalamus_L", "Thalamus_R", "Heschl_L", "Heschl_R",
        "Temporal_Sup_L", "Temporal_Sup_R", "Temporal_Pole_Sup_L", "Temporal_Pole_Sup_R",
        "Temporal_Mid_L", "Temporal_Mid_R", "Temporal_Pole_Mid_L", "Temporal_Pole_Mid_R",
        "Temporal_Inf_L", "Temporal_Inf_R", "Cerebelum_Crus1_L", "Cerebelum_Crus1_R",
        "Cerebelum_Crus2_L", "Cerebelum_Crus2_R", "Cerebelum_3_L", "Cerebelum_3_R",
        "Cerebelum_4_5_L", "Cerebelum_4_5_R", "Cerebelum_6_L", "Cerebelum_6_R",
        "Cerebelum_7b_L", "Cerebelum_7b_R", "Cerebelum_8_L", "Cerebelum_8_R",
        "Cerebelum_9_L", "Cerebelum_9_R", "Cerebelum_10_L", "Cerebelum_10_R",
        "Vermis_1_2", "Vermis_3", "Vermis_4_5", "Vermis_6", "Vermis_7", "Vermis_8", "Vermis_9", "Vermis_10"
    ]
    aal116_json_path = './aal116_roi_id2name.json'
    if not os.path.exists(aal116_json_path):
        roi2name = {str(i): name for i, name in enumerate(aal116_names)}
        with open(aal116_json_path, 'w') as f:
            json.dump(roi2name, f, indent=2)
        print(f'已自动生成标准AAL116脑区名称映射: {aal116_json_path}')
    # 用AAL116标准映射
    roi_info_path = aal116_json_path

    ensemble_path = os.path.join(args.save_dir, 'ensemble_importance.npy')
    output_csv = os.path.join(args.save_dir, 'roi_importance_with_name.csv')
    if os.path.exists(ensemble_path) and os.path.exists(roi_info_path):
        importance = np.load(ensemble_path)
        with open(roi_info_path, 'r') as f:
            roi2name = json.load(f)
        df = pd.DataFrame({
            'ROI': np.arange(len(importance)),
            'BrainRegion': [roi2name.get(str(i), f'ROI_{i}') for i in range(len(importance))],
            'Importance': importance
        })
        df = df.sort_values('Importance', ascending=False)
        df['Rank'] = np.arange(1, len(df)+1)
        df.to_csv(output_csv, index=False)
        print(f'已保存: {output_csv}')
        print(df.head(10))

    # === 自动与临床数据相关性分析 ===
    clinical_csv = './data/clinical_scores.csv'
    corr_csv = os.path.join(args.save_dir, 'roi_clinical_correlation.csv')
    if os.path.exists(ensemble_path) and os.path.exists(clinical_csv):
        importance = np.load(ensemble_path)
        clinical = pd.read_csv(clinical_csv)
        results = []
        for col in clinical.columns[1:]:
            corr, pval = spearmanr(importance, clinical[col])
            results.append({'ClinicalVar': col, 'SpearmanR': corr, 'PValue': pval})
        df_corr = pd.DataFrame(results).sort_values('PValue')
        df_corr.to_csv(corr_csv, index=False)
        print(f'已保存: {corr_csv}')
        print(df_corr.head(5))

    # === 自动生成多任务对比热图 ===
    csv_files = glob.glob('./results/*/roi_importance_with_name.csv')
    if len(csv_files) >= 2:
        dfs = []
        task_names = []
        for path in csv_files:
            task = os.path.basename(os.path.dirname(path))
            df = pd.read_csv(path)[['BrainRegion', 'Importance']]
            df = df.rename(columns={'Importance': task})
            dfs.append(df.set_index('BrainRegion'))
            task_names.append(task)
        heat = pd.concat(dfs, axis=1).fillna(0)
        plt.figure(figsize=(8, max(10, len(heat)//3)))
        sns.heatmap(heat, cmap='viridis')
        plt.title('ROI Importance Across Tasks')
        plt.tight_layout()
        multitask_heatmap_path = './results/roi_importance_multitask_heatmap.png'
        plt.savefig(multitask_heatmap_path)
        print(f'已保存多任务对比热图: {multitask_heatmap_path}')

def extract_and_save_importance(args):
    print("📂 加载数据...")
    dataset = PainGraphDataset(args.data_path)
    from torch.utils.data import Subset
    import numpy as np
    import os
    all_task_types = set()
    for i in range(len(dataset)):
        data = dataset.get(i)
        if hasattr(data, 'task_type'):
            all_task_types.add(int(data.task_type[0].item()))
    print(f"检测到任务类型: {sorted(all_task_types)}")

    # 先读取模型权重，推断期望的输入特征数
    checkpoint_expected_input_dim = None
    if os.path.exists(args.model_path):
        checkpoint = torch.load(args.model_path, map_location='cpu')
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        else:
            state_dict = checkpoint
        # 推断 indim
        for k, v in state_dict.items():
            if ('.weight' in k) and (len(v.shape) == 2):
                checkpoint_expected_input_dim = v.shape[1]
                break
        print(f"模型权重期望输入特征数: {checkpoint_expected_input_dim}")
    else:
        print(f"❌ 模型权重文件 {args.model_path} 不存在，无法推断输入特征数。")
        return

    for ttype in sorted(all_task_types):
        if ttype == -1:
            print(f"跳过无效 task_type={ttype}")
            continue
        indices = [i for i in range(len(dataset)) if hasattr(dataset.get(i), 'task_type') and int(dataset.get(i).task_type[0].item()) == ttype]
        if not indices:
            continue
        print(f"\n==== 处理 task_type={ttype} 的子集，共 {len(indices)} 个样本 ====")
        sub_dataset = Subset(dataset, indices)
        sample_data = dataset.get(indices[0])
        if checkpoint_expected_input_dim is not None and sample_data.x.size(1) != checkpoint_expected_input_dim:
            print(f"跳过 task_type={ttype}，特征数 {sample_data.x.size(1)} 与权重期望 {checkpoint_expected_input_dim} 不一致")
            continue
        from torch_geometric.loader import DataLoader
        test_loader = DataLoader(sub_dataset, batch_size=args.batch_size, shuffle=False)
        args.indim = sample_data.x.size(1)
        args.nroi = sample_data.x.size(0)
        model = Network(args.indim, args.ratio, args.nclass, k=args.k, R=args.nroi)
        if os.path.exists(args.model_path):
            checkpoint = torch.load(args.model_path, map_location='cpu')
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
            print(f"✅ 成功加载模型: {args.model_path}")
        else:
            print(f"❌ 模型文件不存在: {args.model_path}")
            continue
        model = model.to(args.device)
        results = {}
        stat_importance, weighted_importance, max_importance = extract_statistical_importance(model, test_loader, args.device)
        results['statistical'] = stat_importance
        results['weighted'] = weighted_importance
        results['max_activation'] = max_importance
        attention_importance = extract_attention_based_importance(model, test_loader, args.device)
        results['attention'] = attention_importance
        feature_importance = extract_feature_importance(model, test_loader, args.device)
        results['feature'] = feature_importance
        gradient_importance = extract_gradient_based_importance(model, test_loader, args.device)
        results['gradient'] = gradient_importance
        ensemble_importance = calculate_ensemble_importance(results)
        results['ensemble'] = ensemble_importance
        save_dir = os.path.join(args.save_dir, f'task{ttype}')
        os.makedirs(save_dir, exist_ok=True)
        save_improved_importance_scores(results, save_dir)
        src_npy = os.path.join(save_dir, 'ensemble_importance.npy')
        dst_npy = os.path.join(save_dir, f'ensemble_importance_task{ttype}.npy')
        if os.path.exists(src_npy):
            import shutil
            shutil.copy(src_npy, dst_npy)
        src_csv = os.path.join(save_dir, 'roi_importance_with_name.csv')
        dst_csv = os.path.join(save_dir, f'roi_importance_task{ttype}.csv')
        if os.path.exists(src_csv):
            shutil.copy(src_csv, dst_csv)
        print(f"已保存 task{ttype} 的重要性结果到 {save_dir}")

if __name__ == '__main__':
    # 只处理 all_graphs 目录
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--ratio', type=float, default=0.6)
    parser.add_argument('--nclass', type=int, default=2)
    parser.add_argument('--indim', type=int, default=200)
    parser.add_argument('--k', type=int, default=8)
    parser.add_argument('--nroi', type=int, default=116)
    parser.add_argument('--model_path', type=str, default='./model/0.pth')
    parser.add_argument('--save_dir', type=str, default='./results/all_graphs')
    args = parser.parse_args()
    args.data_path = 'data/pain_data/all_graphs'
    extract_and_save_importance(args) 