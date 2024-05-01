import numpy as np 
import matplotlib.pyplot as plt 

label = ("ZeroR","1R","1NN","5NN","NB","DT","MLP","SVM","RF")
Pima = [65.19, 70.79, 69.75, 75.62, 74.71, 74.58, 75.1, 76.4, 77.44]
Occ = [81.27, 98.47, 99.51, 99.51, 96.79, 99.51, 99.31, 98.42, 99.7]

Pima_CFS = [65.19, 70.79, 67.93, 74.97, 76.66, 75.23, 77.7, 77.05, 74.45]
Occ_CFS = [81.27, 98.47, 99.6, 99.46, 98.47, 99.6, 98.96, 98.42, 99.7]

dataset = {
    "Pima": Pima,
    "Pima_CFS": Pima_CFS
}

# dataset = {
#     "Occupancy": Occ,
#     "Occupancy_CFS": Occ_CFS
# }

y = np.arange(len(label))  # the label locations
width = 0.4  # the width of the bars


fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size here
for attribute, measurement in dataset.items():
    rects = ax.barh(y + width * len(ax.containers), measurement, width, label=attribute)
    ax.bar_label(rects, padding=-30, fontsize='small')  # Adjust padding here for better visibility

ax.set_xlabel('Accuracy (%)')
ax.set_title(' Accuracy Comparison between Original and CFS - Room Occupancy')
ax.set_yticks(y + width / 2)
ax.set_yticklabels(label)
ax.set_xlim(0, 100)  # Set x-axis limit from 0 to 100
ax.grid(True)  # Add gridlines

# Position the legend outside of the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
