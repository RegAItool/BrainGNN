import numpy as np
from sklearn.model_selection import StratifiedKFold

def train_val_test_split(fold=0, n_splits=5):
    """
    Split dataset into train/val/test sets using stratified k-fold.
    """
    # Load the dataset to get labels
    from imports.ABIDEDataset import ABIDEDataset
    dataset = ABIDEDataset('./data/ABIDE_pcp/cpac/filt_noglobal', 'ABIDE')
    labels = dataset.data.y.squeeze().numpy()
    
    # Create stratified k-fold split
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Get the split for the specified fold
    splits = list(skf.split(np.arange(len(labels)), labels))
    train_val_idx, test_idx = splits[fold]
    
    # Further split train_val into train and validation
    train_val_labels = labels[train_val_idx]
    skf_inner = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    inner_splits = list(skf_inner.split(train_val_idx, train_val_labels))
    train_idx, val_idx = inner_splits[0]
    
    # Map back to original indices
    train_idx = train_val_idx[train_idx]
    val_idx = train_val_idx[val_idx]
    
    return train_idx, val_idx, test_idx 