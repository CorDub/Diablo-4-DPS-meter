import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO

def extract(data):
    data_extract = []
    for x in data:
        if x[2] > 0.2:  # Remove low confidence numbers
            data_extract.append(x[1])
    return data_extract


def change_obvious_letters_to_numbers(data_extract):
    for i, x in enumerate(data_extract):
        x = x.replace('S', '5').replace('s', '5')
        x = x.replace('L', '1').replace('l', '1').replace('I', '1').replace('i', '1')
        x = x.replace('O', '0').replace('o', '0').replace('u', '0')
        x = x.replace('B', '8')
        x = x.replace('G', '8')
        data_extract[i] = x
    return data_extract

def remove_commas(data_extract):
    for i, x in enumerate(data_extract):
        if ',' in x:
            parts = x.split(',')
            if len(parts) == 2:
                if len(parts[1]) == 2:
                    parts[1] += '0'
                    x = ','.join(parts)
        data_extract[i] = x.replace(',', '')
    return data_extract

def remove_specific_symbols(data_extract):
    symbols_to_remove = "-',_}\*:;]"
    for i, x in enumerate(data_extract):
        for symbol in symbols_to_remove:
            x = x.replace(symbol, '')
        data_extract[i] = x
    return data_extract

def truncate_long_numbers(data_extract):
    for i, x in enumerate(data_extract):
        if x.isdigit() and len(x) > 6:
            data_extract[i] = x[:6]
    return data_extract

def final_number(data_extract):

    data_extract = truncate_long_numbers(data_extract)

    final_numbers = []
    for x in data_extract:
        if x.isdigit():
            final_numbers.append(int(x))
    return final_numbers

def delete_duplicates(damage_lists):
    new_data=[]
    for i, x in enumerate(damage_lists):
        for y in x:
            if not y in damage_lists[i-1]:
                new_data.append(y)
    return sum(new_data)

def create_plot(time_stamps, damage_values):
    ### Create plot
    plt.figure(figsize=(10, 5))
    plt.plot(time_stamps, damage_values, label='Damage Per Frame')
    plt.plot(time_stamps, np.cumsum(damage_values), label='Cumulative Damage')
    plt.xlabel('Time (s)')
    plt.ylabel('Damage')
    plt.title('Damage Over Time')
    plt.legend()
    plt.grid(True)

    # Convert the graph to an in-memory image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Open the image from bytes using Pillow
    plt_image = Image.open(buffer)
    return plt_image
