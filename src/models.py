import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvNet(nn.Module):
    """Convolutional Neural Network for image classification."""
    
    def __init__(self, num_classes=10, input_channels=1, conv_channels=[32, 64], 
                 fc_hidden=128, dropout=0.5):
        super(ConvNet, self).__init__()
        
        self.conv1 = nn.Conv2d(input_channels, conv_channels[0], kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(conv_channels[0], conv_channels[1], kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout1 = nn.Dropout2d(dropout)
        
        # Calculate flattened size after conv layers (28x28 -> 14x14 -> 7x7)
        self.fc1 = nn.Linear(conv_channels[1] * 7 * 7, fc_hidden)
        self.dropout2 = nn.Dropout(dropout)
        self.fc2 = nn.Linear(fc_hidden, num_classes)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.dropout1(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)
        return x


class MLP(nn.Module):
    """Multi-Layer Perceptron for image classification."""
    
    def __init__(self, num_classes=10, input_size=784, hidden_sizes=[256, 128], dropout=0.3):
        super(MLP, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, num_classes))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.network(x)


def create_model(model_type, **kwargs):
    """Factory function to create models."""
    if model_type == "convnet":
        return ConvNet(**kwargs)
    elif model_type == "mlp":
        return MLP(**kwargs)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
