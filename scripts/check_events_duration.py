import os
import pandas as pd

DATASET_DIR = 'data/pain_data/ds005413'
min_durations = []
all_durations = []
short_trial_count = 0
short_trial_threshold = 2  # 你可以调整这个阈值

total_trials = 0
for sub in sorted(os.listdir(DATASET_DIR)):
    if not sub.startswith('sub-'):
        continue
    sub_dir = os.path.join(DATASET_DIR, sub, 'func')
    if not os.path.isdir(sub_dir):
        continue
    for fname in os.listdir(sub_dir):
        if fname.endswith('_events.tsv'):
            events_path = os.path.join(sub_dir, fname)
            try:
                events = pd.read_csv(events_path, sep='\t')
                durations = events['duration'].astype(float).values
                all_durations.extend(durations)
                min_durations.append(durations.min())
                short_count = (durations < short_trial_threshold).sum()
                short_trial_count += short_count
                total_trials += len(durations)
                print(f"{events_path}: min={durations.min()}, max={durations.max()}, mean={durations.mean():.2f}, short(<{short_trial_threshold})={short_count}/{len(durations)}")
            except Exception as e:
                print(f"Failed to read {events_path}: {e}")

if all_durations:
    print("\n=== 全部 trial duration 统计 ===")
    print(f"总trial数: {total_trials}")
    print(f"最小: {min(all_durations)}，最大: {max(all_durations)}，均值: {sum(all_durations)/len(all_durations):.2f}")
    print(f"短trial(<{short_trial_threshold})数量: {short_trial_count}，占比: {short_trial_count/total_trials:.2%}")
else:
    print("未找到任何有效的events.tsv文件或duration列！") 