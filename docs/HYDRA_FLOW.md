# Hydra Configuration System - How It Works

## 🔄 Configuration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Command Line Interface                       │
│   python train.py model=mlp dataset=fashion_mnist               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hydra Decorator (@hydra.main)                 │
│  - Loads config_path: ../configs                                 │
│  - Loads config_name: config.yaml                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Main Config (config.yaml)                      │
│  defaults:                                                       │
│    - model: convnet      ← Can override with model=mlp          │
│    - dataset: mnist      ← Can override with dataset=...        │
│  training:                                                       │
│    epochs: 10            ← Can override with training.epochs=20 │
│    batch_size: 128                                               │
│    learning_rate: 0.001                                          │
└────────────┬───────────────────────┬────────────────────────────┘
             │                       │
             ▼                       ▼
┌─────────────────────┐   ┌─────────────────────┐
│   Model Configs     │   │   Dataset Configs   │
│  (model/*.yaml)     │   │  (dataset/*.yaml)   │
├─────────────────────┤   ├─────────────────────┤
│ • convnet.yaml      │   │ • mnist.yaml        │
│   - type: convnet   │   │   - name: mnist     │
│   - params:         │   │   - num_classes: 10 │
│     • conv_channels │   │   - data_dir: ./data│
│     • fc_hidden     │   │   - val_split: 0.1  │
│     • dropout       │   │                     │
│                     │   │ • fashion_mnist.yaml│
│ • mlp.yaml          │   │   - name: fashion_  │
│   - type: mlp       │   │     mnist           │
│   - params:         │   │   - num_classes: 10 │
│     • input_size    │   │   - data_dir: ./data│
│     • hidden_sizes  │   │                     │
│     • dropout       │   │                     │
└─────────────────────┘   └─────────────────────┘
             │                       │
             └───────────┬───────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Composed Configuration                         │
│  model:                                                          │
│    type: mlp                    ← From model/mlp.yaml           │
│    params:                                                       │
│      input_size: 784                                             │
│      hidden_sizes: [256, 128]                                    │
│      dropout: 0.3                                                │
│  dataset:                                                        │
│    name: fashion_mnist          ← From dataset/fashion_mnist    │
│    num_classes: 10                                               │
│    data_dir: ./data                                              │
│  training:                                                       │
│    epochs: 10                   ← From config.yaml              │
│    batch_size: 128                                               │
│    learning_rate: 0.001                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Training Script (train.py)                  │
│  def main(cfg: DictConfig):                                      │
│    - Access config: cfg.model.type, cfg.training.epochs         │
│    - Create model: create_model(cfg.model.type, **cfg.model...)│
│    - Load data: create_dataloaders(cfg.dataset.name, ...)      │
│    - Train model with configured hyperparameters                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Outputs (Auto-Created)                        │
│  outputs/2024-01-24/20-30-45/                                    │
│    ├── .hydra/                                                   │
│    │   ├── config.yaml        ← Full resolved config            │
│    │   ├── hydra.yaml         ← Hydra settings                  │
│    │   └── overrides.yaml     ← CLI overrides used              │
│    ├── train.log              ← Training output                 │
│    └── best_model.pth         ← Model checkpoint                │
└─────────────────────────────────────────────────────────────────┘
```

## 📝 Example: How Override Works

### Command:
```bash
python train.py model=mlp dataset=fashion_mnist training.learning_rate=0.01
```

### Resolution Process:

1. **Load base config** (`configs/config.yaml`)
   ```yaml
   defaults:
     - model: convnet      # Will be overridden
     - dataset: mnist      # Will be overridden
   training:
     learning_rate: 0.001  # Will be overridden
   ```

2. **Apply config group overrides** (`model=mlp`, `dataset=fashion_mnist`)
   - Replace `model: convnet` with `model: mlp` → Load `configs/model/mlp.yaml`
   - Replace `dataset: mnist` with `dataset: fashion_mnist` → Load `configs/dataset/fashion_mnist.yaml`

3. **Apply parameter overrides** (`training.learning_rate=0.01`)
   - Override `training.learning_rate` from 0.001 to 0.01

4. **Final configuration**:
   ```yaml
   model:
     type: mlp
     params:
       input_size: 784
       hidden_sizes: [256, 128]
       dropout: 0.3
   dataset:
     name: fashion_mnist
     num_classes: 10
     data_dir: ./data
   training:
     learning_rate: 0.01  # ← Overridden!
     batch_size: 128
     epochs: 10
   ```

## 🔍 Multirun Example

### Command:
```bash
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist
```

### Hydra creates 4 experiments:

```
multirun/2024-01-24/20-30-45/
├── 0/  # convnet + mnist
│   └── .hydra/config.yaml
├── 1/  # convnet + fashion_mnist
│   └── .hydra/config.yaml
├── 2/  # mlp + mnist
│   └── .hydra/config.yaml
└── 3/  # mlp + fashion_mnist
    └── .hydra/config.yaml
```

Each experiment runs independently with its own configuration!

## 🎯 Key Benefits

1. **No code changes needed** - Change behavior via CLI
2. **Reproducibility** - Full config saved with every run
3. **Organization** - Timestamped outputs, no conflicts
4. **Experimentation** - Easy parameter sweeps with multirun
5. **Type safety** - Hydra validates configs at runtime
6. **Modularity** - Mix and match config components

## 💡 Pro Tips

1. **View config without running**: `python train.py --cfg job`
2. **Check available options**: `python train.py --help`
3. **Validate config**: Hydra shows full config at start
4. **Inspect outputs**: Check `.hydra/config.yaml` in output dir
5. **Complex sweeps**: Combine multiple parameters
   ```bash
   python train.py -m model=convnet,mlp training.learning_rate=0.001,0.01 training.batch_size=64,128
   # Creates 2×2×2 = 8 experiments!
   ```
