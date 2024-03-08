import os
import matplotlib.pyplot as plt
from collections import Counter
import json
from . import Path

class DataPlotter:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.data = []

    def load_data_from_directory(self):
        self.data = []  # Clear any previous data
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if not file.endswith(".json"):
                    continue

                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    self._process_json_file(json_file)

    def _process_json_file(self, json_file):
        diff_per_frame = json.load(json_file)
        for j in diff_per_frame["dpf"]:
            for i in j:
                if i == 0:
                    continue
                self.data.append(i)

    def plot_data(self):
        if not self.data:
            print("No data to plot. Please load data first.")
            return

        # Count the frequency of each unique value
        data_counter = Counter(self.data)

        # Extract unique values and their frequencies
        unique_values = list(data_counter.keys())
        frequencies = list(data_counter.values())

        # Create a bar plot
        plt.bar(unique_values, frequencies)

        # Add labels and title
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.title("Frequency of Unique Values")

        # Show the plot
        plt.show()


def main():
    directory_path = os.path.join(Path.data, "dpf")  # Adjust the directory path
    plotter = DataPlotter(directory_path)
    plotter.load_data_from_directory()
    plotter.plot_data()

if __name__ == '__main__':
    main()