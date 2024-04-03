import csv
import cv2
import os

def create_raw_data_log(data_extract):
    ### Creates a new csv file in append mode to pass a new line for each frame
    with open('raw_data/raw_log.csv', mode="a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_extract)

def create_damage_lists_log(data_extract):
    with open('raw_data/data_lists_log.csv', mode="a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_extract)

def create_processed_data_log(data_extract):
    with open('raw_data/processed_log.csv', mode="a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_extract)

def refresh_logs(vid_name):
    if os.path.exists("raw_data/raw_log.csv"):
        os.remove("raw_data/raw_log.csv")
    if os.path.exists("raw_data/processed_log.csv"):
        os.remove("raw_data/processed_log.csv")
    if os.path.exists(f"raw_data/{vid_name}"):
        for x in os.listdir(f"raw_data/{vid_name}"):
            os.remove(f"raw_data/{vid_name}"+"/"+x)
        os.rmdir(f"raw_data/{vid_name}")

def draw_boxes(data_extract, frame, output_folder, frame_count):
    ###Get the bounding boxes from the data_extract and store them in a list
    bounding_boxes = []
    for x in range(len(data_extract)):
        bounding_boxes.append([(int(data_extract[x][0][0][0]), int(data_extract[x][0][0][1])),\
            (int(data_extract[x][0][2][0]), int(data_extract[x][0][2][1]))])

    ###Apply all the bounding_boxes to the corresponding frame
    counter = 0
    for x in range(len(bounding_boxes)):
        counter += 1
        boxed_image = cv2.rectangle(frame, bounding_boxes[x][0], bounding_boxes[x][1], (0,0,255), 2)
        boxed_image = cv2.putText(
            img = boxed_image,
            text = str(counter),
            org = ((bounding_boxes[x][0][0] - 40), (bounding_boxes[x][0][1] + 20)),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1.0,
            color =  (255,255,255),
            thickness = 1,
            lineType = cv2.LINE_AA
        )


    ###Create new folder to store the image
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ###Create image name with a new count
    img_name = f'frame_{frame_count}.png'

    ### Push each image to a new folder
    img_path = os.path.join(output_folder, img_name)

    ###Save image
    cv2.imwrite(img_path, boxed_image)
    print(f"created {img_name} stored in {output_folder}")
