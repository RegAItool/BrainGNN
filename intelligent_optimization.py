#!/usr/bin/env python3
"""
BrainGNN智能优化脚本
自动优化模型性能，包括超参数调优、数据增强、模型改进等
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import json
import os
from datetime import datetime
import optuna
import logging

from imports.PainGraphDataset import PainGraphDataset
from net.multitask_braingnn import MultiTaskBrainGNN

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedPainGraphDataset(PainGraphDataset):
    """增强的数据集类，支持数据增强和平衡采样"""
    
    def __init__(self, root_dir, balance_classes=True, augmentation=True):
        super().__init__(root_dir)
        self.balance_classes = balance_classes
        self.augmentation = augmentation
        
        if balance_classes:
            self._balance_dataset()
    
    def _balance_dataset(self):
        """平衡数据集类别"""
        labels = []
        for i in range(len(self.pt_files)):
            try:
                data = torch.load(self.pt_files[i])
                labels.append(int(data.y.item()))
            except:
                continue
        
        labels = np.array(labels)
        unique_labels, counts = np.unique(labels, return_counts=True)
        max_count = max(counts)
        
        # 为少数类创建重复采样索引
        balanced_indices = []
        for label in unique_labels:
            label_indices = np.where(labels == label)[0]
            # 重复采样到最大类别数量
            repeats = max_count // len(label_indices)
            remainder = max_count % len(label_indices)
            
            balanced_indices.extend(label_indices.tolist() * repeats)
            balanced_indices.extend(label_indices[:remainder].tolist())
        
        # 更新文件列表
        original_files = self.pt_files.copy()
        self.pt_files = [original_files[i] for i in balanced_indices]
        logger.info(f"数据平衡后样本数: {len(self.pt_files)}")
    
    def get(self, idx):
        data = super().get(idx)
        
        # 数据增强
        if self.augmentation and torch.rand(1) < 0.3:
            # 添加轻微噪声
            noise = torch.randn_like(data.x) * 0.01
            data.x = data.x + noise
            
            # 边权重扰动
            if hasattr(data, 'edge_attr') and data.edge_attr is not None:
                edge_noise = torch.randn_like(data.edge_attr) * 0.005
                data.edge_attr = data.edge_attr + edge_noise
        
        return data

class ImprovedBrainGNN(MultiTaskBrainGNN):
    """改进的BrainGNN模型"""
    
    def __init__(self, in_dim, hidden_dim=64, n_roi=116, dropout=0.3, use_attention=True):
        super().__init__(in_dim, hidden_dim, n_roi)
        self.dropout = dropout
        self.use_attention = use_attention
        
        # 添加注意力机制
        if use_attention:
            self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4, dropout=dropout)
        
        # 添加Dropout层
        self.dropout_layer = nn.Dropout(dropout)
        
        # 改进的分类头，添加BatchNorm
        self.task_heads = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim//2),
                nn.BatchNorm1d(hidden_dim//2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim//2, 2)
            ),  # gender
            nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim//2),
                nn.BatchNorm1d(hidden_dim//2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim//2, 3)
            ),  # pain_level
            nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim//2),
                nn.BatchNorm1d(hidden_dim//2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim//2, 1)
            ),  # age
            nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim//2),
                nn.BatchNorm1d(hidden_dim//2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim//2, 2)
            )   # stimulus
        ])
    
    def forward(self, data):
        x, *_ = self.encoder(data.x, data.edge_index, data.batch, data.edge_attr, data.pos)
        
        # 应用dropout
        x = self.dropout_layer(x)
        
        # 注意力机制
        if self.use_attention:
            x_unsqueezed = x.unsqueeze(0)  # (1, batch_size, hidden_dim)
            attn_output, _ = self.attention(x_unsqueezed, x_unsqueezed, x_unsqueezed)
            x = attn_output.squeeze(0)
        
        # 任务预测
        if hasattr(data, 'task_type'):
            task_id = int(data.task_type[0]) if isinstance(data.task_type, torch.Tensor) else int(data.task_type)
        else:
            task_id = 0
        
        out = self.task_heads[task_id](x)
        return out, self.task_types[task_id]

def weighted_loss_function(output, target, class_weights):
    """加权损失函数"""
    if class_weights is not None:
        weights = class_weights[target]
        loss = F.nll_loss(output, target, reduction='none')
        return (loss * weights).mean()
    else:
        return F.nll_loss(output, target)

def train_with_optimization(trial=None):
    """训练函数，支持Optuna超参数优化"""
    
    # 超参数定义
    if trial:
        # Optuna优化
        params = {
            'lr': trial.suggest_float('lr', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_categorical('batch_size', [8, 16, 32, 64]),
            'hidden_dim': trial.suggest_categorical('hidden_dim', [32, 64, 128, 256]),
            'dropout': trial.suggest_float('dropout', 0.1, 0.7),
            'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True),
            'use_class_weights': trial.suggest_categorical('use_class_weights', [True, False]),
            'use_attention': trial.suggest_categorical('use_attention', [True, False])
        }
    else:
        # 默认优化参数
        params = {
            'lr': 0.001,
            'batch_size': 32,
            'hidden_dim': 128,
            'dropout': 0.4,
            'weight_decay': 1e-4,
            'use_class_weights': True,
            'use_attention': True
        }
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 加载增强数据集
    print("🚀 加载增强数据集...")
    dataset = EnhancedPainGraphDataset('./data/pain_data/all_graphs/', 
                                     balance_classes=True, 
                                     augmentation=True)
    
    # 过滤数据
    filtered_data = []
    for i in range(len(dataset)):
        try:
            data = dataset[i]
            if data.x.shape == (116, 1):
                data.y = data.y.long()
                filtered_data.append(data)
        except:
            continue
    
    # 计算类别权重
    labels = [data.y.item() for data in filtered_data]
    class_weights = None
    if params['use_class_weights']:
        class_weights = compute_class_weight('balanced', 
                                           classes=np.unique(labels), 
                                           y=labels)
        class_weights = torch.FloatTensor(class_weights).to(device)
    
    # 数据集划分
    train_size = int(0.7 * len(filtered_data))
    val_size = int(0.15 * len(filtered_data))
    test_size = len(filtered_data) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        filtered_data, [train_size, val_size, test_size]
    )
    
    train_loader = DataLoader(train_dataset, batch_size=params['batch_size'], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=params['batch_size'], shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=params['batch_size'], shuffle=False)
    
    # 创建改进模型
    model = ImprovedBrainGNN(in_dim=1, 
                           hidden_dim=params['hidden_dim'],
                           n_roi=116,
                           dropout=params['dropout'],
                           use_attention=params['use_attention']).to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), 
                                 lr=params['lr'], 
                                 weight_decay=params['weight_decay'])
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=10, verbose=True
    )
    
    # 训练循环
    best_val_f1 = 0
    patience_counter = 0
    max_epochs = 50
    
    for epoch in range(max_epochs):
        # 训练
        model.train()
        total_loss = 0
        all_preds = []
        all_labels = []
        
        for data in train_loader:
            data = data.to(device)
            optimizer.zero_grad()
            
            out, _ = model(data)
            
            if params['use_class_weights']:
                loss = weighted_loss_function(out, data.y, class_weights)
            else:
                loss = F.nll_loss(out, data.y)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # 梯度裁剪
            optimizer.step()
            
            total_loss += loss.item()
            pred = out.argmax(dim=1)
            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(data.y.cpu().numpy())
        
        train_f1 = f1_score(all_labels, all_preds, average='weighted')
        
        # 验证
        model.eval()
        val_preds = []
        val_labels = []
        
        with torch.no_grad():
            for data in val_loader:
                data = data.to(device)
                out, _ = model(data)
                pred = out.argmax(dim=1)
                val_preds.extend(pred.cpu().numpy())
                val_labels.extend(data.y.cpu().numpy())
        
        val_f1 = f1_score(val_labels, val_preds, average='weighted')
        val_acc = accuracy_score(val_labels, val_preds)
        
        scheduler.step(val_f1)
        
        print(f'Epoch {epoch+1}/{max_epochs}, Loss: {total_loss/len(train_loader):.4f}, '
              f'Train F1: {train_f1:.4f}, Val F1: {val_f1:.4f}, Val Acc: {val_acc:.4f}')
        
        # 早停和模型保存
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            patience_counter = 0
            if not trial:  # 只在非优化模式下保存模型
                torch.save(model.state_dict(), './model/optimized_brain_model.pth')
        else:
            patience_counter += 1
            if patience_counter >= 15:
                print("早停触发")
                break
    
    # 最终测试
    if not trial:
        model.load_state_dict(torch.load('./model/optimized_brain_model.pth'))
    
    model.eval()
    test_preds = []
    test_labels = []
    
    with torch.no_grad():
        for data in test_loader:
            data = data.to(device)
            out, _ = model(data)
            pred = out.argmax(dim=1)
            test_preds.extend(pred.cpu().numpy())
            test_labels.extend(data.y.cpu().numpy())
    
    test_acc = accuracy_score(test_labels, test_preds)
    test_f1 = f1_score(test_labels, test_preds, average='weighted')
    
    if not trial:
        print("\n" + "="*50)
        print("🎯 优化训练完成！")
        print(f"最佳验证F1: {best_val_f1:.4f}")
        print(f"测试准确率: {test_acc:.4f}")
        print(f"测试F1分数: {test_f1:.4f}")
        print("="*50)
        
        # 保存详细报告
        report = classification_report(test_labels, test_preds, output_dict=True)
        results = {
            'timestamp': datetime.now().isoformat(),
            'parameters': params,
            'best_val_f1': best_val_f1,
            'test_accuracy': test_acc,
            'test_f1': test_f1,
            'classification_report': report
        }
        
        with open('./model/optimization_results.json', 'w') as f:
            json.dump(results, f, indent=2)
    
    return best_val_f1

def run_hyperparameter_optimization():
    """运行超参数优化"""
    print("🔬 开始超参数优化...")
    
    study = optuna.create_study(direction='maximize')
    study.optimize(train_with_optimization, n_trials=20)
    
    print("📊 超参数优化完成！")
    print("最佳参数:", study.best_params)
    print("最佳F1分数:", study.best_value)
    
    # 使用最佳参数重新训练
    print("🚀 使用最佳参数重新训练...")
    best_trial = study.best_trial
    train_with_optimization()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--optimize', action='store_true', help='运行超参数优化')
    args = parser.parse_args()
    
    if args.optimize:
        run_hyperparameter_optimization()
    else:
        train_with_optimization()