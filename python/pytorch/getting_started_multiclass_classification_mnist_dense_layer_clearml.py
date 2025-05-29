#!/usr/bin/env python3
# coding: utf-8

# Source: https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html#

import argparse
from clearml import Task
import json
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sklearn.metrics import confusion_matrix
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.tensorboard import SummaryWriter
from typing import Optional
import safetensors.torch


# CONFIGURATION ###############################################################

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for MNIST classification.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='MNIST Classification with PyTorch')
    parser.add_argument('--batch-size', type=int, default=64, help='Batch size for training')
    parser.add_argument('--epochs', type=int, default=15, help='Number of epochs')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--device', type=str, default='auto', choices=['auto', 'cpu', 'cuda', 'mps'], help='Device to use')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--save-interval', type=int, default=5, help='Save model every N epochs')
    parser.add_argument('--patience', type=int, default=5, help='Early stopping patience')
    parser.add_argument('--dropout-rate', type=float, default=0.2, help='Dropout rate')
    parser.add_argument('--model-path', type=Path, default=Path('mnist_model_final.safetensors'), help='Path to save the final model')
    return parser.parse_args()


# SETUP LOGGING ###############################################################

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger: logging.Logger = logging.getLogger(__name__)


# REPRODUCIBILITY #############################################################

def set_seed(seed: int) -> None:
    """
    Set random seed for reproducibility.

    Parameters
    ----------
    seed : int
        The random seed to use.
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


# DEVICE SELECTION ############################################################

def get_device(device_preference: str) -> torch.device:
    """
    Select the appropriate torch device based on user preference and availability.

    Parameters
    ----------
    device_preference : str
        Device preference: 'auto', 'cpu', 'cuda', or 'mps'.

    Returns
    -------
    torch.device
        The selected device.
    """
    if device_preference == 'auto':
        if torch.cuda.is_available():
            return torch.device('cuda')
        elif torch.backends.mps.is_available():
            return torch.device('mps')
        else:
            return torch.device('cpu')
    return torch.device(device_preference)


# DEFINE MODELS ###############################################################

class NeuralNetwork(nn.Module):
    """
    Simple feedforward neural network for MNIST classification.

    Parameters
    ----------
    dropout_rate : float, optional
        Dropout rate to use in dropout layers (default is 0.).

    Attributes
    ----------
    flatten : nn.Flatten
        Layer to flatten input images.
    linear_relu_stack : nn.Sequential
        Sequential stack of linear, ReLU, and dropout layers.
    """
    def __init__(self, dropout_rate: float=0.) -> None:
        super().__init__()

        self.flatten: nn.Flatten = nn.Flatten()

        self.linear_relu_stack: nn.Sequential = nn.Sequential(
            nn.Linear(28*28, 64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 10)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the neural network.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape (batch_size, 1, 28, 28).

        Returns
        -------
        torch.Tensor
            Output logits tensor of shape (batch_size, 10).
        """
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


# DEFINE THE TRAINING LOOP ####################################################

def train_one_epoch(
    dataloader: DataLoader, 
    model: nn.Module, 
    loss_fn: nn.Module, 
    optimizer: torch.optim.Optimizer, 
    epoch: int, 
    device: torch.device, 
    writer: SummaryWriter
) -> tuple[float, float]:
    """
    Train the model for one epoch.

    Parameters
    ----------
    dataloader : DataLoader
        DataLoader for the training data.
    model : nn.Module
        The neural network model.
    loss_fn : nn.Module
        Loss function.
    optimizer : torch.optim.Optimizer
        Optimizer for model parameters.
    epoch : int
        Current epoch number.
    device : torch.device
        Device to run computations on.
    writer : SummaryWriter
        TensorBoard SummaryWriter for logging.

    Returns
    -------
    tuple of float
        Average loss and accuracy for the epoch.
    """
    dataset_size: int = len(dataloader.dataset)

    # Set the model to training mode (this enables dropout and batch normalization)
    model.train()

    total_loss: float = 0
    correct: int = 0

    for batch_idx, (X, y_true) in enumerate(dataloader):
        X, y_true = X.to(device), y_true.to(device)

        # Compute prediction error
        y_pred: torch.Tensor = model(X)
        train_loss: torch.Tensor = loss_fn(y_pred, y_true)

        # Backpropagation
        train_loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Statistics
        total_loss += train_loss.item()
        correct += (y_pred.argmax(1) == y_true).type(torch.float).sum().item()

        # Print status
        if batch_idx % 100 == 0:
            current_loss: float = train_loss.item()
            train_step: int = (batch_idx + 1) * len(X)
            logger.info(f"loss: {current_loss:>7f}  [{train_step:>5d}/{dataset_size:>5d}]")

            # # Log the loss values to TensorBoard
            # global_step: int = epoch * len(dataloader) + batch_idx
            # writer.add_scalar('Loss/train_batch', current_loss, global_step)

    # Log epoch metrics
    avg_loss: float = total_loss / len(dataloader)
    accuracy: float = 100. * correct / dataset_size
    writer.add_scalar('Loss/train', avg_loss, epoch)
    writer.add_scalar('Accuracy/train', accuracy, epoch)

    return avg_loss, accuracy


