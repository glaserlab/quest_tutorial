#!/bin/bash

# Quick Start Script for Hydra MNIST Project
# This script demonstrates different ways to use Hydra configuration

echo "=========================================="
echo "Hydra MNIST Project - Quick Start Examples"
echo "=========================================="
echo ""

# Make sure we're in the src directory
cd "$(dirname "$0")/src"

echo "Example 1: Default Configuration (ConvNet on MNIST)"
echo "Command: python train.py"
echo ""

echo "Example 2: Change Model to MLP"
echo "Command: python train.py model=mlp"
echo ""

echo "Example 3: Change Dataset to Fashion-MNIST"
echo "Command: python train.py dataset=fashion_mnist"
echo ""

echo "Example 4: Combine Different Settings"
echo "Command: python train.py model=mlp dataset=fashion_mnist"
echo ""

echo "Example 5: Override Hyperparameters"
echo "Command: python train.py training.learning_rate=0.01 training.batch_size=64"
echo ""

echo "Example 6: Run Multiple Experiments (Multirun)"
echo "Command: python train.py -m model=convnet,mlp dataset=mnist,fashion_mnist"
echo ""

echo "=========================================="
echo "To run any example, copy the command after 'Command:'"
echo "For full documentation, see docs/PROJECT_README.md"
echo "=========================================="
