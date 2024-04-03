import random
import os

def random_number_generator(number_of_numbers: int, max_number_possible: int):
    numbers = []

    ### Generate numbers
    for x in range(number_of_numbers):
        numbers.append(random.randint(1,max_number_possible))

    ### Add a comma separator for thousands
    for i, x in enumerate(numbers):
        numbers[i] = "{:,}".format(x)

    ### save each number to a text file on its own line
    for x in numbers:
        with open("raw_data/training_dataset/training_dataset.txt", "a") as file:
            file.write(str(x))
            file.write('\n')
        print(f"{x} saved to training_dataset.txt")

# random_number_generator(100,10000)

def create_gt_file(folder):
    folder_encoded = os.fsencode(folder)
    for file in os.listdir(folder_encoded):
        filename=os.fsdecode(file)
        # image_path = os.path.join(str(folder_encoded)[2:-1], filename)
        with open("raw_data/training_dataset/gt.txt", "a") as file:
            file.write(f'{filename}\t{filename[:-7]}\n')
        print(f'{filename} saved to gt/txt')

create_gt_file("raw_data/training_dataset/test")
