#!/usr/bin/env python3
"""
快速训练脚本
"""

import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from sklearn.metrics import accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from imports.PainGraphDataset import PainGraphDataset
from intelligent_optimization import ImprovedBrainGNN

def main():
    print('🚀 启动快速优化训练...')
    
    # 加载数据
    dataset = PainGraphDataset('./data/pain_data/all_graphs/')
    filtered_data = []
    for i in range(min(2000, len(dataset))):  # 限制样本数量
        try:
            data = dataset[i]
            if data.x.shape == (116, 1):
                data.y = data.y.long()
                filtered_data.append(data)
        except:
            continue
    
    print(f'✅ 加载 {len(filtered_data)} 个样本')
    
    # 数据预处理和平衡
    labels = [data.y.item() for data in filtered_data]
    
    # 重复少数类样本
    minority_indices = [i for i, label in enumerate(labels) if label == 1]
    majority_indices = [i for i, label in enumerate(labels) if label == 0]
    
    # 平衡数据集
    balanced_data = []
    balanced_data.extend([filtered_data[i] for i in majority_indices])
    balanced_data.extend([filtered_data[i] for i in minority_indices * 4])  # 重复4次
    
    print(f'✅ 平衡后样本数: {len(balanced_data)}')
    
    # 数据划分
    torch.manual_seed(42)
    train_size = int(0.8 * len(balanced_data))
    val_size = int(0.1 * len(balanced_data))
    test_size = len(balanced_data) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        balanced_data, [train_size, val_size, test_size]
    )
    
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'🔧 使用设备: {device}')
    
    # 创建模型
    model = ImprovedBrainGNN(in_dim=1, hidden_dim=128, n_roi=116, dropout=0.3).to(device)
    
    # 优化器
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
    
    # 训练
    best_val_acc = 0
    for epoch in range(60):
        model.train()
        total_loss = 0
        train_preds = []
        train_labels = []
        
        for data in train_loader:
            data = data.to(device)
            optimizer.zero_grad()
            
            out, _ = model(data)
            loss = F.nll_loss(out, data.y)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
            pred = out.argmax(dim=1)
            train_preds.extend(pred.cpu().numpy())
            train_labels.extend(data.y.cpu().numpy())
        
        train_acc = accuracy_score(train_labels, train_preds)
        
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
        
        val_acc = accuracy_score(val_labels, val_preds)
        scheduler.step()
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), './model/quick_optimized_model.pth')
        
        if epoch % 10 == 0:
            print(f'Epoch {epoch:3d}: Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}')
    
    # 测试
    model.load_state_dict(torch.load('./model/quick_optimized_model.pth'))
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
    
    print(f'\n' + '='*50)
    print(f'🎯 快速优化结果:')
    print(f'测试准确率: {test_acc:.4f} ({test_acc:.1%})')
    print(f'测试F1分数: {test_f1:.4f}')
    print(f'目标达成: {"✅" if test_acc >= 0.8 else "❌"} (目标: 80%)')
    print('='*50)

if __name__ == "__main__":
    main()