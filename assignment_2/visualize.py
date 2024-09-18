import matplotlib.pyplot as plt
import numpy as np


def memory_log(memory, epoch):
    if epoch == 0:  # Initialize memory log at first epoch
        literals = memory.get_literals()
        memory_log_data = {literal: [] for literal in literals}

    # Log current memory values
    for literal in memory.get_literals():
        memory_log_data[literal].append(memory.get_memory()[literal])

# Visualization function to plot memory values after training
def visualize_memory_log(epochs, memory_log_data):
    plt.figure(figsize=(10, 6))
    epochs_range = np.arange(epochs)

    for literal, values in memory_log_data.items():
        plt.plot(epochs_range, values, label=literal)

    plt.title('Feature Memory Values over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Memory Value (0-10)')
    plt.ylim(0, 10)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()