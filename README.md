# Quest Tutorial

---

## 🎯 Hydra MNIST Classification Project

**A complete demonstration of using Hydra for ML experiment configuration with PyTorch.**

### Quick Start

```bash
# 1. Verify setup
python verify_setup.py

# 2. Install dependencies
conda env create -f environment.yml
conda activate hydra-mnist

# 3. Run training
cd src && python train.py
```

### 📚 Documentation

- **[HYDRA_GUIDE.md](docs/HYDRA_GUIDE.md)** - Quick start guide with examples
- **[PROJECT_README.md](docs/PROJECT_README.md)** - Comprehensive documentation
- **[HYDRA_FLOW.md](docs/HYDRA_FLOW.md)** - Visual explanation of Hydra's configuration system

### 🚀 Quick Examples

```bash
# Compare models
python train.py model=mlp

# Try Fashion-MNIST
python train.py dataset=fashion_mnist

# Hyperparameter override
python train.py training.learning_rate=0.01 training.epochs=20

# Run multiple experiments
python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist
```

### 📦 Project Contents

```
├── src/
│   ├── models.py          # CNN & MLP implementations
│   ├── train.py           # Training script with Hydra
│   └── data_utils.py      # Dataset utilities
├── configs/
│   ├── config.yaml        # Main configuration
│   ├── model/             # Model configs (convnet, mlp)
│   └── dataset/           # Dataset configs (mnist, fashion_mnist)
├── environment.yml        # Conda environment
├── requirements.txt       # Pip dependencies
├── verify_setup.py        # Setup verification
├── show_configs.py        # Config inspection tool
└── quickstart.sh          # Example commands
```

### 🎓 What You'll Learn

✓ How to use **Hydra** for ML experiment configuration  
✓ Modular config files with **config groups**  
✓ Command-line overrides for hyperparameters  
✓ Running **multi-run experiments** for sweeps  
✓ Organized output directories and logging  
✓ Best practices for reproducible ML experiments

### 🛠️ Features

- Two neural network architectures (ConvNet & MLP)
- Two datasets (MNIST & Fashion-MNIST)
- Automatic data downloading and preprocessing
- Validation split and best model checkpointing
- Progress bars and detailed logging
- Learning rate scheduling
- Fully configurable via YAML files

---

## Original Quest Tutorial Content

Writing up a general tutorial for my Quest workflow, which I mostly use when I need to run paralle jobs. I use git/conda to set-up an environment, Globus to transfer files, and the Python multipool to run parallel jobs.

## Set-up

Couple things to do first

### Quest allocation

Join existing allocation: [https://app.smartsheet.com/b/form/797775d810274db5889b5199c4260328](https://app.smartsheet.com/b/form/797775d810274db5889b5199c4260328)

Request new allocation: [https://app.smartsheet.com/b/form/86d88375bd7345439bd391d8184b6ea0](https://app.smartsheet.com/b/form/86d88375bd7345439bd391d8184b6ea0)

When everything is working, you should have an account# (PXXXXX)

### Globus

Activating quest endpoint: [https://services.northwestern.edu/TDClient/30/Portal/KB/ArticleDet?ID=1962](https://services.northwestern.edu/TDClient/30/Portal/KB/ArticleDet?ID=1962)

Activating personal endpoint: [https://www.globus.org/globus-connect-personal](https://www.globus.org/globus-connect-personal)

## Connecting to Quest

### Connecting to log-node

I use SSH to connect. I can't remember if there was anymore set-up than this, but I believe once you're granted allocation you can use `ssh NETID@quest.northwestern.edu`

### Transfering scripts

I suggest using git to clone code onto quest. Git comes preinstalled on the log-in nodes, so `git clone REPO.git` ought to work out of the box.

### Transfering larger files

I use Globus to transfer files. See set-up for there, then I use web GUI [app.globus.org](app.globus.org)

## Submitting jobs on quest

### Submission script

Submit submission script with `sbatch XXX.sh`. Make sure your partition/job length/memory usage/num_cores all "match up": 

![](media/partitions.png)

![](media/waittimes.png)

See sample submission script for exact make-up of script.

### Checking on jobs

`squeue -u NETID` for job status

`scancel JOBID` to cancel job

`seff JOBID` for memory usage of completed job

`sacct -X` for status of all jobs over last week or so

