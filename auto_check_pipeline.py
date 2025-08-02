import torch
import os
import numpy as np
import json
from glob import glob

# --- Configuration ---
# Adjust these paths if they are different in your setup
DATA_ROOT = './data/pain_data/all_graphs/'
MODEL_PATH = './model/best_pain_model.pth'
RESULTS_DIR = './results'
ROI_NAME_MAP_PATH = './aal116_roi_id2name.json'

# Expected parameters from the trained model
EXPECTED_INDIM = 116
EXPECTED_NROI = 116

print("="*60)
print("🚀  Starting Automated Pipeline Consistency Check...")
print("="*60)

# --- 1. Data Shape Check ---
print("\n--- 1. Checking Data Shapes ---")
if not os.path.exists(DATA_ROOT):
    print(f"❌ ERROR: Data directory not found at: {DATA_ROOT}")
else:
    pt_files = glob(os.path.join(DATA_ROOT, '*.pt'))
    if not pt_files:
        print(f"❌ ERROR: No .pt files found in {DATA_ROOT}")
    else:
        print(f"✅ Found {len(pt_files)} graph files in {DATA_ROOT}.")
        # Check the shape of the first 20 valid files
        shapes_found = {}
        files_to_check = pt_files[:20] # Check a sample of files
        print(f"🔬 Checking first {len(files_to_check)} files for feature dimensions...")
        for f in files_to_check:
            try:
                data = torch.load(f)
                shape_str = str(data.x.shape)
                if shape_str not in shapes_found:
                    shapes_found[shape_str] = 0
                shapes_found[shape_str] += 1
            except Exception as e:
                print(f"⚠️  Warning: Could not load or check file {os.path.basename(f)}: {e}")

        if not shapes_found:
            print("❌ ERROR: Could not read shapes from any sample data files.")
        else:
            print("📊 Shape summary from sample files:")
            for shape, count in shapes_found.items():
                print(f"   - Shape {shape}: Found {count} times")
            # Simple majority vote for the most common shape
            most_common_shape_str = max(shapes_found, key=shapes_found.get)
            print(f"👉 Most common data shape: {most_common_shape_str}")
            # Example shape: "torch.Size([116, 1])"
            parts = most_common_shape_str.replace('torch.Size([', '').replace('])', '').split(', ')
            n_roi = int(parts[0])
            in_dim = int(parts[1])
            if n_roi != EXPECTED_NROI or in_dim == EXPECTED_INDIM:
                 print(f"✅ Most common data has n_roi={n_roi}, in_dim={in_dim}.")
            else:
                 print(f"🔥 MISMATCH: Most common data has n_roi={n_roi}, in_dim={in_dim}.")
                 print(f"             But the trained model expects data with in_dim={EXPECTED_INDIM}.")


# --- 2. Model Weights Check ---
print("\n--- 2. Checking Model Weights ---")
if not os.path.exists(MODEL_PATH):
    print(f"❌ ERROR: Model file not found at: {MODEL_PATH}")
else:
    try:
        checkpoint = torch.load(MODEL_PATH, map_location='cpu')
        # Check for both model_state_dict and direct weights
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
            print("✅ Model checkpoint loaded successfully (from 'model_state_dict' key).")
        else:
            state_dict = checkpoint
            print("✅ Model weights loaded successfully (direct state_dict).")

        # Infer indim from a known layer, e.g., 'encoder.n1.0.weight'
        # Shape is [k, indim]
        weight_key = 'encoder.n1.0.weight'
        if weight_key in state_dict:
            model_indim = state_dict[weight_key].shape[1]
            print(f"🔬 Inferred model input dimension (indim) from '{weight_key}': {model_indim}")
            if model_indim != EXPECTED_INDIM:
                print(f"🔥 MISMATCH: Model expects indim={model_indim}, but configuration expects {EXPECTED_INDIM}.")
            else:
                print(f"✅ Model indim ({model_indim}) matches expected value ({EXPECTED_INDIM}).")
        else:
            print(f"❌ ERROR: Cannot find key '{weight_key}' in model state_dict to infer indim.")

        # Infer nroi from another layer if possible, e.g. 'encoder.conv1.nn.0.weight' in some versions
        # This is trickier. We will rely on EXPECTED_NROI for now.
        print(f"ℹ️  Assuming number of ROIs (n_roi) is {EXPECTED_NROI} based on AAL116 atlas.")

    except Exception as e:
        print(f"❌ ERROR: Could not load or inspect model file {MODEL_PATH}: {e}")

# --- 3. Importance Extraction Output Check ---
print("\n--- 3. Checking Importance Extraction Outputs ---")
if not os.path.exists(RESULTS_DIR):
    print(f"⚠️  Warning: Results directory '{RESULTS_DIR}' not found. It seems the pipeline hasn't been run yet.")
else:
    print(f"✅ Found results directory: {RESULTS_DIR}")
    # The script saves results in subdirectories named after tasks, e.g., 'task_1'
    task_dirs = [d for d in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, d)) and 'task' in d]
    if not task_dirs:
        print("❌ ERROR: No task-specific result directories (e.g., 'results/task_1/') found.")
        print("     This means the main loop in the extraction script did not run or save any outputs.")
    else:
        print(f"✅ Found {len(task_dirs)} task result directories: {task_dirs}")
        for task_dir_name in sorted(task_dirs):
            task_path = os.path.join(RESULTS_DIR, task_dir_name)
            score_file = os.path.join(task_path, f'ensemble_importance_{task_dir_name}.npy')
            csv_file = os.path.join(task_path, f'roi_importance_{task_dir_name}.csv')

            print(f"\n--- Checking {task_dir_name} ---")
            # Check for .npy file
            if os.path.exists(score_file):
                try:
                    scores = np.load(score_file)
                    print(f"  ✅ Found score file: {os.path.basename(score_file)}")
                    print(f"     - Shape: {scores.shape}")
                    if len(scores.shape) == 1 and scores.shape[0] == EXPECTED_NROI:
                        print(f"     - Shape is consistent with n_roi={EXPECTED_NROI}.")
                    else:
                        print(f"     🔥 MISMATCH: Score shape {scores.shape} is NOT consistent with expected n_roi={EXPECTED_NROI}.")
                except Exception as e:
                    print(f"  ❌ ERROR: Could not load or check score file {score_file}: {e}")
            else:
                print(f"  ❌ ERROR: Importance score file not found: {score_file}")

            # Check for .csv file
            if os.path.exists(csv_file):
                print(f"  ✅ Found CSV file: {os.path.basename(csv_file)}")
            else:
                print(f"  ❌ ERROR: ROI name CSV file not found: {csv_file}")


# --- 4. ROI Name Map Check ---
print("\n--- 4. Checking ROI Name Map ---")
if not os.path.exists(ROI_NAME_MAP_PATH):
    print(f"❌ ERROR: ROI name map file not found at: {ROI_NAME_MAP_PATH}")
    print("     This file is crucial for generating the final tables and visualizations.")
else:
    try:
        with open(ROI_NAME_MAP_PATH, 'r') as f:
            roi_map = json.load(f)
        if isinstance(roi_map, dict) and len(roi_map) == EXPECTED_NROI:
            print(f"✅ ROI name map loaded successfully with {len(roi_map)} entries.")
        else:
            print(f"🔥 MISMATCH: ROI name map has {len(roi_map)} entries, but expected {EXPECTED_NROI}.")
    except Exception as e:
        print(f"❌ ERROR: Could not load or parse ROI name map {ROI_NAME_MAP_PATH}: {e}")


print("\n" + "="*60)
print("✅ Automated Check Complete.")
print("="*60) 