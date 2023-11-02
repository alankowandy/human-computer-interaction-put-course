import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Ścieżki plików do wczytania
file_paths = [
    '1c.csv',
    '1crs.csv',
    '1ers.csv',
    '2c.csv',
    '2crs.csv'
]

# Wczytanie danych z plików do odpowiednich list
loaded_plot_data = [pd.read_csv(path, skiprows=None) for path in file_paths]
loaded_box_data = [pd.read_csv(path, skiprows=None).iloc[-1, 2:] for path in file_paths]

# Utworzenie listy z etykietami
labels = ['1-Coev', '1-Coev-RS', '1-Evol-RS', '2-Coev', '2-Coev-RS']

# Zdefiniowanie funkcji wczytującej
def load_data(file_path):
    return pd.read_csv(file_path, skiprows=None)

# Zdefiniowanie funkcji rysującej wykres plot
def plot_data(data, label, ax):
    ax.plot(data['effort'], data['average'], label=label, markevery=marker_positions,
            marker=markers[label], markersize=6.5, markeredgecolor='black', markeredgewidth=0.7)
    
# Zdefiniowanie funkcji formatującej etykiety osi x
def multiply_labels(x, pos):
    return f'{x*100:.0f}'

# Zdefiniowanie funkcji formatującej etykiety osi y
def divide_labels(x, pos):
    return f'{x/1000:.0f}'

fig, (ax1, ax_boxplot) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 1]}, figsize=(10,8))

plot_attribute_data = load_data(file_paths[0])

marker_positions = range(0, len(plot_attribute_data), 25)

markers = {
    '1-Coev': 's',
    '1-Coev-RS': 'v',
    '1-Evol-RS': 'o',
    '2-Coev': 'd',
    '2-Coev-RS': 'D'
}

# Calculate mean values for sorting
mean_values = [data.iloc[:, 2:].mean(axis=1).mean() for data in loaded_plot_data]

# Sort plot_data and labels based on mean values
sorted_plot_data = [data for _, data in sorted(zip(mean_values, loaded_plot_data), reverse=True)]
sorted_labels = [label for _, label in sorted(zip(mean_values, labels), reverse=True)]

# Rysowanie wykresu plot
for data, label in zip(sorted_plot_data, sorted_labels):
    data_avg = data.iloc[:, 2:].mean(axis=1)
    data['average'] = data_avg
    plot_data(data, label, ax1)

# Rysowanie wykresu plot
# for label, path in zip(labels, file_paths):
#     data = load_data(path)
#     data_avg = data.iloc[:, 2:].mean(axis=1)
#     data['Average'] = data_avg
#     plot_data(data, label, ax1)

# Ustawienie atrybutów wykresu plot
ax1.set(xlim=(0, max(plot_attribute_data['effort'])),
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

ax2.set(xlim=(0, max(plot_attribute_data['generation'])),
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

# Zapis narysowanych wykresów do pliku .pdf
plt.savefig('myplot.pdf')

# Pokazanie narysowanych wykresów na ekranie
plt.show()