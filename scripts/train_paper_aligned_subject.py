import os
import numpy as np
import torch
import torch.nn.functional as F
from torch.optim import lr_scheduler
from torch_geometric.data import DataLoader, Data
from net.braingnn import Network
from imports.read_abide_stats_parall import read_sigle_data
import random
import argparse
import copy

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

parser = argparse.ArgumentParser()
parser.add_argument('--dataroot', type=str, default='./data/ABIDE_pcp/cpac/filt_noglobal')
parser.add_argument('--save_path', type=str, default='./model_paper_aligned_subject/')
parser.add_argument('--n_epochs', type=int, default=100)
parser.add_argument('--batchSize', type=int, default=400)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--weightdecay', type=float, default=0.005)
parser.add_argument('--stepsize', type=int, default=20)
parser.add_argument('--gamma', type=float, default=0.5)
parser.add_argument('--indim', type=int, default=84)
parser.add_argument('--nroi', type=int, default=84)
parser.add_argument('--k', type=int, default=8)
parser.add_argument('--dim1', type=int, default=16)
parser.add_argument('--dim2', type=int, default=16)
parser.add_argument('--nclass', type=int, default=2)
parser.add_argument('--ratio', type=float, default=0.5)
parser.add_argument('--save_model', type=bool, default=True)
opt = parser.parse_args()

if not os.path.exists(opt.save_path):
    os.makedirs(opt.save_path)

raw_dir = os.path.join(opt.dataroot, 'raw')
all_files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.h5')])
np.random.seed(42)
np.random.shuffle(all_files)
n_subjects = len(all_files)
n_test = n_subjects // 5
n_val = n_subjects // 5
n_train = n_subjects - n_test - n_val
test_files = all_files[:n_test]
val_files = all_files[n_test:n_test+n_val]
train_files = all_files[n_test+n_val:]

# 自动检测输入特征维度和ROI数
sample_edge_att, sample_edge_index, sample_att, sample_label, sample_num_nodes = read_sigle_data(raw_dir, all_files[0])
indim = sample_att.shape[1]
nroi = sample_att.shape[0]
print(f"自动检测到输入特征维度 indim={indim}, ROI数 nroi={nroi}")

def load_graphs(file_list):
    data_list = []
    for fname in file_list:
        edge_att, edge_index, att, label, num_nodes = read_sigle_data(raw_dir, fname)
        pos = torch.eye(num_nodes)
        data = Data(x=torch.from_numpy(att).float(),
                    edge_index=torch.from_numpy(edge_index).long(),
                    y=torch.tensor(label).long(),
                    edge_attr=torch.from_numpy(edge_att).float(),
                    pos=pos.float())
        data_list.append(data)
    return data_list

train_data = load_graphs(train_files)
val_data = load_graphs(val_files)
test_data = load_graphs(test_files)

train_loader = DataLoader(train_data, batch_size=opt.batchSize, shuffle=True)
val_loader = DataLoader(val_data, batch_size=opt.batchSize, shuffle=False)
test_loader = DataLoader(test_data, batch_size=opt.batchSize, shuffle=False)

model = Network(indim, opt.ratio, opt.nclass, k=opt.k, R=nroi).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr, weight_decay=opt.weightdecay)
scheduler = lr_scheduler.StepLR(optimizer, step_size=opt.stepsize, gamma=opt.gamma)

def train(epoch):
    model.train()
    scheduler.step()
    loss_all = 0
    for data in train_loader:
        data = data.to(device)
        optimizer.zero_grad()
        output, w1, w2, s1, s2 = model(data.x, data.edge_index, data.batch, data.edge_attr, data.pos)
        loss = F.nll_loss(output, data.y)
        loss.backward()
        optimizer.step()
        loss_all += loss.item() * data.num_graphs
    return loss_all / len(train_data)

def test_acc(loader):
    model.eval()
    correct = 0
    for data in loader:
        data = data.to(device)
        outputs = model(data.x, data.edge_index, data.batch, data.edge_attr, data.pos)
        pred = outputs[0].max(dim=1)[1]
        correct += pred.eq(data.y).sum().item()
    return correct / len(loader.dataset)

best_model_wts = copy.deepcopy(model.state_dict())
best_acc = 0
for epoch in range(opt.n_epochs):
    tr_loss = train(epoch)
    tr_acc = test_acc(train_loader)
    val_acc = test_acc(val_loader)
    print(f"Epoch {epoch:03d} | Train Loss: {tr_loss:.4f} | Train Acc: {tr_acc:.4f} | Val Acc: {val_acc:.4f}")
    if val_acc > best_acc:
        best_acc = val_acc
        best_model_wts = copy.deepcopy(model.state_dict())
        if opt.save_model:
            torch.save(best_model_wts, os.path.join(opt.save_path, 'best_model.pth'))

model.load_state_dict(best_model_wts)
test_accu = test_acc(test_loader)
print(f"Test Accuracy: {test_accu:.4f}") 

# === 自动化后处理：提取重要性分数与可视化 ===
import os

# 路径参数可根据实际情况调整
model_path = os.path.join(opt.save_path, 'best_model.pth')
data_path = opt.dataroot
save_dir = './results/importance_subject'  # 可自定义输出目录
score_path = os.path.join(save_dir, 'ensemble_importance.npy')

# 1. 自动提取重要性分数
os.system(
    f"python scripts/improved_importance_extraction.py "
    f"--model_path {model_path} "
    f"--data_path {data_path} "
    f"--save_dir {save_dir} "
)

# 2. 自动可视化
os.system(
    f"python scripts/brain_importance_visualization.py "
    f"--score_path {score_path} "
)

print("\n✅ 训练、重要性分数提取与可视化全部完成！请查看 results/importance_subject 和图片输出目录。\n") 