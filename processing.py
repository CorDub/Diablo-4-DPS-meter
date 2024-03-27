import easyocr
import numpy as np
import os
import post_processing

reader = easyocr.Reader(['en'], gpu=True)
directory = os.fsencode("raw_data/Frames video 25")

frame_damage = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    image_path = os.path.join(str(directory)[2:-1], filename)
    result = reader.readtext(image_path)
    data_extract = post_processing.extract(result)
    data = post_processing.remove_commas(data_extract)
    final_number = post_processing.final_number(data)
    # print(final_number)
    frame_damage.append(final_number)

dps =  []
for x in range(0, len(frame_damage), 5):
    dps.append(sum(frame_damage[x:x+5]))

print(dps)
print(sum(dps)/len(dps))
