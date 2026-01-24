#!/usr/bin/env python3
"""
Example script showing programmatic access to Hydra configs.
This demonstrates how to load and inspect configurations without running training.
"""

from hydra import compose, initialize
from omegaconf import OmegaConf

def show_configs():
    """Display all available configurations."""
    
    print("=" * 80)
    print("Available Configurations")
    print("=" * 80)
    
    # Initialize Hydra
    with initialize(version_base=None, config_path="../configs"):
        
        # Default configuration
        print("\n1. DEFAULT CONFIGURATION (ConvNet + MNIST)")
        print("-" * 80)
        cfg = compose(config_name="config")
        print(OmegaConf.to_yaml(cfg))
        
        # MLP configuration
        print("\n2. MLP MODEL CONFIGURATION")
        print("-" * 80)
        cfg = compose(config_name="config", overrides=["model=mlp"])
        print(OmegaConf.to_yaml(cfg.model))
        
        # Fashion-MNIST configuration
        print("\n3. FASHION-MNIST DATASET CONFIGURATION")
        print("-" * 80)
        cfg = compose(config_name="config", overrides=["dataset=fashion_mnist"])
        print(OmegaConf.to_yaml(cfg.dataset))
        
        # Custom overrides
        print("\n4. CUSTOM CONFIGURATION (MLP + Fashion-MNIST + Custom LR)")
        print("-" * 80)
        cfg = compose(
            config_name="config",
            overrides=[
                "model=mlp",
                "dataset=fashion_mnist",
                "training.learning_rate=0.01",
                "training.epochs=5"
            ]
        )
        print(OmegaConf.to_yaml(cfg))
        
        # Show specific parameters
        print("\n5. ACCESSING SPECIFIC PARAMETERS")
        print("-" * 80)
        print(f"Model type: {cfg.model.type}")
        print(f"Dataset name: {cfg.dataset.name}")
        print(f"Learning rate: {cfg.training.learning_rate}")
        print(f"Batch size: {cfg.training.batch_size}")
        print(f"Number of epochs: {cfg.training.epochs}")
        
        # Show parameter counts for both models
        print("\n6. MODEL COMPARISONS")
        print("-" * 80)
        
        cfg_cnn = compose(config_name="config", overrides=["model=convnet"])
        cfg_mlp = compose(config_name="config", overrides=["model=mlp"])
        
        print("ConvNet Parameters:")
        print(f"  - Channels: {cfg_cnn.model.params.conv_channels}")
        print(f"  - FC Hidden: {cfg_cnn.model.params.fc_hidden}")
        print(f"  - Dropout: {cfg_cnn.model.params.dropout}")
        
        print("\nMLP Parameters:")
        print(f"  - Hidden sizes: {cfg_mlp.model.params.hidden_sizes}")
        print(f"  - Dropout: {cfg_mlp.model.params.dropout}")


def show_sweep_examples():
    """Show examples of multirun configurations."""
    
    print("\n" + "=" * 80)
    print("Multirun Sweep Examples")
    print("=" * 80)
    
    examples = [
        {
            "description": "Compare both models on MNIST",
            "command": "python train.py -m model=convnet,mlp"
        },
        {
            "description": "Test learning rates",
            "command": "python train.py -m training.learning_rate=0.001,0.01,0.1"
        },
        {
            "description": "Full model-dataset comparison (4 runs)",
            "command": "python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist"
        },
        {
            "description": "Grid search: 2 models × 3 learning rates (6 runs)",
            "command": "python train.py -m model=convnet,mlp training.learning_rate=0.001,0.01,0.1"
        },
        {
            "description": "Architecture search for ConvNet",
            "command": "python train.py -m model=convnet model.params.fc_hidden=64,128,256"
        },
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   {example['command']}")


if __name__ == "__main__":
    show_configs()
    show_sweep_examples()
    
    print("\n" + "=" * 80)
    print("To run training with any configuration, use:")
    print("  cd src && python train.py [overrides]")
    print("=" * 80)
