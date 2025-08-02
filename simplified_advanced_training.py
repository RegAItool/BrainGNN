#!/usr/bin/env python3
"""
简化的高级训练系统
专注于达到80%准确率的核心优化
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
import numpy as np
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from imports.PainGraphDataset import PainGraphDataset
from intelligent_optimization import ImprovedBrainGNN

class OptimizedTrainer:
    """优化训练器"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🔧 使用设备: {self.device}")
    
    def load_and_preprocess_data(self):
        """加载和预处理全部数据"""
        print("📊 加载全部数据并进行高级预处理...")
        
        # 加载数据集
        dataset = PainGraphDataset('./data/pain_data/all_graphs/')
        
        # 过滤有效数据
        valid_data = []
        for i in range(len(dataset)):
            try:
                data = dataset[i]
                if data.x.shape == (116, 1):
                    data.y = data.y.long()
                    valid_data.append(data)
            except:
                continue
        
        print(f"✅ 成功加载 {len(valid_data)} 个有效样本")
        
        # 高级数据预处理
        processed_data = []
        all_features = []
        labels = []
        
        for data in valid_data:
            # 异常值处理
            x = data.x.clone()
            mean = x.mean()
            std = x.std()
            x = torch.clamp(x, mean - 3*std, mean + 3*std)
            
            # 归一化
            x = (x - x.mean()) / (x.std() + 1e-8)
            
            data.x = x
            processed_data.append(data)
            
            # 收集特征用于类别权重计算
            all_features.append(x.flatten().numpy())
            labels.append(data.y.item())
        
        # 计算类别权重
        class_weights = compute_class_weight('balanced', 
                                           classes=np.unique(labels), 
                                           y=labels)
        class_weights = torch.FloatTensor(class_weights).to(self.device)
        
        print(f"✅ 数据预处理完成")
        print(f"✅ 类别分布: {np.bincount(labels)}")
        print(f"✅ 类别权重: {class_weights}")
        
        return processed_data, class_weights
    
    def create_ensemble_models(self, n_models=5):
        """创建集成模型"""
        models = []
        
        configs = [
            {'hidden_dim': 128, 'dropout': 0.4},
            {'hidden_dim': 96, 'dropout': 0.35},
            {'hidden_dim': 160, 'dropout': 0.45},
            {'hidden_dim': 80, 'dropout': 0.3},
            {'hidden_dim': 192, 'dropout': 0.5}
        ]
        
        for i in range(n_models):
            config = configs[i % len(configs)]
            model = ImprovedBrainGNN(
                in_dim=1,
                hidden_dim=config['hidden_dim'],
                n_roi=116,
                dropout=config['dropout'],
                use_attention=True
            ).to(self.device)
            models.append(model)
        
        print(f"🤖 创建 {n_models} 个集成模型")
        return models
    
    def train_single_model(self, model, train_loader, val_loader, class_weights, model_id=0):
        """训练单个模型"""
        print(f"🚀 开始训练模型 {model_id+1}...")
        
        # 优化器配置
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=0.001,
            weight_decay=1e-4,
            betas=(0.9, 0.999)
        )
        
        # 学习率调度器
        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, T_0=15, T_mult=2, eta_min=1e-6
        )
        
        best_val_f1 = 0
        patience_counter = 0
        max_epochs = 150
        
        for epoch in range(max_epochs):
            # 训练阶段
            model.train()
            total_loss = 0
            all_preds = []
            all_labels = []
            
            for data in train_loader:
                data = data.to(self.device)
                optimizer.zero_grad()
                
                # 数据增强
                if torch.rand(1) < 0.2:
                    noise = torch.randn_like(data.x) * 0.01
                    data.x = data.x + noise
                
                out, _ = model(data)
                
                # 加权损失
                if class_weights is not None:
                    weights = class_weights[data.y]
                    loss = F.nll_loss(out, data.y, reduction='none')
                    loss = (loss * weights).mean()
                else:
                    loss = F.nll_loss(out, data.y)
                
                # 标签平滑
                smoothed_loss = loss * 0.9 + 0.1 * (-out.mean())
                
                smoothed_loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                
                total_loss += smoothed_loss.item()
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
            
            scheduler.step()
            
            if epoch % 10 == 0:
                print(f'  Epoch {epoch:3d}: Train F1: {train_f1:.4f}, Val F1: {val_f1:.4f}, Val Acc: {val_acc:.4f}')
            
            # 早停
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                patience_counter = 0
                torch.save(model.state_dict(), f'./model/ensemble_model_{model_id}.pth')
            else:
                patience_counter += 1
                if patience_counter >= 30:
                    print(f"  ⏹️ 模型 {model_id+1} 早停，最佳验证F1: {best_val_f1:.4f}")
                    break
        
        return best_val_f1
    
    def ensemble_predict(self, models, test_loader):
        """集成预测"""
        print("🔮 执行集成预测...")
        
        all_predictions = []
        test_labels = []
        
        # 收集所有模型的预测
        for model_id, model in enumerate(models):
            model.load_state_dict(torch.load(f'./model/ensemble_model_{model_id}.pth'))
            model.eval()
            
            model_preds = []
            model_probs = []
            
            with torch.no_grad():
                for data in test_loader:
                    data = data.to(self.device)
                    out, _ = model(data)
                    pred = out.argmax(dim=1)
                    prob = F.softmax(out, dim=1)
                    
                    model_preds.extend(pred.cpu().numpy())
                    model_probs.extend(prob.cpu().numpy())
                    
                    if model_id == 0:  # 只需要收集一次标签
                        test_labels.extend(data.y.cpu().numpy())
            
            all_predictions.append(np.array(model_probs))
        
        # 平均概率预测
        avg_probs = np.mean(all_predictions, axis=0)
        ensemble_preds = np.argmax(avg_probs, axis=1)
        
        # 计算性能指标
        ensemble_acc = accuracy_score(test_labels, ensemble_preds)
        ensemble_f1 = f1_score(test_labels, ensemble_preds, average='weighted')
        
        try:
            ensemble_auc = roc_auc_score(test_labels, avg_probs[:, 1])
        except:
            ensemble_auc = 0.5
        
        return ensemble_acc, ensemble_f1, ensemble_auc, test_labels, ensemble_preds
    
    def run_advanced_training(self):
        """运行高级训练流程"""
        print("🎯 开始高级训练流程，目标: 80%准确率")
        
        # 1. 数据加载和预处理
        data, class_weights = self.load_and_preprocess_data()
        
        # 2. 数据划分 (80/10/10)
        train_size = int(0.8 * len(data))
        val_size = int(0.1 * len(data))
        test_size = len(data) - train_size - val_size
        
        # 固定随机种子确保可重现性
        torch.manual_seed(42)
        train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
            data, [train_size, val_size, test_size]
        )
        
        # 创建数据加载器
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        print(f"📊 数据划分 - 训练: {len(train_dataset)}, 验证: {len(val_dataset)}, 测试: {len(test_dataset)}")
        
        # 3. 创建和训练集成模型
        models = self.create_ensemble_models(n_models=5)
        
        val_f1_scores = []
        for i, model in enumerate(models):
            val_f1 = self.train_single_model(model, train_loader, val_loader, class_weights, i)
            val_f1_scores.append(val_f1)
        
        print(f"✅ 所有模型训练完成，验证F1分数: {val_f1_scores}")
        print(f"✅ 平均验证F1: {np.mean(val_f1_scores):.4f}")
        
        # 4. 集成预测
        ensemble_acc, ensemble_f1, ensemble_auc, test_labels, ensemble_preds = self.ensemble_predict(models, test_loader)
        
        # 5. 结果报告
        print("\n" + "="*60)
        print("🎯 高级训练完成！")
        print("="*60)
        print(f"集成模型测试准确率: {ensemble_acc:.4f} ({ensemble_acc:.1%})")
        print(f"集成模型测试F1分数: {ensemble_f1:.4f}")
        print(f"集成模型测试AUC: {ensemble_auc:.4f}")
        print(f"目标达成: {'✅' if ensemble_acc >= 0.8 else '❌'} (目标: 80%)")
        
        # 详细分类报告
        print("\\n📊 详细分类报告:")
        print(classification_report(test_labels, ensemble_preds))
        
        # 保存结果
        results = {
            'timestamp': datetime.now().isoformat(),
            'ensemble_accuracy': float(ensemble_acc),
            'ensemble_f1': float(ensemble_f1),
            'ensemble_auc': float(ensemble_auc),
            'individual_val_f1_scores': [float(f1) for f1 in val_f1_scores],
            'average_val_f1': float(np.mean(val_f1_scores)),
            'classification_report': classification_report(test_labels, ensemble_preds, output_dict=True),
            'target_achieved': ensemble_acc >= 0.8
        }
        
        with open('./model/advanced_training_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\\n📁 结果已保存: ./model/advanced_training_results.json")
        
        if ensemble_acc < 0.8:
            print("\\n💡 改进建议:")
            print("- 当前准确率未达到80%，可能需要:")
            print("  1. 增加更多训练数据")
            print("  2. 尝试更复杂的模型架构")
            print("  3. 使用预训练的脑网络特征")
            print("  4. 收集更高质量的疼痛数据")
        
        return ensemble_acc

def main():
    """主函数"""
    print("🚀 启动BrainGNN高级训练系统")
    print("🎯 目标: 达到80%以上准确率")
    
    trainer = OptimizedTrainer()
    accuracy = trainer.run_advanced_training()
    
    print(f"\\n✨ 最终准确率: {accuracy:.1%}")

if __name__ == "__main__":
    main()