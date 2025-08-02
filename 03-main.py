import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from imports.PainGraphDataset import PainGraphDataset
from net.multitask_braingnn import MultiTaskBrainGNN
from sklearn.metrics import classification_report, accuracy_score
import argparse
import os

def train_model(model, train_loader, val_loader, optimizer, device, args):
    model.train()
    best_val_acc = 0
    patience_counter = 0

    for epoch in range(args.epochs):
        total_loss = 0
        correct_predictions = 0
        total_samples = 0
        model.train()
        for data in train_loader:
            data = data.to(device)
            optimizer.zero_grad()
            out, _ = model(data) # Unpack the tuple here
            loss = F.nll_loss(out, data.y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * data.num_graphs
            pred = out.argmax(dim=1)
            correct_predictions += pred.eq(data.y).sum().item()
            total_samples += data.num_graphs

        train_loss = total_loss / total_samples
        train_acc = correct_predictions / total_samples
        val_acc, _ = evaluate_model(model, val_loader, device)
        
        print(f'Epoch {epoch+1}/{args.epochs}, Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}')

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            torch.save(model.state_dict(), args.model_path)
            print(f"✅ New best model saved to {args.model_path} with Val Acc: {val_acc:.4f}")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"Early stopping triggered after {args.patience} epochs with no improvement.")
                break

def evaluate_model(model, loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out, _ = model(data) # Unpack the tuple here
            preds = out.argmax(dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(data.y.cpu().numpy())
            
    accuracy = accuracy_score(all_labels, all_preds)
    report = classification_report(all_labels, all_preds, zero_division=0)
    return accuracy, report

def main():
    parser = argparse.ArgumentParser(description="Train MultiTask BrainGNN Model")
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu', help='Device to use for training (cuda or cpu)')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--weight_decay', type=float, default=0.0005, help='Weight decay (L2 penalty)')
    parser.add_argument('--patience', type=int, default=20, help='Patience for early stopping')
    parser.add_argument('--data_path', type=str, default='./data/pain_data/all_graphs/', help='Path to the graph data directory')
    parser.add_argument('--model_path', type=str, default='./model/best_pain_model_113.pth', help='Path to save the best model')

    args = parser.parse_args()
    device = torch.device(args.device)
    print(f"Using device: {device}")

    # Ensure model directory exists
    os.makedirs(os.path.dirname(args.model_path), exist_ok=True)

    # --- Data Loading and Filtering ---
    # Hardcoded shape based on our data analysis
    N_ROI = 116
    IN_DIM = 1
    print(f"❗ Configuring for n_roi={N_ROI} and in_dim={IN_DIM}.")

    print(f"🔍 Loading all data from: {args.data_path} for manual filtering...")
    # Load the entire dataset without pre-filtering
    full_dataset = PainGraphDataset(root_dir=args.data_path)
    
    # Manually filter the dataset
    filtered_data_list = []
    for i in range(len(full_dataset)):
        try:
            data = full_dataset[i]
            if data.x.shape == (N_ROI, IN_DIM):
                filtered_data_list.append(data)
        except Exception as e:
            # print(f"Skipping sample {i} due to error: {e}")
            continue # Skip corrupted or problematic files

    if not filtered_data_list:
        print(f"❌ CRITICAL ERROR: No data found with shape ({N_ROI}, {IN_DIM}) after manual filtering.")
        print("Please check the `data_path` or the N_ROI/IN_DIM settings in the script.")
        return

    print(f"✅ Successfully filtered dataset. Found {len(filtered_data_list)} samples with shape ({N_ROI}, {IN_DIM}).")
    
    # Set the target 'y' for all samples to be a long tensor
    for data in filtered_data_list:
        data.y = data.y.long()


    # --- Dataset Splitting ---
    train_size = int(0.7 * len(filtered_data_list))
    val_size = int(0.15 * len(filtered_data_list))
    test_size = len(filtered_data_list) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        filtered_data_list, [train_size, val_size, test_size]
    )
    print(f"Split dataset into Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}")
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    # --- Model, Optimizer ---
    model = MultiTaskBrainGNN(in_dim=IN_DIM, n_roi=N_ROI).to(device)
    print(f"Model created on {device}. Total parameters: {sum(p.numel() for p in model.parameters())}")
    
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    
    # --- Training ---
    print("\n--- Starting Model Training ---")
    train_model(model, train_loader, val_loader, optimizer, device, args)
    
    # --- Final Evaluation ---
    print("\n--- Final Test Set Evaluation ---")
    print(f"Loading best model from {args.model_path} for final evaluation.")
    model.load_state_dict(torch.load(args.model_path, map_location=device))
    test_accuracy, test_report = evaluate_model(model, test_loader, device)
    
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    print("Classification Report:")
    print(test_report)
    print("\n✨ Training and evaluation complete. Best model saved at:", args.model_path)

if __name__ == '__main__':
    main() 