# Hydra MNIST Project - Documentation Index

Welcome! This project demonstrates using Hydra for ML experiment configuration. Start here to find what you need.

## 🚀 Quick Start (First Time Users)

1. **[HYDRA_GUIDE.md](HYDRA_GUIDE.md)** - Start here! Quick reference with examples
2. **[verify_setup.py](../verify_setup.py)** - Run this to check your environment
3. **[QUICK_REFERENCE.txt](../QUICK_REFERENCE.txt)** - Command cheat sheet

## 📚 Complete Documentation

### For Learning
- **[HYDRA_GUIDE.md](HYDRA_GUIDE.md)** (5.3 KB)
  - Quick overview and common commands
  - Perfect for getting started quickly
  
- **[HYDRA_FLOW.md](HYDRA_FLOW.md)** (9.7 KB)
  - Visual explanation of how Hydra works
  - Flow diagrams and examples
  - Best for understanding the system

- **[PROJECT_README.md](PROJECT_README.md)** (6.0 KB)
  - Comprehensive documentation
  - All features explained in detail
  - Reference for advanced usage

### For Reference
- **[QUICK_REFERENCE.txt](../QUICK_REFERENCE.txt)** (4.5 KB)
  - One-page command reference
  - Common workflows and tips
  - Keep this handy while working

- **[PROJECT_SUMMARY.txt](../PROJECT_SUMMARY.txt)** (9.9 KB)
  - Complete project checklist
  - All deliverables listed
  - Setup verification guide

## 🛠️ Tools & Scripts

### Setup & Verification
- **[verify_setup.py](../verify_setup.py)**
  - Tests all dependencies
  - Verifies project structure
  - Validates Hydra configs
  - **Run this first!**

### Configuration Tools
- **[show_configs.py](../show_configs.py)**
  - Displays all available configurations
  - Shows how overrides work
  - Examples of different config combinations

### Examples
- **[quickstart.sh](../quickstart.sh)**
  - Shell script with example commands
  - Good for copy-pasting

## 📁 Project Files

### Source Code
```
src/
├── models.py       # ConvNet and MLP implementations
├── train.py        # Main training script with Hydra
└── data_utils.py   # Dataset preparation utilities
```

### Configurations
```
configs/
├── config.yaml     # Main configuration
├── model/
│   ├── convnet.yaml  # CNN configuration
│   └── mlp.yaml      # MLP configuration
└── dataset/
    ├── mnist.yaml           # MNIST dataset
    └── fashion_mnist.yaml   # Fashion-MNIST dataset
```

### Environment
- **[environment.yml](../environment.yml)** - Conda environment (recommended)
- **[requirements.txt](../requirements.txt)** - Pip dependencies (alternative)

## 🎯 Usage Examples

### Viewing Examples
```bash
# See example commands
./quickstart.sh

# View all configurations
python show_configs.py

# Print config without running
cd src && python train.py --cfg job
```

### Basic Training
```bash
cd src

# Default configuration
python train.py

# Use different model
python train.py model=mlp

# Use different dataset
python train.py dataset=fashion_mnist

# Combine both
python train.py model=mlp dataset=fashion_mnist
```

### Advanced Usage
```bash
# Override hyperparameters
python train.py training.learning_rate=0.01 training.epochs=20

# Run multiple experiments
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist

# Hyperparameter sweep
python train.py -m training.learning_rate=0.001,0.01,0.1
```

## 📖 Learning Path

### Beginner
1. Read [HYDRA_GUIDE.md](HYDRA_GUIDE.md)
2. Run `python verify_setup.py`
3. Try `cd src && python train.py`
4. Experiment with `model=mlp` and `dataset=fashion_mnist`

### Intermediate
1. Read [HYDRA_FLOW.md](HYDRA_FLOW.md) to understand the system
2. Try overriding parameters: `training.learning_rate=0.01`
3. Run multi-experiments: `python train.py -m model=convnet,mlp`
4. Inspect outputs in `outputs/` directory

### Advanced
1. Read [PROJECT_README.md](PROJECT_README.md) for all features
2. Create custom model configs
3. Run complex sweeps with multiple parameters
4. Extend with new models and datasets

## ❓ Troubleshooting

### Installation Issues
1. Run `python verify_setup.py` to diagnose
2. Check [PROJECT_README.md](PROJECT_README.md) - "Common Issues" section
3. Try pip install if conda fails: `pip install -r requirements.txt`

### Running Issues
- **Out of memory**: `python train.py training.batch_size=32`
- **Slow loading**: `python train.py dataset.num_workers=4`
- **Config errors**: Check [HYDRA_FLOW.md](HYDRA_FLOW.md) for syntax

## 🔗 External Resources

- [Hydra Official Docs](https://hydra.cc/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [MNIST Dataset Info](http://yann.lecun.com/exdb/mnist/)
- [Fashion-MNIST Dataset](https://github.com/zalandoresearch/fashion-mnist)

## 📋 Quick Links by Task

| I want to... | Read this... |
|-------------|--------------|
| Get started quickly | [HYDRA_GUIDE.md](HYDRA_GUIDE.md) |
| Understand how Hydra works | [HYDRA_FLOW.md](HYDRA_FLOW.md) |
| See all features | [PROJECT_README.md](PROJECT_README.md) |
| Find a specific command | [QUICK_REFERENCE.txt](../QUICK_REFERENCE.txt) |
| Verify my setup | Run `python verify_setup.py` |
| See example commands | Run `./quickstart.sh` |
| View all configs | Run `python show_configs.py` |
| Check what was created | [PROJECT_SUMMARY.txt](../PROJECT_SUMMARY.txt) |

## 💡 Tips

- Keep [QUICK_REFERENCE.txt](QUICK_REFERENCE.txt) open while experimenting
- All configs are saved in `.hydra/config.yaml` in output directories
- Use `-m` flag for running multiple experiments
- Start with default config, then try variations

---

**Ready to start?** Run: `python verify_setup.py`

**Need help?** Check the documentation files above or run `./quickstart.sh` for examples.
