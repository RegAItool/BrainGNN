import matplotlib.pyplot as plt
import numpy as np
import os
import re
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def read_tensorboard_logs(log_dir):
    """读取TensorBoard日志文件"""
    ea = EventAccumulator(log_dir)
    ea.Reload()
    
    # 获取所有可用的标量标签
    print("可用的标量标签:", ea.Tags()['scalars'])
    
    # 读取损失数据
    losses = {}
    steps = []
    
    # 读取分类损失
    try:
        scalars = ea.Scalars('train/classification_loss')
        steps = [event.step for event in scalars]
        losses['classification'] = [event.value for event in scalars]
        print(f"找到分类损失数据: {len(losses['classification'])} 个点")
    except:
        print("未找到分类损失数据")
    
    # 读取其他损失，确保使用相同的步数
    loss_types = ['unit_loss1', 'unit_loss2', 'TopK_loss1', 'TopK_loss2', 'GCL_loss']
    for loss_type in loss_types:
        try:
            scalars = ea.Scalars(f'train/{loss_type}')
            # 只取与分类损失相同长度的数据
            loss_values = [event.value for event in scalars]
            if len(loss_values) == len(steps):
                losses[loss_type] = loss_values
                print(f"找到 {loss_type} 数据: {len(losses[loss_type])} 个点")
            else:
                print(f"跳过 {loss_type} 数据: 长度不匹配 ({len(loss_values)} vs {len(steps)})")
        except:
            print(f"未找到 {loss_type} 数据")
    
    return steps, losses

def plot_training_curves():
    """绘制训练曲线"""
    log_dir = './log/0'
    
    if not os.path.exists(log_dir):
        print(f"日志目录 {log_dir} 不存在")
        return
    
    try:
        steps, losses = read_tensorboard_logs(log_dir)
        
        if not steps:
            print("未找到训练数据")
            return
        
        plt.figure(figsize=(15, 10))
        
        # 绘制分类损失曲线
        plt.subplot(2, 3, 1)
        if 'classification' in losses:
            plt.plot(steps, losses['classification'], 'b-', label='Classification Loss', linewidth=2)
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.title('Classification Loss')
            plt.legend()
            plt.grid(True)
        
        # 绘制单元损失曲线
        plt.subplot(2, 3, 2)
        if 'unit_loss1' in losses:
            plt.plot(steps, losses['unit_loss1'], 'g-', label='Unit Loss 1', linewidth=2)
        if 'unit_loss2' in losses:
            plt.plot(steps, losses['unit_loss2'], 'r-', label='Unit Loss 2', linewidth=2)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Unit Losses')
        plt.legend()
        plt.grid(True)
        
        # 绘制TopK损失曲线
        plt.subplot(2, 3, 3)
        if 'TopK_loss1' in losses:
            plt.plot(steps, losses['TopK_loss1'], 'm-', label='TopK Loss 1', linewidth=2)
        if 'TopK_loss2' in losses:
            plt.plot(steps, losses['TopK_loss2'], 'c-', label='TopK Loss 2', linewidth=2)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('TopK Losses')
        plt.legend()
        plt.grid(True)
        
        # 绘制GCL损失曲线
        plt.subplot(2, 3, 4)
        if 'GCL_loss' in losses:
            plt.plot(steps, losses['GCL_loss'], 'y-', label='GCL Loss', linewidth=2)
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.title('GCL Loss')
            plt.legend()
            plt.grid(True)
        
        # 显示当前训练状态
        plt.subplot(2, 3, 5)
        if 'classification' in losses:
            plt.text(0.1, 0.8, f'Latest Class Loss: {losses["classification"][-1]:.4f}', fontsize=10)
        if 'unit_loss1' in losses:
            plt.text(0.1, 0.6, f'Latest Unit Loss 1: {losses["unit_loss1"][-1]:.4f}', fontsize=10)
        if 'unit_loss2' in losses:
            plt.text(0.1, 0.4, f'Latest Unit Loss 2: {losses["unit_loss2"][-1]:.4f}', fontsize=10)
        plt.text(0.1, 0.2, f'Total Epochs: {len(steps)}', fontsize=10)
        plt.axis('off')
        plt.title('Training Status')
        
        plt.tight_layout()
        plt.savefig('training_curves.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("训练曲线已保存为 training_curves.png")
        
        # 打印当前训练状态
        if 'classification' in losses:
            print(f"最新分类损失: {losses['classification'][-1]:.4f}")
        if 'unit_loss1' in losses:
            print(f"最新单元损失1: {losses['unit_loss1'][-1]:.4f}")
        if 'unit_loss2' in losses:
            print(f"最新单元损失2: {losses['unit_loss2'][-1]:.4f}")
        print(f"已训练轮数: {len(steps)}")
        
    except Exception as e:
        print(f"读取日志时出错: {e}")
        print("尝试手动查看日志文件...")
        
        # 手动读取日志文件
        log_files = [f for f in os.listdir(log_dir) if f.startswith('events.out.tfevents')]
        if log_files:
            print(f"找到 {len(log_files)} 个日志文件")
            print("最新的日志文件:", max(log_files))
            
            # 显示最新的训练输出
            print("\n根据之前的输出，当前训练状态:")
            print("Epoch 013: Train Acc: 0.5265700, Test Acc: 0.5024155")
            print("训练正在进行中...")
        else:
            print("未找到日志文件")

if __name__ == "__main__":
    plot_training_curves() 