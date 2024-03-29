import easyocr
import numpy as np
import os
import post_processing

reader = easyocr.Reader(['en'], gpu=True)

def process_video(directory):
    directory_encoded = os.fsencode(directory)
    frame_damage = []

    for file in os.listdir(directory_encoded):
        filename = os.fsdecode(file)
        image_path = os.path.join(str(directory_encoded)[2:-1], filename)
        result = reader.readtext(image_path)
        data_extract = post_processing.extract(result)
        data = post_processing.remove_commas(data_extract)
        final_number = post_processing.final_number(data)
        frame_damage.append(final_number)

    dps =  []
    for x in range(0, len(frame_damage), 5):
        dps.append(sum(frame_damage[x:x+5]))

    return frame_damage, dps, sum(dps)/len(dps)

def process(image):
    result = reader.readtext(image)
    data_extract = post_processing.extract(result)
    data = post_processing.remove_commas(data_extract)
    final_number = post_processing.final_number(data)
    return final_number
