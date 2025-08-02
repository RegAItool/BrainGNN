import torch
import matplotlib.pyplot as plt
from torch_geometric.utils import to_networkx
from torch_geometric.data import Data as PyGData
import networkx as nx

PT_PATH = 'data/pain_data/ds000140/graphs/sub-01_graph.pt'
IMG_PATH = 'results/sub-01_graph_first20.png'

data = torch.load(PT_PATH)
num_nodes = 20
mask = (data.edge_index[0] < num_nodes) & (data.edge_index[1] < num_nodes)
sub_edge_index = data.edge_index[:, mask]
sub_edge_attr = data.edge_attr[mask]
sub_x = data.x[:num_nodes]
sub_data = PyGData(x=sub_x, edge_index=sub_edge_index, edge_attr=sub_edge_attr, y=data.y)

G = to_networkx(sub_data, edge_attrs=['edge_attr'], to_undirected=True)
plt.figure(figsize=(6,6))
nx.draw(G, node_size=100, alpha=0.8, with_labels=True)
plt.title('Subgraph of sub-01 (first 20 nodes)')
plt.savefig(IMG_PATH)
plt.close()
print(f'子图已保存为 {IMG_PATH}') 