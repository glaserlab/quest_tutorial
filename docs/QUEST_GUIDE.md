# Running on QUEST SLURM Cluster

This guide explains how to run experiments on Northwestern's QUEST SLURM cluster using Hydra's submitit launcher.

## 🚀 Quick Start

```bash
# Run on QUEST with single experiment
python train.py env=quest

# Run sweep on QUEST
python train.py -m env=quest model=convnet,mlp dataset=mnist,fashion_mnist
```

## 📋 Table of Contents

1. [Setup](#setup)
2. [Configuration](#configuration)
3. [Running Jobs](#running-jobs)
4. [Monitoring Jobs](#monitoring-jobs)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Setup

### 1. Install Dependencies

On QUEST, load modules and install the environment:

```bash
# SSH to QUEST
ssh your_netid@quest.northwestern.edu

# Navigate to your project directory
cd /projects/YOUR_PROJECT_ID/hydra-mnist

# Load Python module
module load python/3.10

# Create conda environment
conda env create -f environment.yml
conda activate hydra-mnist
```

### 2. Configure QUEST Paths

Edit `configs/env/quest.yaml` and update the paths:

```yaml
paths:
  data_dir: /projects/YOUR_PROJECT_ID/data
  output_dir: /projects/YOUR_PROJECT_ID/outputs
```

### 3. Configure SLURM Parameters (Optional)

Edit `configs/hydra/launcher/quest.yaml` to set your preferred defaults:

- **Account**: Your QUEST allocation (if required)
- **Partition**: Default partition to use
- **Email**: For job notifications
- **Resources**: Memory, CPUs, GPUs, timeout

---

## Configuration

### Environment Configs

Two environment configurations are provided:

#### Local (`configs/env/local.yaml`)
- **Use when**: Running on your laptop/desktop
- **Data location**: `./data`
- **Output location**: `./outputs`
- **Launcher**: Basic (no SLURM)

```bash
# Use local environment (default)
python train.py env=local
# or simply
python train.py
```

#### QUEST (`configs/env/quest.yaml`)
- **Use when**: Running on QUEST cluster
- **Data location**: `/projects/YOUR_PROJECT_ID/data`
- **Output location**: `/projects/YOUR_PROJECT_ID/outputs`
- **Launcher**: Submitit SLURM

```bash
# Use QUEST environment
python train.py env=quest
```

### SLURM Launcher Config

The `configs/hydra/launcher/quest.yaml` file controls SLURM job parameters:

```yaml
hydra:
  launcher:
    timeout_min: 60        # Job timeout (minutes)
    cpus_per_task: 4       # CPUs per task
    gpus_per_node: 1       # GPUs per node (0 for CPU-only)
    mem_gb: 16             # Memory in GB
    nodes: 1               # Number of nodes
    partition: "short"     # QUEST partition
```

---

## Running Jobs
**NOTE:** All jobs must use the -m (--multirun) flag to trigger hydra_submitit
### Single Job

Run a single experiment on QUEST:

```bash
python train.py -m env=quest
```

### Multirun/Sweep

Run multiple experiments in parallel on QUEST:

```bash
# Compare models
python train.py -m env=quest model=convnet,mlp

# Full sweep (4 jobs)
python train.py -m env=quest model=convnet,mlp dataset=mnist,fashion_mnist

# Hyperparameter search
python train.py -m env=quest training.learning_rate=0.001,0.01,0.1
```

### Override SLURM Parameters

Override SLURM parameters from command line:

```bash
# Use GPU partition with more memory
python train.py env=quest \
  hydra.launcher.partition=gpu \
  hydra.launcher.mem_gb=32 \
  hydra.launcher.timeout_min=120

# CPU-only job
python train.py env=quest \
  hydra.launcher.gpus_per_node=0 \
  hydra.launcher.cpus_per_task=8

# Long-running job
python train.py env=quest \
  hydra.launcher.partition=long \
  hydra.launcher.timeout_min=1440 \
  training.epochs=100
```

---

## Monitoring Jobs

### Check Job Status

```bash
# View your jobs
squeue -u $USER

# View detailed job info
scontrol show job JOBID

# Cancel a job
scancel JOBID

# Cancel all your jobs
scancel -u $USER
```

### View Outputs

Job outputs are stored in the Hydra output directory:

```bash
# Navigate to output directory
cd /projects/YOUR_PROJECT_ID/SUBFOLDERS/outputs/YYYY-MM-DD/HH-MM-SS

# View Hydra logs
ls -la .submitit/

# View training output (if job completed)
cat train.log
```

### Check Job Logs

Submitit creates detailed logs in `.submitit/` subdirectory:

```bash
# In your Hydra output directory
cd .submitit/

# View SLURM output
cat *_0_log.out

# View SLURM errors
cat *_0_log.err
```

---

## Advanced Usage

### Custom SLURM Configuration

Create a custom launcher config for specific needs:

```bash
# Create configs/hydra/launcher/gpu_long.yaml
cp configs/hydra/launcher/quest.yaml configs/hydra/launcher/gpu_long.yaml

# Edit to set GPU and long partition defaults
# Then use:
python train.py env=quest hydra/launcher=gpu_long
```

### Email Notifications

Add email notifications in `configs/hydra/launcher/quest.yaml`:

```yaml
additional_parameters:
  mail-type: "ALL"
  mail-user: "your.email@northwestern.edu"
```

### Module Loading

Set up environment in `configs/hydra/launcher/quest.yaml`:

```yaml
setup:
  - "module load python/3.10"
  - "module load cuda/11.8"
  - "source activate hydra-mnist"
```

### Array Jobs

Run massive parameter sweeps efficiently:

```bash
# This creates an array job with one SLURM job per parameter combination
python train.py -m env=quest \
  model=convnet,mlp \
  training.learning_rate=0.0001,0.001,0.01,0.1 \
  training.batch_size=32,64,128,256
# Creates 2×4×4 = 32 jobs
```

---

## QUEST Partitions

### Available Partitions

| Partition | Max Time | Max CPUs | Max Memory | GPUs | Best For |
|-----------|----------|----------|------------|------|----------|
| `short` | 4 hours | 24 | 64 GB | No | Quick tests |
| `normal` | 48 hours | 52 | 240 GB | No | Standard jobs |
| `long` | 168 hours | 52 | 240 GB | No | Long training |
| `gpu` | 48 hours | 16 | 180 GB | Yes | GPU jobs |
| `gengpu` | 48 hours | 32 | 240 GB | Yes | General GPU |

### Choosing Resources

**For MNIST experiments:**
```bash
# Small model (MLP), CPU-only
python train.py env=quest \
  model=mlp \
  hydra.launcher.partition=short \
  hydra.launcher.gpus_per_node=0 \
  hydra.launcher.cpus_per_task=4 \
  hydra.launcher.mem_gb=8 \
  hydra.launcher.timeout_min=30

# Large model (ConvNet), GPU
python train.py env=quest \
  model=convnet \
  hydra.launcher.partition=gpu \
  hydra.launcher.gpus_per_node=1 \
  hydra.launcher.mem_gb=16 \
  hydra.launcher.timeout_min=60
```

---

## Troubleshooting

### Job Fails Immediately

**Check:**
1. Paths in `configs/env/quest.yaml` are correct
2. You have access to specified directories
3. Conda environment exists and is activated

**Debug:**
```bash
# Check submitit logs
cat .submitit/*_0_log.err

# Try running locally first
python train.py env=local

# Test with minimal resources
python train.py env=quest \
  training.epochs=1 \
  hydra.launcher.timeout_min=10
```

### Out of Memory

**Solution:**
```bash
# Increase memory
python train.py env=quest hydra.launcher.mem_gb=32

# OR reduce batch size
python train.py env=quest training.batch_size=32
```

### Job Timeout

**Solution:**
```bash
# Increase timeout
python train.py env=quest hydra.launcher.timeout_min=120

# OR use longer partition
python train.py env=quest hydra.launcher.partition=normal
```

### Permission Denied

**Check:**
```bash
# Verify directory permissions
ls -la /projects/YOUR_PROJECT_ID/

# Create directories if needed
mkdir -p /projects/YOUR_PROJECT_ID/data
mkdir -p /projects/YOUR_PROJECT_ID/outputs
```

### Module Not Found

**Solution:**
```bash
# Ensure conda environment has all packages
conda activate hydra-mnist
conda list | grep hydra-submitit

# Reinstall if missing
pip install hydra-submitit-launcher==1.2.0
```

---

## Example Workflows

### 1. Quick Test on QUEST

```bash
# Test with 1 epoch on short partition
python train.py env=quest \
  training.epochs=1 \
  hydra.launcher.timeout_min=10
```

### 2. Full Model Comparison

```bash
# Compare both models on both datasets (4 jobs)
python train.py -m env=quest \
  model=convnet,mlp \
  dataset=mnist,fashion_mnist \
  training.epochs=20
```

### 3. Hyperparameter Search

```bash
# Grid search over learning rates and dropouts (9 jobs)
python train.py -m env=quest \
  training.learning_rate=0.0001,0.001,0.01 \
  model.params.dropout=0.3,0.5,0.7 \
  training.epochs=15
```

### 4. GPU Sweep

```bash
# Multiple experiments on GPU partition
python train.py -m env=quest \
  model=convnet \
  training.batch_size=64,128,256 \
  hydra.launcher.partition=gpu \
  hydra.launcher.gpus_per_node=1
```

---

## Tips and Best Practices

1. **Test locally first**: Always verify your code works with `env=local` before submitting to QUEST

2. **Start small**: Test on QUEST with `epochs=1` before running full experiments

3. **Monitor resources**: Check job efficiency with `seff JOBID` after completion

4. **Use appropriate partition**: Don't use `long` partition if job finishes in 1 hour

5. **Batch experiments**: Use multirun (`-m`) to submit many jobs at once

6. **Check quotas**: Verify you have sufficient storage: `quota -s`

7. **Clean up**: Remove old outputs to save space: `rm -rf outputs/old_runs/`

8. **Save configurations**: Hydra saves all configs in `.hydra/config.yaml` for reproducibility

---

## Additional Resources

- [QUEST User Guide](https://services.northwestern.edu/TDClient/30/Portal/KB/)
- [SLURM Documentation](https://slurm.schedmd.com/)
- [Hydra Submitit Plugin](https://hydra.cc/docs/plugins/submitit_launcher/)
- [Northwestern Research Computing](https://www.it.northwestern.edu/research/)

---

## Support

For QUEST-specific issues:
- Email: quest-help@northwestern.edu
- Office Hours: Check [Research Computing website](https://www.it.northwestern.edu/research/)

For Hydra/code issues:
- Check documentation in `docs/` folder
- Review error logs in `.submitit/` directory
