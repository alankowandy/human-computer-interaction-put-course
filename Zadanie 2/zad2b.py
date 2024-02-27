import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path):
    # Wczytanie danych z pliku i zwrócenie informacji
    with open(file_path, 'r') as file:
        w, h, distance = map(int, file.readline().split())
        data = []
        for _ in range(h):
            row = list(map(float, file.readline().split()))
            data.append(row)
    return w, h, distance, np.array(data)

def visualize_map(data):
    # Normalizacja danych
    normed_data = (data - data.min()) / (data.max() - data.min())
    
    # Mapa kolorów do odwzorowanie danych
    cmap = plt.get_cmap('RdYlGn_r')  # Użyj '_r', aby odwrócić mapę kolorów
    mapped_data = cmap(normed_data)

    # Wyświetlenie mapy
    plt.imshow(mapped_data, interpolation='nearest', aspect='auto', cmap='RdYlGn_r')
    plt.colorbar()
    plt.show()

def add_shading(data):
    # Dodanie cieniowania obliczając różnicę między kolejnymi kolumnami
    shaded_data = np.zeros_like(data)
    for i in range(1, data.shape[1]):
        diff = data[:, i] - data[:, i - 1]
        shaded_data[:, i] = diff

    return shaded_data

def visualize_combined(data, shaded_data):
    # Połączenie mapy z mapą cieniowania
    combined_data = data + shaded_data
    
    # Normalizacja połączonych danych dla spójności kolorwania
    normed_data = (combined_data - combined_data.min()) / (combined_data.max() - combined_data.min())
    
    # Mapa kolorów do odwzorowanie danych
    cmap = plt.get_cmap('RdYlGn_r')  # Użyto '_r', aby odwrócić mapę kolorów
    mapped_data = cmap(normed_data)

    # Zapisanie wizualizacji jako plik PDF i wyświetlenie jej z paskiem kolorów
    plt.imshow(mapped_data, interpolation='nearest', aspect='auto', cmap='RdYlGn_r')
    plt.colorbar()
    plt.savefig('map.pdf')
    plt.show()

def main():
    # Główna funkcja do wykonania programu
    file_path = 'big.dem'
    w, h, distance, data = load_data(file_path)

    # Wizualizacja mapy bez cieniowania
    # visualize_map(data)

    # Wizualizacja mapy z cieniowaniem
    shaded_data = add_shading(data)
    visualize_combined(data, shaded_data)

if __name__ == "__main__":
    main()
