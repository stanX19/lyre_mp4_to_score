import matplotlib.pyplot as plt
from collections import Counter
import json

diff_data_path = r'C:\Users\DELL\PycharmProjects\pythonProject\mp4_to_lyre\srcs\data\diff_per_frame.json'
data = []

with open(diff_data_path, 'r') as json_file:
    diff_per_frame = json.load(json_file)
    for j in diff_per_frame:
        for i in j:
            if i > 0:
                data.append(i)

# with open("brightness.txt") as f:
#     data = []
#     for line in f:
#         data.append(int(line))

# Count the frequency of each unique value
data_counter = Counter(data)

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