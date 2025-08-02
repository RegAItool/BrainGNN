#!/usr/bin/env python3
"""
自动导出BrainGNN重要性分数
从训练好的模型中提取每个ROI的重要性分数，用于脑图谱可视化
"""

import torch
import numpy as np
import os
import pickle
from torch_geometric.data import DataLoader
import argparse
from net.braingnn import Network
from imports.ABIDEDataset import ABIDEDataset
from imports.utils import train_val_test_split

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

def extract_importance_scores(model, dataloader, device='cpu'):
    """提取重要性分数"""
    model.eval()
    all_scores1 = []
    all_scores2 = []
    all_predictions = []
    all_labels = []
    
    print("🔍 正在提取重要性分数...")
    
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            
            # 前向传播，获取分数
            output, _, _, score1, score2 = model(batch.x, batch.edge_index, 
                                                batch.batch, batch.edge_attr, batch.pos)
            
            # 收集分数
            all_scores1.append(score1.cpu().numpy())
            all_scores2.append(score2.cpu().numpy())
            
            # 收集预测和标签
            pred = output.argmax(dim=1)
            all_predictions.append(pred.cpu().numpy())
            all_labels.append(batch.y.cpu().numpy())
    
    # 转换为numpy数组
    scores1 = np.concatenate(all_scores1, axis=0)  # shape: (n_samples, n_rois)
    scores2 = np.concatenate(all_scores2, axis=0)  # shape: (n_samples, n_rois)
    predictions = np.concatenate(all_predictions, axis=0)
    labels = np.concatenate(all_labels, axis=0)
    
    return scores1, scores2, predictions, labels

def calculate_roi_importance(scores1, scores2, predictions, labels, method='mean'):
    """只用第一层分数计算每个ROI的重要性分数"""
    print(f"📊 计算ROI重要性分数 (方法: {method}, 只用第一层)...")
    correct_mask = (predictions == labels)
    print(f"   正确预测样本数: {np.sum(correct_mask)}/{len(predictions)}")
    if method == 'mean':
        roi_importance1 = np.mean(scores1[correct_mask], axis=0)
    elif method == 'weighted':
        confidence = np.max(scores1[correct_mask], axis=1)
        weights = confidence / np.sum(confidence)
        roi_importance1 = np.average(scores1[correct_mask], axis=0, weights=weights)
    elif method == 'max':
        roi_importance1 = np.max(scores1[correct_mask], axis=0)
    roi_importance = roi_importance1
    roi_importance2 = None
    return roi_importance, roi_importance1, roi_importance2

def save_importance_scores(roi_importance, roi_importance1, roi_importance2, 
                          scores1, scores2, predictions, labels, save_dir='./importance_scores'):
    """保存重要性分数"""
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存主要的重要性分数
    np.save(os.path.join(save_dir, 'roi_importance.npy'), roi_importance)
    np.save(os.path.join(save_dir, 'roi_importance_layer1.npy'), roi_importance1)
    
    # 保存原始分数数据
    np.save(os.path.join(save_dir, 'all_scores_layer1.npy'), scores1)
    
    # 收集预测和标签
    all_predictions = predictions
    all_labels = labels
    
    # 保存统计信息
    stats = {
        'n_samples': len(predictions),
        'n_correct': np.sum(predictions == labels),
        'accuracy': np.mean(predictions == labels),
        'roi_importance_shape': roi_importance.shape,
        'score1_shape': scores1.shape
    }
    
    with open(os.path.join(save_dir, 'stats.pkl'), 'wb') as f:
        pickle.dump(stats, f)
    
    print(f"💾 重要性分数已保存到: {save_dir}")
    print(f"   - ROI重要性分数: {roi_importance.shape}")
    print(f"   - 准确率: {stats['accuracy']:.3f}")
    print(f"   - 正确预测样本: {stats['n_correct']}/{stats['n_samples']}")

def main():
    parser = argparse.ArgumentParser(description='导出BrainGNN重要性分数')
    parser.add_argument('--model_path', type=str, default='./model/best_model.pth',
                       help='训练好的模型路径')
    parser.add_argument('--data_path', type=str, default='./data/ABIDE_pcp/cpac/filt_noglobal',
                       help='数据路径')
    parser.add_argument('--save_dir', type=str, default='./importance_scores',
                       help='保存重要性分数的目录')
    parser.add_argument('--method', type=str, default='mean', 
                       choices=['mean', 'weighted', 'max'],
                       help='计算ROI重要性的方法')
    parser.add_argument('--batch_size', type=int, default=100,
                       help='批处理大小')
    parser.add_argument('--device', type=str, default='cpu',
                       help='设备 (cpu/cuda)')
    
    # 模型参数
    parser.add_argument('--indim', type=int, default=200, help='输入维度')
    parser.add_argument('--ratio', type=float, default=0.5, help='pooling比例')
    parser.add_argument('--nclass', type=int, default=2, help='类别数')
    
    args = parser.parse_args()
    
    print("🚀 开始导出BrainGNN重要性分数...")
    
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
    scores1, scores2, predictions, labels = extract_importance_scores(model, test_loader, args.device)
    
    # 5. 计算ROI重要性
    roi_importance, roi_importance1, roi_importance2 = calculate_roi_importance(
        scores1, scores2, predictions, labels, args.method)
    
    # 6. 保存结果
    save_importance_scores(roi_importance, roi_importance1, roi_importance2,
                          scores1, scores2, predictions, labels, args.save_dir)
    
    print("✅ 重要性分数导出完成！")
    print(f"📊 前10个ROI的重要性分数:")
    top_indices = np.argsort(roi_importance)[-10:][::-1]
    for i, idx in enumerate(top_indices):
        print(f"   ROI {idx:3d}: {roi_importance[idx]:.4f}")

if __name__ == '__main__':
    main() 