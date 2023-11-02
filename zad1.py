import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Ścieżki plików do wczytania
file_paths = [
    '/home/alan/Downloads/1c.csv',
    '/home/alan/Downloads/1crs.csv',
    '/home/alan/Downloads/1ers.csv',
    '/home/alan/Downloads/2c.csv',
    '/home/alan/Downloads/2crs.csv'
]

loaded_plot_data = [pd.read_csv(path, skiprows=None) for path in file_paths]
loaded_box_data = [pd.read_csv(path, skiprows=None).iloc[-1, 2:] for path in file_paths]

labels = ['1-Coev', '1-Coev-RS', '1-Evol-RS', '2-Coev', '2-Coev-RS']



# for i in range(len(file_paths)):
#     plot_data.append(loaded_plot_data[i])

# data1 = loaded_plot_data[0]
# data2 = loaded_plot_data[1]
# data3 = loaded_plot_data[2]
# data4 = loaded_plot_data[3]
# data5 = loaded_plot_data[4]

# data1_box = pd.read_csv(file_path1, skiprows=None)
# data2_box = pd.read_csv(file_path2, skiprows=None)
# data3_box = pd.read_csv(file_path3, skiprows=None)
# data4_box = pd.read_csv(file_path4, skiprows=None)
# data5_box = pd.read_csv(file_path5, skiprows=None)

#data1_avg = data1.iloc[:, 2:].mean(axis=1)
# print(data1_avg)
# data2_avg = data2.iloc[:, 2:].mean(axis=1)
# data3_avg = data3.iloc[:, 2:].mean(axis=1)
# data4_avg = data4.iloc[:, 2:].mean(axis=1)
# data5_avg = data5.iloc[:, 2:].mean(axis=1)

# data1_box = loaded_box_data[0]
# data2_box = loaded_box_data[1]
# data3_box = loaded_box_data[2]
# data4_box = loaded_box_data[3]
# data5_box = loaded_box_data[4]

#data1['Average'] = data1_avg
# data2['Average'] = data2_avg
# data3['Average'] = data3_avg
# data4['Average'] = data4_avg
# data5['Average'] = data5_avg

def load_data(file_path):
    return pd.read_csv(file_path, skiprows=None)

plot_data = load_data(file_paths[0])

def plot_data(data, label, ax):
    ax.plot(data['effort'], data['Average'], label=label, markevery=marker_positions,
            marker=markers[label], markersize=6.5, markeredgecolor='black', markeredgewidth=0.7)
    
def multiply_labels(x, pos):
    return f'{x*100:.0f}'

def divide_labels(x, pos):
    return f'{x/1000:.0f}'

fig, (ax1, ax_boxplot) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 1]}, figsize=(10,8))

marker_positions = range(0, len(loaded_plot_data[0]), 25)

markers = {
    '1-Coev': 's',
    '1-Coev-RS': 'v',
    '1-Evol-RS': 'o',
    '2-Coev': 'd',
    '2-Coev-RS': 'D'
}

# Rysowanie wykresu plot
for label, path in zip(labels, file_paths):
    data = load_data(path)
    data_avg = data.iloc[:, 2:].mean(axis=1)
    data['Average'] = data_avg
    plot_data(data, label, ax1)

# Ustawienie atrybutów wykresu plot
ax1.set(xlim=(0, max(plot_data['effort'])),
        ylim=(0.6, 1.0),
        xlabel='Rozegranych gier (x1000)',
        ylabel='Odsetek wygranych gier [%]',)

ax1.tick_params(axis='both', which='both', direction='in', pad=7)
ax1.legend(loc = 'lower right')

formatter = FuncFormatter(multiply_labels)
ax1.yaxis.set_major_formatter(formatter)
formatter = FuncFormatter(divide_labels)
ax1.xaxis.set_major_formatter(formatter)

ax1.grid(True, linestyle=(0, (1, 5)), linewidth='1')

# Ustawienie górnej osi 'pokolenie'
ax2 = ax1.twiny()

ax2.set(xlim=(0, max(plot_data['generation'])),
        xticks=[0, 40, 80, 120, 160, 200],
        xticklabels=['0', '40', '80', '120', '160', '200'],
        xlabel='Pokolenie')

ax2.tick_params(axis='both', which='both', direction='in', pad=5)

# Utworzenie pustej listy dla wczytanych danych wykresu pudełkowego
box_data = []

# Wczytanie odpowiednich danych do listy box_data
for i in range(len(file_paths)):
    box_data.append(loaded_box_data[i])

# Sortowanie danych wykresu pudełkowego
sorted_box_data = sorted(box_data, key=lambda x: x.mean(), reverse=True)

# Utworzenie listy z etykietami oraz pustej listy dla odpowiednio posortowanych etykiet
labels = ['1-Coev', '1-Coev-RS', '1-Evol-RS', '2-Coev', '2-Coev-RS']

sorted_labels = []

# Sortowanie etykiet wykresu pudełkowego na podstawie wcześniej posortowanych danych
for data in sorted_box_data:
    for i, loaded_data_i in enumerate(loaded_box_data):
        if data.equals(loaded_data_i):
            sorted_labels.append(labels[i])
            break

# Rysowanie wykresu pudełkowego
boxplot = ax_boxplot.boxplot(sorted_box_data, 
                             showmeans=True, 
                             notch=True, 
                             patch_artist=True)

ax_boxplot.set(xticklabels=sorted_labels, ylim=(0.6, 1.0))
ax_boxplot.yaxis.tick_right()
ax_boxplot.tick_params(axis='both', which='both', direction='in', pad=5)

formatter = FuncFormatter(multiply_labels)
ax_boxplot.yaxis.set_major_formatter(formatter)

for mean in boxplot['means']:
    mean.set(marker='o', markerfacecolor='blue', markeredgecolor='black')

for median in boxplot['medians']:
    median.set(color='red', linewidth=2)

for label in ax_boxplot.get_xticklabels():
    label.set(rotation=45)
    
for patch in boxplot['boxes']:
    patch.set(facecolor='none', edgecolor='blue', linewidth=1.5)

for whisker in boxplot['whiskers']:
    whisker.set(linestyle=(0, (5, 7)), color='blue', linewidth=1.5)

for flier in boxplot['fliers']:
    flier.set(marker='+', markeredgecolor="blue", markersize=8)

ax_boxplot.grid(True, linestyle=(0, (1, 5)), linewidth='1')

plt.savefig('myplot.pdf')
plt.show()