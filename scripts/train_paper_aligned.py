import os
import numpy as np
import torch
import torch.nn.functional as F
from torch.optim import lr_scheduler
from tensorboardX import SummaryWriter
from imports.ABIDEDataset import ABIDEDataset
from torch_geometric.data import DataLoader
from net.braingnn import Network
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
parser.add_argument('--save_path', type=str, default='./model_paper_aligned/')
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

dataset = ABIDEDataset(opt.dataroot, 'ABIDE')
dataset.data.y = dataset.data.y.squeeze()
dataset.data.x[dataset.data.x == float('inf')] = 0

subjects = np.unique(dataset.subject_list)
np.random.shuffle(subjects)
n_subjects = len(subjects)
n_test = n_subjects // 5
n_val = n_subjects // 5
n_train = n_subjects - n_test - n_val
test_subjects = subjects[:n_test]
val_subjects = subjects[n_test:n_test+n_val]
train_subjects = subjects[n_test+n_val:]

def get_indices(subjects_set):
    return [i for i, s in enumerate(dataset.subject_list) if s in subjects_set]

train_index = get_indices(train_subjects)
val_index = get_indices(val_subjects)
test_index = get_indices(test_subjects)

train_dataset = dataset[train_index]
val_dataset = dataset[val_index]
test_dataset = dataset[test_index]

train_loader = DataLoader(train_dataset, batch_size=opt.batchSize, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=opt.batchSize, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=opt.batchSize, shuffle=False)

model = Network(opt.indim, opt.ratio, opt.nclass, k=opt.k, R=opt.nroi).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr, weight_decay=opt.weightdecay)
scheduler = lr_scheduler.StepLR(optimizer, step_size=opt.stepsize, gamma=opt.gamma)
writer = SummaryWriter(os.path.join('./log_paper_aligned'))

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
    return loss_all / len(train_dataset)

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