# DEFINE THE TESTING LOOP #####################################################

def evaluate(
    dataloader: DataLoader,
    model: nn.Module,
    loss_fn: nn.Module,
    device: torch.device,
) -> tuple[float, float, list[int], list[int]]:
    """
    Evaluate the model on the validation/test dataset.

    Parameters
    ----------
    dataloader : DataLoader
        DataLoader for the test data.
    model : nn.Module
        The neural network model.
    loss_fn : nn.Module
        Loss function.
    device : torch.device
        Device to run computations on.

    Returns
    -------
    tuple of float and list
        Average loss and accuracy, along with lists of true labels and predicted labels.
    """
    dataset_size: int = len(dataloader.dataset)
    num_batches: int = len(dataloader)
    test_loss: float = 0
    correct: int = 0

    all_preds: list[int] = []
    all_labels: list[int] = []

    model.eval()

    with torch.no_grad():
        for X, y_true in dataloader:
            X, y_true = X.to(device), y_true.to(device)
            y_pred: torch.Tensor = model(X)
            test_loss += loss_fn(y_pred, y_true).item()

            pred_labels: torch.Tensor = y_pred.argmax(1)
            correct += (pred_labels == y_true).type(torch.float).sum().item()

            all_preds.extend(pred_labels.cpu().numpy())
            all_labels.extend(y_true.cpu().numpy())

    test_loss /= num_batches
    test_accuracy: float = 100. * correct / dataset_size

    logger.info(f"Test Error: Accuracy: {test_accuracy:>0.1f}%, Avg loss: {test_loss:>8f}")

    return test_loss, test_accuracy, all_labels, all_preds


# MAIN EXECUTION ###############################################################

