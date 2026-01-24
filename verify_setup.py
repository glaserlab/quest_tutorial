#!/usr/bin/env python3
"""
Quick test script to verify the Hydra MNIST project setup.
Run this before training to ensure everything is configured correctly.
"""

import sys
import os

def test_imports():
    """Test that all required libraries can be imported."""
    print("Testing imports...")
    
    required = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'hydra': 'Hydra',
        'omegaconf': 'OmegaConf',
        'tqdm': 'tqdm'
    }
    
    failed = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing libraries: {', '.join(failed)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required libraries found!")
        return True


def test_project_structure():
    """Test that all required files exist."""
    print("\nTesting project structure...")
    
    required_files = [
        'src/models.py',
        'src/train.py',
        'src/data_utils.py',
        'configs/config.yaml',
        'configs/model/convnet.yaml',
        'configs/model/mlp.yaml',
        'configs/dataset/mnist.yaml',
        'configs/dataset/fashion_mnist.yaml',
    ]
    
    missing = []
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} - NOT FOUND")
            missing.append(filepath)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    else:
        print("\n✓ All required files found!")
        return True


def test_hydra_config():
    """Test that Hydra can load configurations."""
    print("\nTesting Hydra configuration...")
    
    try:
        from hydra import compose, initialize
        from omegaconf import OmegaConf
        
        with initialize(version_base=None, config_path="configs"):
            # Test default config
            cfg = compose(config_name="config")
            print(f"  ✓ Loaded default config")
            print(f"    - Model: {cfg.model.type}")
            print(f"    - Dataset: {cfg.dataset.name}")
            
            # Test model configs
            cfg = compose(config_name="config", overrides=["model=mlp"])
            print(f"  ✓ Loaded MLP config")
            
            # Test dataset configs
            cfg = compose(config_name="config", overrides=["dataset=fashion_mnist"])
            print(f"  ✓ Loaded Fashion-MNIST config")
            
        print("\n✓ All configurations load successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        return False


def test_model_creation():
    """Test that models can be created."""
    print("\nTesting model creation...")
    
    try:
        sys.path.insert(0, 'src')
        from models import create_model
        
        # Test ConvNet
        model = create_model('convnet', num_classes=10, input_channels=1)
        print(f"  ✓ Created ConvNet")
        
        # Test MLP
        model = create_model('mlp', num_classes=10, input_size=784)
        print(f"  ✓ Created MLP")
        
        print("\n✓ All models can be created!")
        return True
        
    except Exception as e:
        print(f"\n❌ Model creation error: {e}")
        return False


def print_summary():
    """Print helpful summary."""
    print("\n" + "="*80)
    print("SETUP VERIFICATION COMPLETE")
    print("="*80)
    print("\n✅ Your environment is ready!")
    print("\nNext steps:")
    print("  1. cd src")
    print("  2. python train.py")
    print("\nFor more examples, see:")
    print("  - docs/HYDRA_GUIDE.md")
    print("  - docs/PROJECT_README.md")
    print("  - ./quickstart.sh")
    print("  - python ../show_configs.py")
    print("="*80)


def main():
    """Run all tests."""
    print("="*80)
    print("HYDRA MNIST PROJECT - SETUP VERIFICATION")
    print("="*80)
    
    tests = [
        test_imports,
        test_project_structure,
        test_hydra_config,
        test_model_creation,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*80)
    if all(results):
        print_summary()
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*80)
        print("\nPlease fix the issues above before running training.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
