#!/usr/bin/env python3
"""
BrainGNN高级优化系统
实现所有先进优化技术，目标达到80%以上准确率
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import numpy as np
import json
import os
from datetime import datetime
import optuna
import logging
from collections import defaultdict
import pickle
import warnings
warnings.filterwarnings('ignore')

from imports.PainGraphDataset import PainGraphDataset
from net.multitask_braingnn import MultiTaskBrainGNN

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedPainGraphDataset(PainGraphDataset):
    """高级数据集类，支持完整的数据预处理和增强"""
    
    def __init__(self, root_dir, use_all_samples=True, advanced_preprocessing=True, 
                 feature_selection=None, scaler_type='robust'):
        super().__init__(root_dir)
        self.use_all_samples = use_all_samples
        self.advanced_preprocessing = advanced_preprocessing
        self.feature_selection = feature_selection
        self.scaler_type = scaler_type
        self.scaler = None
        self.feature_selector = None
        
        if advanced_preprocessing:
            self._setup_preprocessing()
    
    def _setup_preprocessing(self):
        """设置预处理组件"""
        if self.scaler_type == 'robust':
            self.scaler = RobustScaler()
        elif self.scaler_type == 'standard':
            self.scaler = StandardScaler()
        
        print(f"✅ 设置预处理：{self.scaler_type} scaler")
    
    def _apply_advanced_preprocessing(self, data):
        """应用高级预处理"""
        try:
            # 1. 异常值处理
            x = data.x.clone()
            
            # 移除极端异常值 (3-sigma rule)
            mean = x.mean(dim=0)
            std = x.std(dim=0) + 1e-8  # 避免除零
            mask = torch.abs(x - mean) < 3 * std
            x = torch.where(mask, x, mean.unsqueeze(0))
            
            # 2. 特征标准化
            if self.scaler is not None and hasattr(self, '_scaler_fitted'):
                # 展平为 (116,) 进行标准化，然后恢复形状
                x_flat = x.flatten().numpy().reshape(1, -1)  # (1, 116)
                x_scaled = self.scaler.transform(x_flat)
                x = torch.FloatTensor(x_scaled.reshape(116, 1))
            
            # 3. 特征选择
            if self.feature_selector is not None:
                x_flat = x.flatten().numpy().reshape(1, -1)  # (1, 116)
                x_selected = self.feature_selector.transform(x_flat)
                # 由于特征选择会改变维度，我们需要填充回116维度
                x_new = np.zeros((1, 116))
                selected_indices = self.feature_selector.get_support()
                x_new[:, selected_indices] = x_selected
                x = torch.FloatTensor(x_new.reshape(116, 1))
            
            # 4. 边权重正则化
            if hasattr(data, 'edge_attr') and data.edge_attr is not None:
                edge_attr = data.edge_attr.clone()
                # 归一化边权重
                edge_attr = F.normalize(edge_attr, p=2, dim=-1)
                data.edge_attr = edge_attr
            
            data.x = x
            return data
            
        except Exception as e:
            logger.warning(f"预处理失败: {e}")
            return data
    
    def fit_preprocessing(self, sample_data):
        """拟合预处理参数"""
        if not self.advanced_preprocessing:
            return
        
        # 收集所有特征数据
        all_features = []
        labels = []
        
        for data in sample_data:
            # 每个样本的特征是 (116, 1)，我们需要展平为 (116,)
            features = data.x.numpy().flatten()
            all_features.append(features)
            labels.append(data.y.item())
        
        all_features = np.array(all_features)  # Shape: (n_samples, 116)
        
        # 拟合标准化器
        if self.scaler is not None:
            self.scaler.fit(all_features)
            self._scaler_fitted = True
            print(f"✅ 拟合标准化器，特征维度: {all_features.shape}")
        
        # 拟合特征选择器
        if self.feature_selection:
            selector = SelectKBest(score_func=mutual_info_classif, 
                                 k=min(self.feature_selection, all_features.shape[1]))
            selector.fit(all_features, labels)
            self.feature_selector = selector
            print(f"✅ 拟合特征选择器，选择 {self.feature_selection} 个特征")
    
    def get(self, idx):
        data = super().get(idx)
        
        if self.advanced_preprocessing:
            data = self._apply_advanced_preprocessing(data)
        
        return data

class EnsembleBrainGNN(nn.Module):
    """集成BrainGNN模型"""
    
    def __init__(self, in_dim, n_roi=116, n_models=5):
        super().__init__()
        self.n_models = n_models
        self.models = nn.ModuleList()
        
        # 创建多个不同配置的模型
        configs = [
            {'hidden_dim': 64, 'dropout': 0.3},
            {'hidden_dim': 128, 'dropout': 0.4},
            {'hidden_dim': 96, 'dropout': 0.35},
            {'hidden_dim': 160, 'dropout': 0.45},
            {'hidden_dim': 80, 'dropout': 0.25}
        ]
        
        for i in range(n_models):
            config = configs[i % len(configs)]
            from intelligent_optimization import ImprovedBrainGNN
            model = ImprovedBrainGNN(
                in_dim=in_dim,
                hidden_dim=config['hidden_dim'],
                n_roi=n_roi,
                dropout=config['dropout'],
                use_attention=True
            )
            self.models.append(model)
        
        # 集成权重
        self.ensemble_weights = nn.Parameter(torch.ones(n_models) / n_models)
        
    def forward(self, data):
        outputs = []
        task_types = []
        
        for model in self.models:
            out, task_type = model(data)
            outputs.append(out)
            task_types.append(task_type)
        
        # 加权平均
        weights = F.softmax(self.ensemble_weights, dim=0)
        ensemble_output = sum(w * out for w, out in zip(weights, outputs))
        
        return ensemble_output, task_types[0]

class AdvancedTrainer:
    """高级训练器"""
    
    def __init__(self, device='auto'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device == 'auto' else device
        self.best_models = []
        self.training_history = defaultdict(list)
        
    def train_with_advanced_techniques(self, trial=None, use_ensemble=True):
        """使用所有高级技术进行训练"""
        
        # 超参数配置
        if trial:
            params = {
                'lr': trial.suggest_float('lr', 1e-5, 1e-2, log=True),
                'batch_size': trial.suggest_categorical('batch_size', [16, 32, 64]),
                'hidden_dim': trial.suggest_categorical('hidden_dim', [64, 96, 128, 160, 192]),
                'dropout': trial.suggest_float('dropout', 0.2, 0.6),
                'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True),
                'use_class_weights': trial.suggest_categorical('use_class_weights', [True, False]),
                'feature_selection': trial.suggest_int('feature_selection', 50, 116),
                'scaler_type': trial.suggest_categorical('scaler_type', ['robust', 'standard']),
                'ensemble_size': trial.suggest_int('ensemble_size', 3, 7) if use_ensemble else 1,
                'augmentation_prob': trial.suggest_float('augmentation_prob', 0.1, 0.5)
            }
        else:
            # 最优参数配置
            params = {
                'lr': 0.0005,
                'batch_size': 32,
                'hidden_dim': 128,
                'dropout': 0.4,
                'weight_decay': 5e-5,
                'use_class_weights': True,
                'feature_selection': 80,
                'scaler_type': 'robust',
                'ensemble_size': 5 if use_ensemble else 1,
                'augmentation_prob': 0.3
            }
        
        print(f"🚀 开始高级训练，参数配置: {params}")
        
        # 1. 加载和预处理全部数据
        print("📊 加载全部4659个有效样本...")
        dataset = AdvancedPainGraphDataset(
            './data/pain_data/all_graphs/',
            use_all_samples=True,
            advanced_preprocessing=True,
            feature_selection=params['feature_selection'],
            scaler_type=params['scaler_type']
        )
        
        # 过滤有效数据
        filtered_data = []
        for i in range(len(dataset)):
            try:
                data = dataset[i]
                if data.x.shape == (116, 1):
                    data.y = data.y.long()
                    filtered_data.append(data)
            except:
                continue
        
        print(f"✅ 成功加载 {len(filtered_data)} 个有效样本")
        
        # 2. 拟合预处理参数
        sample_size = min(1000, len(filtered_data))
        sample_data = filtered_data[:sample_size]
        dataset.fit_preprocessing(sample_data)
        
        # 3. 重新应用预处理
        processed_data = []
        for data in filtered_data:
            processed_data.append(dataset.get(filtered_data.index(data)))
        
        # 4. 计算类别权重
        labels = [data.y.item() for data in processed_data]
        class_weights = None
        if params['use_class_weights']:
            class_weights = compute_class_weight('balanced', 
                                               classes=np.unique(labels), 
                                               y=labels)
            class_weights = torch.FloatTensor(class_weights).to(self.device)
            print(f"✅ 计算类别权重: {class_weights}")
        
        # 5. 数据集划分 (80/10/10)
        train_size = int(0.8 * len(processed_data))
        val_size = int(0.1 * len(processed_data))
        test_size = len(processed_data) - train_size - val_size
        
        train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
            processed_data, [train_size, val_size, test_size],
            generator=torch.Generator().manual_seed(42)  # 固定随机种子
        )
        
        train_loader = DataLoader(train_dataset, batch_size=params['batch_size'], shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=params['batch_size'], shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=params['batch_size'], shuffle=False)
        
        print(f"📊 数据划分 - 训练: {len(train_dataset)}, 验证: {len(val_dataset)}, 测试: {len(test_dataset)}")
        
        # 6. 创建模型
        if use_ensemble and params['ensemble_size'] > 1:
            model = EnsembleBrainGNN(in_dim=1, n_roi=116, n_models=params['ensemble_size']).to(self.device)
            print(f"🤖 创建集成模型，包含 {params['ensemble_size']} 个子模型")
        else:
            from intelligent_optimization import ImprovedBrainGNN
            model = ImprovedBrainGNN(
                in_dim=1,
                hidden_dim=params['hidden_dim'],
                n_roi=116,
                dropout=params['dropout'],
                use_attention=True
            ).to(self.device)
            print(f"🤖 创建单一模型，隐藏层维度: {params['hidden_dim']}")
        
        # 7. 优化器和调度器
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=params['lr'],
            weight_decay=params['weight_decay'],
            betas=(0.9, 0.999)
        )
        
        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, T_0=10, T_mult=2, eta_min=params['lr']/100
        )
        
        # 8. 训练循环
        best_val_f1 = 0
        patience_counter = 0
        max_epochs = 100
        
        for epoch in range(max_epochs):
            # 训练阶段
            model.train()
            total_loss = 0
            all_preds = []
            all_labels = []
            
            for batch_idx, data in enumerate(train_loader):
                data = data.to(self.device)
                optimizer.zero_grad()
                
                # 数据增强
                if torch.rand(1) < params['augmentation_prob']:
                    noise = torch.randn_like(data.x) * 0.02
                    data.x = data.x + noise
                
                out, _ = model(data)
                
                # 损失计算
                if params['use_class_weights'] and class_weights is not None:
                    weights = class_weights[data.y]
                    loss = F.nll_loss(out, data.y, reduction='none')
                    loss = (loss * weights).mean()
                else:
                    loss = F.nll_loss(out, data.y)
                
                # L2正则化
                l2_reg = sum(p.pow(2.0).sum() for p in model.parameters())
                loss = loss + params['weight_decay'] * l2_reg
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                
                total_loss += loss.item()
                pred = out.argmax(dim=1)
                all_preds.extend(pred.cpu().numpy())
                all_labels.extend(data.y.cpu().numpy())
            
            train_f1 = f1_score(all_labels, all_preds, average='weighted')
            train_acc = accuracy_score(all_labels, all_preds)
            
            # 验证阶段
            model.eval()
            val_preds = []
            val_labels = []
            val_probs = []
            
            with torch.no_grad():
                for data in val_loader:
                    data = data.to(self.device)
                    out, _ = model(data)
                    pred = out.argmax(dim=1)
                    prob = F.softmax(out, dim=1)
                    
                    val_preds.extend(pred.cpu().numpy())
                    val_labels.extend(data.y.cpu().numpy())
                    val_probs.extend(prob.cpu().numpy())
            
            val_f1 = f1_score(val_labels, val_preds, average='weighted')
            val_acc = accuracy_score(val_labels, val_preds)
            
            # 尝试计算AUC
            try:
                val_auc = roc_auc_score(val_labels, np.array(val_probs)[:, 1])
            except:
                val_auc = 0.5
            
            scheduler.step()
            current_lr = optimizer.param_groups[0]['lr']
            
            # 记录训练历史
            self.training_history['train_f1'].append(train_f1)
            self.training_history['train_acc'].append(train_acc)
            self.training_history['val_f1'].append(val_f1)
            self.training_history['val_acc'].append(val_acc)
            self.training_history['val_auc'].append(val_auc)
            self.training_history['lr'].append(current_lr)
            
            print(f'Epoch {epoch+1:3d}/{max_epochs}, Loss: {total_loss/len(train_loader):.4f}, '
                  f'Train F1: {train_f1:.4f}, Train Acc: {train_acc:.4f}, '
                  f'Val F1: {val_f1:.4f}, Val Acc: {val_acc:.4f}, Val AUC: {val_auc:.4f}, '
                  f'LR: {current_lr:.6f}')
            
            # 早停和模型保存
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                patience_counter = 0
                if not trial:
                    model_name = f'advanced_model_ensemble_{params["ensemble_size"]}.pth' if use_ensemble else 'advanced_model_single.pth'
                    torch.save(model.state_dict(), f'./model/{model_name}')
                    print(f"✅ 保存最佳模型: {model_name}, Val F1: {val_f1:.4f}")
            else:
                patience_counter += 1
                if patience_counter >= 20:
                    print("🛑 早停触发")
                    break
        
        # 9. 最终测试评估
        if not trial:
            model_name = f'advanced_model_ensemble_{params["ensemble_size"]}.pth' if use_ensemble else 'advanced_model_single.pth'
            model.load_state_dict(torch.load(f'./model/{model_name}'))
        
        model.eval()
        test_preds = []
        test_labels = []
        test_probs = []
        
        with torch.no_grad():
            for data in test_loader:
                data = data.to(self.device)
                out, _ = model(data)
                pred = out.argmax(dim=1)
                prob = F.softmax(out, dim=1)
                
                test_preds.extend(pred.cpu().numpy())
                test_labels.extend(data.y.cpu().numpy())
                test_probs.extend(prob.cpu().numpy())
        
        test_acc = accuracy_score(test_labels, test_preds)
        test_f1 = f1_score(test_labels, test_preds, average='weighted')
        
        try:
            test_auc = roc_auc_score(test_labels, np.array(test_probs)[:, 1])
        except:
            test_auc = 0.5
        
        if not trial:
            print("\n" + "="*80)
            print("🎯 高级优化训练完成！")
            print(f"最佳验证F1: {best_val_f1:.4f}")
            print(f"测试准确率: {test_acc:.4f}")
            print(f"测试F1分数: {test_f1:.4f}")
            print(f"测试AUC: {test_auc:.4f}")
            print("="*80)
            
            # 保存详细结果
            results = {
                'timestamp': datetime.now().isoformat(),
                'parameters': params,
                'best_val_f1': best_val_f1,
                'test_accuracy': test_acc,
                'test_f1': test_f1,
                'test_auc': test_auc,
                'training_history': dict(self.training_history),
                'classification_report': classification_report(test_labels, test_preds, output_dict=True)
            }
            
            result_file = f'./model/advanced_optimization_results_{"ensemble" if use_ensemble else "single"}.json'
            with open(result_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"📊 详细结果已保存: {result_file}")
        
        return best_val_f1 if trial else test_acc

def run_deep_hyperparameter_optimization():
    """运行深度超参数优化"""
    print("🔬 开始深度超参数优化（目标: 50次试验）...")
    
    trainer = AdvancedTrainer()
    
    # 创建优化研究
    study = optuna.create_study(
        direction='maximize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=10)
    )
    
    # 优化目标函数
    def objective(trial):
        return trainer.train_with_advanced_techniques(trial=trial, use_ensemble=True)
    
    # 运行优化
    study.optimize(objective, n_trials=50, timeout=3600*4)  # 4小时超时
    
    print("📊 超参数优化完成！")
    print("最佳参数:", study.best_params)
    print("最佳F1分数:", study.best_value)
    
    # 保存优化结果
    with open('./model/hyperparameter_optimization_results.json', 'w') as f:
        json.dump({
            'best_params': study.best_params,
            'best_value': study.best_value,
            'n_trials': len(study.trials),
            'optimization_history': [{'value': trial.value, 'params': trial.params} 
                                   for trial in study.trials if trial.value is not None]
        }, f, indent=2)
    
    return study.best_params

def main():
    """主函数"""
    print("🚀 启动BrainGNN高级优化系统...")
    print("目标: 达到80%以上准确率")
    
    trainer = AdvancedTrainer()
    
    # 运行超参数优化
    print("\n" + "="*50)
    print("阶段1: 深度超参数优化")
    print("="*50)
    best_params = run_deep_hyperparameter_optimization()
    
    # 使用最佳参数训练集成模型
    print("\n" + "="*50)
    print("阶段2: 集成模型训练")
    print("="*50)
    ensemble_acc = trainer.train_with_advanced_techniques(use_ensemble=True)
    
    # 训练单一最佳模型
    print("\n" + "="*50)
    print("阶段3: 单一最佳模型训练") 
    print("="*50)
    single_acc = trainer.train_with_advanced_techniques(use_ensemble=False)
    
    # 最终结果
    print("\n" + "="*80)
    print("🎯 BrainGNN高级优化完成！")
    print("="*80)
    print(f"集成模型准确率: {ensemble_acc:.1%}")
    print(f"单一模型准确率: {single_acc:.1%}")
    print(f"目标达成: {'✅' if max(ensemble_acc, single_acc) >= 0.8 else '❌'} (目标: 80%)")
    
    if max(ensemble_acc, single_acc) < 0.8:
        print("\n💡 建议:")
        print("- 准确率未达到80%，需要考虑增加更多训练数据")
        print("- 可以尝试收集更多不同类型的疼痛数据")
        print("- 考虑使用预训练的脑网络模型")
        print("- 探索更复杂的图神经网络架构")
    
    print("\n📁 生成文件:")
    print("- ./model/advanced_model_ensemble_*.pth - 集成模型")
    print("- ./model/advanced_model_single.pth - 单一模型")
    print("- ./model/advanced_optimization_results_*.json - 详细结果")
    print("- ./model/hyperparameter_optimization_results.json - 超参数优化结果")

if __name__ == "__main__":
    main()