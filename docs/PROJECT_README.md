# Hydra Configuration for MNIST Classification

This project demonstrates the use of **Hydra** for configuring machine learning experiments on MNIST and Fashion-MNIST datasets using PyTorch.

## Project Structure

```
.
├── src/
│   ├── models.py          # CNN and MLP model implementations
│   ├── train.py           # Main training script with Hydra integration
│   └── data_utils.py      # Dataset preparation and dataloader utilities
├── configs/
│   ├── config.yaml        # Main configuration file
│   ├── model/
│   │   ├── convnet.yaml   # ConvNet configuration
│   │   └── mlp.yaml       # MLP configuration
│   └── dataset/
│       ├── mnist.yaml     # MNIST dataset configuration
│       └── fashion_mnist.yaml  # Fashion-MNIST dataset configuration
├── environment.yml        # Conda environment specification
└── requirements.txt       # Pip requirements
```

## Installation

### Option 1: Using Conda (Recommended)

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate hydra-mnist
```

### Option 2: Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Training

Train with default configuration (ConvNet on MNIST):

```bash
cd src
python train.py
```

### Changing Model

Train with MLP model:

```bash
python train.py model=mlp
```

### Changing Dataset

Train on Fashion-MNIST:

```bash
python train.py dataset=fashion_mnist
```

### Combining Configurations

Train MLP on Fashion-MNIST:

```bash
python train.py model=mlp dataset=fashion_mnist
```

### Override Hyperparameters

Override specific hyperparameters from command line:

```bash
# Change learning rate and batch size
python train.py training.learning_rate=0.01 training.batch_size=64

# Change model architecture
python train.py model=convnet model.params.fc_hidden=256

# Change number of epochs
python train.py training.epochs=20
```

### Run Multiple Experiments (Sweep)

Use Hydra's multirun feature to run multiple experiments:

```bash
# Test different learning rates
python train.py -m training.learning_rate=0.001,0.01,0.1

# Test different models on both datasets
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist

# Grid search
python train.py -m model=convnet,mlp training.learning_rate=0.001,0.01
```

## Configuration Files

### Main Config (`configs/config.yaml`)

Contains:
- Default model and dataset selections
- Training hyperparameters (epochs, batch size, learning rate, etc.)
- Hydra output directory settings

### Model Configs (`configs/model/`)

- `convnet.yaml`: Convolutional Neural Network with configurable channels and layers
- `mlp.yaml`: Multi-Layer Perceptron with configurable hidden layer sizes

### Dataset Configs (`configs/dataset/`)

- `mnist.yaml`: MNIST dataset configuration
- `fashion_mnist.yaml`: Fashion-MNIST dataset configuration

Both include settings for data directory, validation split, and normalization.

## Models

### ConvNet
- 2 convolutional layers with max pooling
- Configurable number of channels
- Fully connected layers with dropout
- ~1.2M parameters (default config)

### MLP
- Fully connected layers
- Configurable hidden layer sizes
- Dropout for regularization
- ~200K parameters (default config)

## Outputs

Hydra automatically creates organized output directories:

```
outputs/
└── YYYY-MM-DD/
    └── HH-MM-SS/
        ├── .hydra/           # Hydra configuration files
        │   ├── config.yaml   # Full resolved config
        │   ├── hydra.yaml    # Hydra settings
        │   └── overrides.yaml # Command line overrides
        ├── train.log         # Training logs
        └── best_model.pth    # Best model checkpoint
```

For multirun experiments:

```
multirun/
└── YYYY-MM-DD/
    └── HH-MM-SS/
        ├── 0/  # First experiment
        ├── 1/  # Second experiment
        └── ...
```

## Example Workflows

### Quick Experiment
```bash
# Train ConvNet on MNIST with default settings
python train.py
```

### Compare Models
```bash
# Run both models on MNIST
python train.py -m model=convnet,mlp
```

### Full Comparison
```bash
# Test all combinations of models and datasets
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist
```

### Hyperparameter Tuning
```bash
# Grid search over learning rates and dropout
python train.py -m training.learning_rate=0.001,0.01 model.params.dropout=0.3,0.5
```

## Key Features

1. **Modular Configuration**: Easy to add new models or datasets
2. **Reproducibility**: All configurations are logged automatically
3. **Experiment Tracking**: Organized output directories with timestamps
4. **Easy Hyperparameter Tuning**: Command-line overrides and multi-run sweeps
5. **Type Safety**: Hydra validates configurations at runtime

## Extending the Project

### Adding a New Model

1. Implement the model in `src/models.py`
2. Update `create_model()` function
3. Create a new config file in `configs/model/`

### Adding a New Dataset

1. Add dataset loading logic in `src/data_utils.py`
2. Create a new config file in `configs/dataset/`

## Tips

- Use `-m` flag for multirun/sweep experiments
- Check `.hydra/config.yaml` in output directory for full resolved configuration
- Use `hydra.run.dir` to customize output directory structure
- Combine with tools like Weights & Biases or MLflow for experiment tracking

## Common Issues

### CUDA Out of Memory
```bash
# Reduce batch size
python train.py training.batch_size=32
```

### Slow Data Loading
```bash
# Increase number of workers
python train.py dataset.num_workers=4
```

## References

- [Hydra Documentation](https://hydra.cc/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
- [Fashion-MNIST Dataset](https://github.com/zalandoresearch/fashion-mnist)
