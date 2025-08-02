import numpy as np

# 1. 生成100个节点的空间坐标（-50~50mm均匀分布）
np.random.seed(42)
coords = np.random.uniform(-50, 50, size=(100, 3))

# 2. 读取重要性分数
importance = np.load('importance_scores/roi_importance.npy')  # shape (100,)

# 3. 节点大小（可全部设为10）
size = np.ones(100) * 10

# 4. 生成node文件（x, y, z, size, importance）
node_data = np.column_stack([coords, size, importance])
np.savetxt('brainnet_nodes.node', node_data, fmt='%.3f\t%.3f\t%.3f\t%.3f\t%.6f')
print('✅ 已生成 brainnet_nodes.node (100 nodes)')

# 5. 生成edge文件（100x100单位矩阵，主对角为0）
edge_data = np.eye(100)
np.fill_diagonal(edge_data, 0)
np.savetxt('brainnet_edges.edge', edge_data, fmt='%.3f', delimiter='\t')
print('✅ 已生成 brainnet_edges.edge (100x100)')

# 6. 检查
print('节点文件 shape:', node_data.shape)
print('边文件 shape:', edge_data.shape) 