def train_model(args: argparse.Namespace) -> None:
    """
    Train the neural network model on the MNIST dataset.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments containing training configuration.
    """

    # Set seed for reproducibility
    set_seed(args.seed)

    # INITIALIZING CLEARML TASK ###############################################

    task: Optional[Task] = None
    try:
        # Always initialize ClearML before anything else to let automatic hooks track as much as possible
        task = Task.init(
            project_name="Snippets",
            task_name="MNIST Dense Layers"
        )
        logger.info("ClearML task initialized successfully")
        # # Connect argparse arguments to ClearML
        # # This will log hyperparameters and allow modification from ClearML UI if run by an agent
        # task.connect(args, name='Hyperparameters')
        # # Note: If run by clearml-agent, 'args' might be updated in-place by task.connect
        # # To be certain about using potentially overridden args, you might re-fetch them:
        # # effective_args_dict = task.get_configuration_object(name='Hyperparameters')
        # # args = argparse.Namespace(**effective_args_dict) # Or update existing args
        # logger.info(f"Hyperparameters connected to ClearML: {args}")
    except Exception as e:
        logger.warning(f"Failed to initialize ClearML task: {e}")

    # INITIALIZING TENSORBOARD SUMMARYWRITER ##################################

    runs_dir = Path('runs')
    runs_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=runs_dir)
    logger.info("TensorBoard SummaryWriter initialized")
    logger.info(f"To visualize: tensorboard --logdir={runs_dir} then open http://localhost:6006/")

    # DOWNLOAD THE MNIST DATASET ##############################################

    data_dir = Path("data")
    try:
        training_data = datasets.MNIST(root=data_dir, train=True, download=True, transform=ToTensor())
        test_data = datasets.MNIST(root=data_dir, train=False, download=True, transform=ToTensor())
        logger.info("MNIST dataset loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load MNIST dataset: {e}")
        return

    # INSTANTIATE DATALOADERS #################################################

    train_dataloader = DataLoader(training_data, batch_size=args.batch_size, shuffle=True)
    test_dataloader = DataLoader(test_data, batch_size=args.batch_size)

    # CREATING MODELS #########################################################

    device: torch.device = get_device(args.device)
    logger.info(f"Using device: {device}")

    model = NeuralNetwork(dropout_rate=args.dropout_rate).to(device)
    logger.info(f"Model created with {sum(p.numel() for p in model.parameters())} parameters")

    # OPTIMIZE THE MODEL PARAMETERS ###########################################

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    # TRAIN THE MODEL #########################################################

    best_accuracy: float = 0
    patience_counter: int = 0

    # Create checkpoint directory
    checkpoints_dir = Path('checkpoints')
    checkpoints_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(args.epochs):
        logger.info(f"Epoch {epoch+1}/{args.epochs}")
        logger.info("-" * 50)

        train_loss: float
        train_acc: float
        train_loss, train_acc = train_one_epoch(train_dataloader, model, loss_fn, optimizer, epoch, device, writer)

        test_loss: float
        test_accuracy: float
        test_loss, test_accuracy, all_labels, all_preds = evaluate(test_dataloader, model, loss_fn, device)

        # Log the metrics to TensorBoard
        writer.add_scalar('Loss/test', test_loss, epoch)
        writer.add_scalar('Accuracy/test', test_accuracy, epoch)

        # Log confusion matrix to ClearML
        if task:
            cm = confusion_matrix(all_labels, all_preds, labels=list(range(10))) # Assuming 10 classes for MNIST
            task.get_logger().report_confusion_matrix(
                title="Confusion Matrix",
                series="Test Performance", # Grouping for ClearML plots
                iteration=epoch,
                matrix=cm,
                xaxis="Predicted",
                yaxis="Actual",
                xlabels=[str(i) for i in range(10)],
                ylabels=[str(i) for i in range(10)]
            )

        # Early stopping
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            patience_counter = 0
            # Save best model
            safetensors.torch.save_model(model, checkpoints_dir / 'best_model.safetensors')
            # Save metadata separately
            metadata = {
                'epoch': epoch,
                'best_accuracy': best_accuracy,
                'train_loss': train_loss,
                'test_loss': test_loss,
                'test_accuracy': test_accuracy,
            }
            with open(checkpoints_dir / 'best_model_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"New best model saved with accuracy: {best_accuracy:.2f}%")
            if task:
                task.upload_artifact(name='best_model', artifact_object=checkpoints_dir / 'best_model.safetensors')
                task.upload_artifact(name='best_model_metadata', artifact_object=checkpoints_dir / 'best_model_metadata.json')
                logger.info("Best model uploaded as ClearML artifact")
        else:
            patience_counter += 1

        if patience_counter >= args.patience:
            logger.info(f"Early stopping triggered after {epoch+1} epochs")
            break

        # Save checkpoint
        if (epoch + 1) % args.save_interval == 0:
            safetensors.torch.save_model(model, checkpoints_dir / f'checkpoint_epoch_{epoch+1}.safetensors')
            # Save metadata separately
            metadata = {
                'epoch': epoch,
                'train_loss': train_loss,
                'test_loss': test_loss,
                'test_accuracy': test_accuracy,
            }
            with open(checkpoints_dir / f'checkpoint_epoch_{epoch+1}_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Checkpoint saved at epoch {epoch+1}")
            if task:
                task.upload_artifact(name=f'checkpoint_epoch_{epoch+1}', artifact_object=checkpoints_dir / f'checkpoint_epoch_{epoch+1}.safetensors')
                task.upload_artifact(name=f'checkpoint_epoch_{epoch+1}_metadata', artifact_object=checkpoints_dir / f'checkpoint_epoch_{epoch+1}_metadata.json')
                logger.info(f"Checkpoint epoch {epoch+1} uploaded as ClearML artifact")


    # Closing SummaryWriter
    writer.close()
    logger.info("Training completed")

    # SAVE THE FINAL MODEL ####################################################

    safetensors.torch.save_model(model, args.model_path)
    logger.info("Final model saved")
    if task:
        task.upload_artifact(name='final_model', artifact_object=args.model_path)
        logger.info("Final model uploaded as ClearML artifact")


def test_model(args: argparse.Namespace) -> None:
    """
    Test the trained model on a subset of the MNIST test dataset and report predictions.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments containing configuration and model path.
    """
    device: torch.device = get_device(args.device)
    logger.info(f"Using device: {device}")

    # Load the model (safetensors format)
    model = NeuralNetwork()
    try:
        safetensors.torch.load_model(model, args.model_path)
        logger.info(f"Model loaded from {args.model_path}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return

    model.to(device)
    model.eval()

    # Load MNIST test dataset
    test_data = datasets.MNIST(root="data", train=False, download=True, transform=ToTensor())

    # Take the first 16 images for inference
    n_samples = 16
    images, labels = zip(*[test_data[i] for i in range(n_samples)])
    images_tensor = torch.stack(images).to(device)

    with torch.no_grad():
        outputs = model(images_tensor)
        preds = outputs.argmax(dim=1).cpu().numpy()

    # Display with matplotlib
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for i, ax in enumerate(axes.flat):
        img = images[i].squeeze().cpu().numpy()
        ax.imshow(img, cmap='gray')
        ax.set_title(f"Pred: {preds[i]}, True: {labels[i]}")
        ax.axis('off')
    plt.tight_layout()

    # Save the figure temporarily
    fig_path = "mnist_predictions.png"
    plt.savefig(fig_path)
    plt.close(fig)

    # Report the image to ClearML if possible
    try:
        task = Task.current_task()
        if task:
            task.get_logger().report_image(
                title="MNIST Predictions",
                series="Test Samples",
                local_path=fig_path,
                iteration=0
            )
            logger.info("Sample predictions reported to ClearML")
    except Exception as e:
        logger.warning(f"Could not report image to ClearML: {e}")

    logger.info("Sample predictions completed")


if __name__ == "__main__":
    """
    Main entry point for training and testing the MNIST classifier.
    """
    try:
        # Parse command line arguments
        args: argparse.Namespace = parse_args()

        # Train the model
        train_model(args)

        # Test the model
        test_model(args)
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
