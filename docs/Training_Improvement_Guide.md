# BrainGNN 训练改进指南

## 🎯 问题分析

当前模型存在以下问题：
- **过拟合严重**: 训练准确率83.4% vs 测试准确率52.2%
- **ROI重要性分数区分性差**: 标准差仅0.000571，所有ROI重要性几乎相同
- **模型泛化能力不足**: 无法学到有效的特征表示

## 🚀 改进方案

### 1. 改进的训练脚本 (`improved_training.py`)

#### 主要改进点：

**正则化增强**:
- 权重衰减: `5e-3` → `1e-2`
- 正则化系数: `lamb1-5` 从 `0.1` 增加到 `0.2`
- 新增L2正则化损失
- 梯度裁剪: `grad_clip=1.0`

**学习率优化**:
- 初始学习率: `0.01` → `0.005`
- 使用余弦退火调度器替代步进调度器
- 增加warmup阶段

**数据增强**:
- 批次大小: `100` → `64` (减少过拟合)
- 添加输入噪声增强
- 标签平滑: `label_smoothing=0.1`

**早停机制**:
- 耐心值: `patience=20`
- 防止过拟合

#### 使用方法：

```bash
# 运行改进的训练
python improved_training.py \
    --n_epochs 150 \
    --lr 0.005 \
    --batchSize 64 \
    --weightdecay 1e-2 \
    --lamb1 0.2 \
    --lamb2 0.2 \
    --lamb3 0.2 \
    --lamb4 0.2 \
    --lamb5 0.2 \
    --patience 20 \
    --label_smoothing 0.1 \
    --grad_clip 1.0
```

### 2. 改进的重要性分数提取 (`improved_importance_extraction.py`)

#### 多种提取方法：

**1. 统计方法 (Statistical)**:
- 使用正确预测样本的平均pooling分数
- 置信度加权平均
- 最大激活值

**2. 注意力方法 (Attention)**:
- 基于pooling层的注意力权重
- 使用sigmoid激活后的分数

**3. 梯度方法 (Gradient)**:
- 计算输入特征对损失的梯度
- 使用梯度绝对值作为重要性

**4. 特征重要性 (Feature)**:
- 基于输入特征的方差
- 反映特征的变化程度

**5. 集成方法 (Ensemble)**:
- 组合多种方法的结果
- 标准化后加权平均

#### 使用方法：

```bash
# 提取改进的重要性分数
python improved_importance_extraction.py \
    --model_path ./model_improved/best_model_fold0.pth \
    --save_dir ./importance_scores_improved \
    --batch_size 64
```

## 📊 预期改进效果

### 训练改进：
- **减少过拟合**: 训练和测试准确率差距缩小
- **提高泛化能力**: 更好的特征学习
- **稳定性增强**: 早停机制防止过拟合

### 重要性分数改进：
- **更好的区分性**: 标准差显著增加
- **多种视角**: 不同方法提供互补信息
- **鲁棒性**: 集成方法减少单一方法的偏差

## 🔧 参数调优建议

### 如果仍然过拟合：
```bash
# 进一步增加正则化
python improved_training.py \
    --weightdecay 2e-2 \
    --lamb1 0.3 \
    --lamb2 0.3 \
    --lamb3 0.3 \
    --lamb4 0.3 \
    --lamb5 0.3 \
    --dropout 0.7
```

### 如果欠拟合：
```bash
# 减少正则化
python improved_training.py \
    --weightdecay 5e-3 \
    --lamb1 0.1 \
    --lamb2 0.1 \
    --lamb3 0.1 \
    --lamb4 0.1 \
    --lamb5 0.1 \
    --dropout 0.5
```

### 如果学习率不合适：
```bash
# 调整学习率
python improved_training.py \
    --lr 0.001 \
    --stepsize 50 \
    --gamma 0.8
```

## 📈 监控指标

### 训练过程监控：
1. **损失曲线**: 训练损失和验证损失应该收敛
2. **准确率**: 训练和验证准确率差距应该小于10%
3. **早停**: 观察是否触发早停机制

### 重要性分数质量：
1. **标准差**: 应该显著大于0.001
2. **分布**: 应该呈现明显的区分性
3. **一致性**: 不同方法的结果应该有一定重叠

## 🎯 最佳实践

### 1. 渐进式调优：
- 先运行基础改进版本
- 根据结果逐步调整参数
- 记录每次改进的效果

### 2. 多折验证：
- 使用不同的fold进行训练
- 比较不同fold的结果
- 确保改进的稳定性

### 3. 结果分析：
- 比较改进前后的重要性分数
- 分析不同方法的优缺点
- 选择最适合的方法

## 📁 输出文件

### 训练输出：
- `./model_improved/best_model_fold0.pth`: 最佳模型
- `./model_improved/results_fold0.json`: 训练结果
- `./log_improved/0/`: TensorBoard日志

### 重要性分数输出：
- `./importance_scores_improved/ensemble_importance.npy`: 集成重要性分数
- `./importance_scores_improved/importance_comparison.png`: 比较图
- `./importance_scores_improved/*_stats.pkl`: 各方法统计信息

## 🔍 故障排除

### 常见问题：

1. **内存不足**:
   ```bash
   # 减少批次大小
   --batchSize 32
   ```

2. **训练太慢**:
   ```bash
   # 减少正则化计算
   --lamb1 0.1 --lamb2 0.1
   ```

3. **梯度爆炸**:
   ```bash
   # 调整梯度裁剪
   --grad_clip 0.5
   ```

4. **重要性分数仍然相似**:
   - 检查模型是否真正收敛
   - 尝试不同的重要性提取方法
   - 增加训练轮数

## 📚 参考文献

1. BrainGNN: Graph Neural Network for Brain Network Analysis
2. Attention Is All You Need
3. Gradient-based Feature Attribution Methods
4. Ensemble Methods in Machine Learning

---

**注意**: 这些改进是基于当前问题的针对性解决方案。根据具体的数据集和任务，可能需要进一步调整参数。 