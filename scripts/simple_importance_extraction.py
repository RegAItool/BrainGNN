#!/usr/bin/env python3
"""
简化的重要性分数提取
专注于统计方法来计算ROI重要性分数
"""

import torch
import numpy as np
import os
import pickle
import argparse
from torch_geometric.data import DataLoader
from net.braingnn import Network
from imports.ABIDEDataset import ABIDEDataset
from imports.utils import train_val_test_split
import matplotlib.pyplot as plt

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

def extract_improved_importance(model, dataloader, device='cpu'):
    """提取改进的重要性分数"""
    print("🔍 提取改进的重要性分数...")
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
        
        # 计算标准差加权的重要性
        std_importance = np.std(scores[correct_mask], axis=0)
        
        return roi_importance, weighted_importance, max_importance, std_importance
    else:
        return None, None, None, None

def save_importance_scores(results, save_dir='./importance_scores_improved'):
    """保存重要性分数"""
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
    
    print(f"💾 重要性分数已保存到: {save_dir}")

def visualize_importance_comparison(results, save_dir='./importance_scores_improved'):
    """可视化重要性分数比较"""
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
    
    # 2. 重要性分数排序
    ax2 = axes[0, 1]
    for method_name, importance in results.items():
        if importance is not None:
            sorted_scores = np.sort(importance)[::-1]
            ax2.plot(range(1, len(sorted_scores) + 1), sorted_scores, 
                    label=method_name, linewidth=2)
    ax2.set_xlabel('ROI Rank')
    ax2.set_ylabel('Importance Score')
    ax2.set_title('ROI Importance Scores (Ranked)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. 前20个最重要ROI
    ax3 = axes[1, 0]
    for method_name, importance in results.items():
        if importance is not None:
            top_indices = np.argsort(importance)[-20:][::-1]
            top_scores = importance[top_indices]
            ax3.bar(range(len(top_indices)), top_scores, alpha=0.6, label=method_name)
    ax3.set_xlabel('Top 20 ROIs')
    ax3.set_ylabel('Importance Score')
    ax3.set_title('Top 20 Most Important ROIs')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 统计信息表格
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    info_text = "Importance Score Statistics:\n\n"
    for method_name, importance in results.items():
        if importance is not None:
            info_text += f"{method_name}:\n"
            info_text += f"  Mean: {np.mean(importance):.6f}\n"
            info_text += f"  Std: {np.std(importance):.6f}\n"
            info_text += f"  Max: {np.max(importance):.6f}\n"
            info_text += f"  Min: {np.min(importance):.6f}\n"
            info_text += f"  Range: {np.max(importance) - np.min(importance):.6f}\n\n"
    
    ax4.text(0.1, 0.9, info_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'importance_comparison.png'), dpi=300, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='简化的重要性分数提取')
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
    
    args = parser.parse_args()
    
    print("🚀 开始简化的重要性分数提取...")
    
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
    model = load_trained_model(args.model_path, args)
    if model is None:
        return
    
    model = model.to(args.device)
    
    # 4. 提取重要性分数
    results = {}
    
    # 统计方法
    stat_importance, weighted_importance, max_importance, std_importance = extract_improved_importance(
        model, test_loader, args.device)
    results['statistical'] = stat_importance
    results['weighted'] = weighted_importance
    results['max_activation'] = max_importance
    results['std_based'] = std_importance
    
    # 5. 保存结果
    save_importance_scores(results, args.save_dir)
    
    # 6. 可视化比较
    visualize_importance_comparison(results, args.save_dir)
    
    print("✅ 简化的重要性分数提取完成！")
    print(f"📊 提取的方法:")
    for method_name, importance in results.items():
        if importance is not None:
            print(f"   - {method_name}: 均值={np.mean(importance):.6f}, 标准差={np.std(importance):.6f}")
            print(f"     范围: {np.max(importance) - np.min(importance):.6f}")
    
    # 推荐使用的方法
    if stat_importance is not None:
        print(f"🎯 推荐使用统计方法的重要性分数")
        print(f"   文件位置: {args.save_dir}/statistical_importance.npy")
        
        # 比较改进前后的效果
        print(f"\n📈 改进效果分析:")
        print(f"   - 标准差: {np.std(stat_importance):.6f}")
        print(f"   - 分数范围: {np.max(stat_importance) - np.min(stat_importance):.6f}")
        print(f"   - 前10个最重要ROI: {np.argsort(stat_importance)[-10:][::-1]}")

if __name__ == '__main__':
    main() 