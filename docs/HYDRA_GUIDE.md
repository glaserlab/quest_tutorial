# Hydra MNIST Classification Project

## 📁 Project Overview

A complete PyTorch project demonstrating **Hydra configuration framework** for managing ML experiments on MNIST and Fashion-MNIST datasets. Features modular configuration, easy hyperparameter tuning, and organized experiment tracking.

## 🚀 Quick Start

### 1. Install Dependencies

**Option A: Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate hydra-mnist
```

**Option B: Pip**
```bash
pip install -r requirements.txt
```

### 2. Run Training

```bash
cd src
python train.py
```

## 📂 Project Structure

```
.
├── src/
│   ├── models.py          # CNN and MLP implementations
│   ├── train.py           # Training script with Hydra
│   ├── data_utils.py      # Dataset utilities
│   └── utils.py           # General utilities
├── configs/
│   ├── config.yaml        # Main configuration
│   ├── model/
│   │   ├── convnet.yaml   # ConvNet config
│   │   └── mlp.yaml       # MLP config
│   └── dataset/
│       ├── mnist.yaml     # MNIST config
│       └── fashion_mnist.yaml  # Fashion-MNIST config
├── environment.yml        # Conda environment
├── requirements.txt       # Pip requirements
├── quickstart.sh          # Example commands
└── PROJECT_README.md      # Detailed documentation
```

## 🎯 Usage Examples

### Basic Commands

```bash
# Default: ConvNet on MNIST
python train.py

# Use MLP model
python train.py model=mlp

# Use Fashion-MNIST dataset
python train.py dataset=fashion_mnist

# Combine both
python train.py model=mlp dataset=fashion_mnist
```

### Override Hyperparameters

```bash
# Change learning rate and batch size
python train.py training.learning_rate=0.01 training.batch_size=64

# Modify model architecture
python train.py model=convnet model.params.fc_hidden=256

# Change training duration
python train.py training.epochs=20
```

### Run Multiple Experiments

```bash
# Test different learning rates
python train.py -m training.learning_rate=0.001,0.01,0.1

# Compare models on both datasets (4 experiments)
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist

# Grid search
python train.py -m model=convnet,mlp training.learning_rate=0.001,0.01
```

## 🧠 Models

### ConvNet (Convolutional Neural Network)
- 2 conv layers (32, 64 channels)
- Max pooling + dropout
- 2 FC layers
- ~1.2M parameters

### MLP (Multi-Layer Perceptron)
- Fully connected layers (256, 128 hidden)
- ReLU activation + dropout
- ~200K parameters

## 📊 Datasets

- **MNIST**: Handwritten digits (10 classes)
- **Fashion-MNIST**: Fashion items (10 classes)
- Automatic download and preprocessing
- 10% validation split by default

## ⚙️ Configuration

### Main Config (`configs/config.yaml`)
- Training: epochs, batch size, learning rate, scheduler
- Defaults: which model and dataset to use
- Hydra: output directory structure

### Model Configs (`configs/model/`)
- Architecture parameters
- Dropout rates
- Layer sizes

### Dataset Configs (`configs/dataset/`)
- Dataset selection
- Data directory
- Validation split
- Normalization settings

## 📁 Output Structure

Each experiment creates an organized directory:

```
outputs/
└── 2024-01-24/
    └── 20-30-45/
        ├── .hydra/
        │   ├── config.yaml      # Full resolved config
        │   └── overrides.yaml   # CLI overrides
        ├── train.log            # Training logs
        └── best_model.pth       # Best checkpoint
```

Multirun experiments:
```
multirun/
└── 2024-01-24/
    └── 20-30-45/
        ├── 0/  # Experiment 1
        ├── 1/  # Experiment 2
        └── ...
```

## 🎓 Key Hydra Features Demonstrated

1. **Modular Configuration**: Separate configs for models and datasets
2. **Config Groups**: Easy switching with `model=` and `dataset=`
3. **Override from CLI**: Change any parameter on the fly
4. **Multirun/Sweeps**: Run multiple experiments with `-m` flag
5. **Automatic Logging**: All configs saved with outputs
6. **Structured Outputs**: Timestamped directories

## 🔧 Extending the Project

### Add a New Model

1. Implement in `src/models.py`
2. Update `create_model()` function
3. Create `configs/model/your_model.yaml`

```yaml
# configs/model/resnet.yaml
# @package _global_.model
type: resnet
params:
  num_layers: 18
  pretrained: false
```

### Add a New Dataset

1. Add loader in `src/data_utils.py`
2. Create `configs/dataset/your_dataset.yaml`

```yaml
# configs/dataset/cifar10.yaml
# @package _global_.dataset
name: cifar10
num_classes: 10
data_dir: ./data
```

## 💡 Tips

- Use `./quickstart.sh` to see example commands
- Check `.hydra/config.yaml` in output dir for full config
- Combine with Weights & Biases or MLflow for tracking
- Use `-m` for parameter sweeps
- Reduce `batch_size` if out of memory

## 📚 Additional Resources

- Full documentation: `PROJECT_README.md`
- [Hydra Docs](https://hydra.cc/)
- [PyTorch Docs](https://pytorch.org/)

## 🐛 Troubleshooting

**CUDA Out of Memory**
```bash
python train.py training.batch_size=32
```

**Slow Data Loading**
```bash
python train.py dataset.num_workers=4
```

**View Full Config**
```bash
python train.py --cfg job  # Print config and exit
```

---

**Ready to run?** Execute `./quickstart.sh` to see examples or jump to `src/` and run `python train.py`!
