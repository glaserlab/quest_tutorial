import os
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import hydra
from omegaconf import DictConfig, OmegaConf

from models import create_model
from data_utils import create_dataloaders


def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc="Training")
    for inputs, labels in pbar:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({
            'loss': running_loss / (pbar.n + 1),
            'acc': 100. * correct / total
        })
    
    return running_loss / len(train_loader), 100. * correct / total


def evaluate(model, data_loader, criterion, device, desc="Validation"):
    """Evaluate model on a dataset."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(data_loader, desc=desc)
        for inputs, labels in pbar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': running_loss / (pbar.n + 1),
                'acc': 100. * correct / total
            })
    
    return running_loss / len(data_loader), 100. * correct / total


@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    """Main training function."""
    
    print("=" * 80)
    print("Configuration:")
    print(OmegaConf.to_yaml(cfg))
    print("=" * 80)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nUsing device: {device}")
    
    # Create dataloaders
    print(f"\nPreparing {cfg.dataset.name} dataset...")
    train_loader, val_loader, test_loader = create_dataloaders(
        dataset_name=cfg.dataset.name,
        data_dir=cfg.dataset.data_dir,
        batch_size=cfg.training.batch_size,
        val_split=cfg.dataset.val_split,
        num_workers=cfg.dataset.num_workers,
        normalize=cfg.dataset.normalize
    )
    
    print(f"Train samples: {len(train_loader.dataset)}")
    if val_loader:
        print(f"Validation samples: {len(val_loader.dataset)}")
    print(f"Test samples: {len(test_loader.dataset)}")
    
    # Create model
    print(f"\nCreating {cfg.model.type} model...")
    model = create_model(
        model_type=cfg.model.type,
        num_classes=cfg.dataset.num_classes,
        **cfg.model.params
    )
    model = model.to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(
        model.parameters(),
        lr=cfg.training.learning_rate,
        weight_decay=cfg.training.weight_decay
    )
    
    # Learning rate scheduler
    scheduler = None
    if cfg.training.use_scheduler:
        scheduler = optim.lr_scheduler.StepLR(
            optimizer,
            step_size=cfg.training.scheduler_step,
            gamma=cfg.training.scheduler_gamma
        )
    
    # Training loop
    print(f"\nTraining for {cfg.training.epochs} epochs...")
    best_val_acc = 0.0
    
    for epoch in range(cfg.training.epochs):
        print(f"\nEpoch {epoch + 1}/{cfg.training.epochs}")
        
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device
        )
        
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        
        if val_loader:
            val_loss, val_acc = evaluate(
                model, val_loader, criterion, device, desc="Validation"
            )
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), "best_model.pth")
                print(f"Saved best model with validation accuracy: {best_val_acc:.2f}%")
        
        if scheduler:
            scheduler.step()
            print(f"Learning rate: {scheduler.get_last_lr()[0]:.6f}")
    
    # Test evaluation
    print("\n" + "=" * 80)
    print("Final Test Evaluation")
    print("=" * 80)
    
    if val_loader and os.path.exists("best_model.pth"):
        print("Loading best model...")
        model.load_state_dict(torch.load("best_model.pth"))
    
    test_loss, test_acc = evaluate(
        model, test_loader, criterion, device, desc="Testing"
    )
    print(f"\nTest Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")
    
    return test_acc


if __name__ == "__main__":
    main()
