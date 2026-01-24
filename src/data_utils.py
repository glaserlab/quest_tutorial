import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split


def get_transforms(normalize=True):
    """Get data transformations for MNIST-style datasets."""
    transform_list = [transforms.ToTensor()]
    
    if normalize:
        # MNIST and Fashion-MNIST normalization values
        transform_list.append(transforms.Normalize((0.5,), (0.5,)))
    
    return transforms.Compose(transform_list)


def prepare_dataset(dataset_name, data_dir, train=True, download=True, normalize=True):
    """Download and prepare MNIST or Fashion-MNIST dataset."""
    transform = get_transforms(normalize=normalize)
    
    if dataset_name.lower() == "mnist":
        dataset = datasets.MNIST(
            root=data_dir,
            train=train,
            download=download,
            transform=transform
        )
    elif dataset_name.lower() == "fashion_mnist":
        dataset = datasets.FashionMNIST(
            root=data_dir,
            train=train,
            download=download,
            transform=transform
        )
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    return dataset


def create_dataloaders(dataset_name, data_dir, batch_size=64, val_split=0.1, 
                       num_workers=2, download=True, normalize=True):
    """Create train, validation, and test dataloaders."""
    
    # Load training data
    train_dataset = prepare_dataset(
        dataset_name, data_dir, train=True, download=download, normalize=normalize
    )
    
    # Split into train and validation
    if val_split > 0:
        val_size = int(len(train_dataset) * val_split)
        train_size = len(train_dataset) - val_size
        train_dataset, val_dataset = random_split(
            train_dataset, 
            [train_size, val_size],
            generator=torch.Generator().manual_seed(42)
        )
    else:
        val_dataset = None
    
    # Load test data
    test_dataset = prepare_dataset(
        dataset_name, data_dir, train=False, download=download, normalize=normalize
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = None
    if val_dataset is not None:
        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True
        )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader
