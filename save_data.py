import requests
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ESP32 configuration
ESP32_IP = "192.168.0.14"  # Replace with your ESP32's IP address
URL = f"http://{ESP32_IP}/save"

# CSV file name
CSV_FILE = "thermal_data.csv"

def get_thermal_data():
    """Pull thermal data from ESP32 via HTTP request"""
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_csv(data, filename=CSV_FILE):
    """Save thermal data to CSV file"""
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data)

def temperature_to_color(t):
    """Define color based on temperature range"""
    if t < 27.99:
        return (235/255, 131/255, 52/255)  
    elif t < 28.51:
        return (235/255, 195/255, 52/255) 
    elif t < 28.99:
        return (228/255, 235/255, 52/255)  
    elif t < 29.51:
        return (187/255, 235/255, 52/255)  
    elif t < 29.99:
        return (177/255, 235/255, 52/255)  
    elif t < 30.51:
        return (52/255, 235/255, 110/255)  
    elif t < 30.99:
        return (52/255, 235/255, 191/255)  
    elif t < 31.55:
        return (52/255, 235/255, 235/255)  
    elif t < 31.99:
        return (83/255, 213/255, 83/255)  
    elif t < 32.55:
        return (52/255, 177/255, 235/255)  
    elif t < 32.99:
        return (52/255, 142/255, 235/255)  
    elif t < 33.55:
        return (52/255, 112/255, 235/255)  
    elif t < 34.00:
        return (52/255, 83/255, 235/255)  
    elif t < 34.55:
        return (29/255, 63/255, 231/255) 
    elif t < 34.99:
        return (0/255, 0/255, 255/255)  
    elif t < 35.00:
        return (217/255, 39/255, 39/255)  
    else:
        return (2/255, 2/255, 196/255)  

def plot_thermal_image(row_data, timestamp):
    """Plot thermal image from row data"""
    row_data_numeric = pd.to_numeric(row_data[1:], errors='coerce')
    if row_data_numeric.isnull().any():
        print("Error: Non-numeric data found.")
        return

    thermal_data = np.array(row_data_numeric).reshape(24, 32)

    cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', [temperature_to_color(t) for t in np.linspace(27.99, 35.00, 256)], N=256)

    fig, ax = plt.subplots()
    im = ax.imshow(thermal_data, cmap=cmap, interpolation='nearest')
    cbar = plt.colorbar(im)
    cbar.set_label('Temperature (°C)')

    safe_timestamp = timestamp.replace(':', '-')
    plt.title(f'Thermal Image at {timestamp}')
    plt.savefig(f"thermal_image_{safe_timestamp}.png")
    plt.close()

def main():
    # Get and save data
    data = get_thermal_data()
    if data:
        save_to_csv(data)
        print("Data saved to CSV")
    else:
        print("Failed to get data")

    # Read and plot data
    csv_data = pd.read_csv(CSV_FILE, header=None)
    for index, row in csv_data.iterrows():
        timestamp = row[0]
        plot_thermal_image(row, timestamp)

if __name__ == "__main__":
    main()