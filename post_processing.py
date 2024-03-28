def extract(data):
    data_extract=[]
    for x in data:
        data_extract.append(x[1])
    return data_extract

def change_obvious_letters_to_numbers(data_extract):
    for i, x in enumerate(data_extract):
        x = x.replace('S', '5').replace('s', '5')
        x = x.replace('L', '1').replace('l', '1').replace('I', '1').replace('i', '1')
        x = x.replace('O', '0').replace('o', '0')
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

def truncate_long_numbers(data_extract):
    for i, x in enumerate(data_extract):
        if x.isdigit() and len(x) > 7:
            data_extract[i] = x[:7]
    return data_extract

def final_number(data_extract):

    data_extract = truncate_long_numbers(data_extract)

    final_numbers = []
    for x in data_extract:
        if x.isdigit():
            final_numbers.append(int(x))
    return sum(final_numbers)
