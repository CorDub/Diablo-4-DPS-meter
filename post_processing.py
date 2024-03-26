def extract(data):
    data_extract=[]
    for x in data:
        data_extract.append(x[1])
    return data_extract

def remove_commas(data_extract):
    for i, x in enumerate(data_extract):
        data_extract[i] = x.replace(',','')
    return data_extract

def final_number(data_extract):
    final_numbers = []
    for x in data_extract:
        if x.isdigit():
            final_numbers.append(int(x))
    return sum(final_numbers)
