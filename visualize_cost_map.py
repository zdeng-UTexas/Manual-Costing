import numpy as np
import matplotlib.pyplot as plt
import argparse

# Parse command line arguments for the CSV file path
parser = argparse.ArgumentParser(description="Visualize a cost map from a CSV file.")
parser.add_argument("csv_file", type=str, help="Path to the CSV file containing the cost map.")
args = parser.parse_args()

def load_cost_map(csv_file):
    return np.loadtxt(csv_file, delimiter=',')

def visualize_cost_map(cost_map):
    plt.imshow(cost_map, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.show()

def main():
    cost_map = load_cost_map(args.csv_file)
    visualize_cost_map(cost_map)

if __name__ == "__main__":
    main()
