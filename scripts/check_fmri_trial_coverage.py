import os
import pandas as pd
import nibabel as nib

DATASET_DIR = 'data/pain_data/ds005413'
TR = 2.0  # 默认TR=2s
min_required_length = 3  # 与生成脚本一致

def check_fmri_and_trials():
    for sub in sorted(os.listdir(DATASET_DIR)):
        if not sub.startswith('sub-'):
            continue
        sub_dir = os.path.join(DATASET_DIR, sub, 'func')
        if not os.path.isdir(sub_dir):
            continue
        for fname in os.listdir(sub_dir):
            if fname.endswith('_bold.nii.gz'):
                fmri_path = os.path.join(sub_dir, fname)
                try:
                    img = nib.load(fmri_path)
                    n_vols = img.shape[3]
                except Exception as e:
                    print(f"❌ Failed to load {fmri_path}: {e}")
                    continue
                base = fname.replace('_bold.nii.gz', '')
                events_path = os.path.join(sub_dir, base + '_events.tsv')
                if not os.path.exists(events_path):
                    print(f'No events file for {fmri_path}')
                    continue
                try:
                    events = pd.read_csv(events_path, sep='\t')
                except Exception as e:
                    print(f"❌ Failed to read {events_path}: {e}")
                    continue
                print(f"\n{fmri_path}: n_vols={n_vols}")
                for idx, row in events.iterrows():
                    onset = float(row['onset'])
                    duration = float(row['duration'])
                    start_vol = int(onset // TR)
                    end_vol = int((onset + duration) // TR)
                    seg_len = end_vol - start_vol
                    out_of_bounds = end_vol > n_vols or start_vol >= n_vols
                    print(f"  trial {idx}: onset={onset}, duration={duration}, start_vol={start_vol}, end_vol={end_vol}, seg_len={seg_len}, out_of_bounds={out_of_bounds}")
                    if seg_len < min_required_length:
                        print(f"    ⚠️ Too short segment (length={seg_len}, min_required_length={min_required_length})")
                    if out_of_bounds:
                        print(f"    ❌ Out of bounds! fMRI n_vols={n_vols}")

if __name__ == '__main__':
    check_fmri_and_trials() 