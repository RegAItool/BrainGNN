import os
import shutil

# 源目录列表
source_dirs = [
    'data/pain_data/ds000140/graphs',
    'data/pain_data/ds003836/graphs',
    'data/pain_data/ds005413/graphs',
]
# 目标目录
target_dir = 'data/pain_data/all_graphs'
os.makedirs(target_dir, exist_ok=True)

count = 0
for src in source_dirs:
    if not os.path.exists(src):
        print(f"Source dir not found: {src}")
        continue
    for fname in os.listdir(src):
        if fname.endswith('.pt'):
            src_path = os.path.join(src, fname)
            dst_path = os.path.join(target_dir, fname)
            if os.path.exists(dst_path):
                print(f"Skip existing: {dst_path}")
                continue
            shutil.copy2(src_path, dst_path)
            count += 1
            if count % 1000 == 0:
                print(f"Copied {count} files...")
print(f"合并完成，共复制 {count} 个 .pt 文件到 {target_dir}") 