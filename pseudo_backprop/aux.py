"""Standalone functions for auxillary computations."""
import numpy as np
import torch


def evaluate_model(network_model, testloader, batch_size):
    """
    Evaluate the model on the given dataset and obtain the loss function and
    the results

    Params:
        network_model: FullyConnectedNetwork object containing the neural
                       network
        testloader: the testloader object from torch
        batch_size: batch size

    Returns:
        loss: the computed loss value
        confusion_matrix: numpy matrix with the confusion matrix
    """

    confusion_matrix = np.zeros((10, 10))
    loss_function = torch.nn.CrossEntropyLoss()
    loss = 0
    # turn off gathering the gradient for testing
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images = images.view(batch_size, -1)
            outputs = network_model(images)
            loss_value = loss_function(outputs, labels)
            loss += loss_value
            _, predicted = torch.max(outputs, 1)
            for tested in zip(labels.numpy().astype(int),
                              predicted.numpy().astype(int)):
                confusion_matrix[tested] += 1

    return loss, confusion_matrix