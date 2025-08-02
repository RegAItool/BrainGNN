import subprocess
import argparse

parser = argparse.ArgumentParser(description='一键多任务BrainGNN全流程')
parser.add_argument('--skip-train', action='store_true', help='只做重要性提取和可视化，跳过训练')
parser.add_argument('--device', type=str, default='cpu', help='推理/提取时用的设备(cpu/cuda)')
args = parser.parse_args()

if not args.skip_train:
    # 1. 训练模型
    print("=== Step 1: 训练模型 ===")
    subprocess.run(['python', '03-main.py'], check=True)
else:
    print("=== 跳过训练，直接进行重要性提取和可视化 ===")

# 2. 提取多任务ROI重要性
print("=== Step 2: 提取多任务ROI重要性 ===")
subprocess.run(['python', 'scripts/improved_importance_extraction.py', '--device', args.device, '--model_path', './model/best_pain_model.pth'], check=True)

# 3. 可视化脑区重要性
print("=== Step 3: 可视化脑区重要性 ===")
subprocess.run(['python', 'scripts/brain_importance_visualization.py'], check=True)

print("=== 全流程完成！请在 results/ 目录下查看多任务脑区显著性可视化结果 ===") 