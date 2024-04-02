import easyocr
import cv2
from pre_processing import preprocess
from post_processing import extract, change_obvious_letters_to_numbers, remove_commas, remove_specific_symbols, truncate_long_numbers, final_number, delete_duplicates, create_plot
from log import create_processed_data_log, create_raw_data_log, refresh_logs, draw_boxes

reader = easyocr.Reader(['en'], gpu=True)

def process_video_and_display_results(video):
    ### Check if argument passed is a video
    if isinstance(video, str):
        cap = cv2.VideoCapture(video)
    else:
        cap = cv2.VideoCapture(video.name)

    ### Prepare necessary video variables:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(fps / 4), 1)  # 4 frames per second
    time_stamps = []
    vid_name = video
    frame_count = 0

    ### Prepare necessary post-processing variables:
    frame_damage = []
    damage_values = []
    damage_lists = []

    ### Delete logs before creating new ones:
    refresh_logs(vid_name)

    ### Start processing frames
    while cap.isOpened():
        ret, frame = cap.read()

        ### Count the frames
        frame_count +=1

        ### Break when there is no more frames
        if not ret:
                break

        ### Set processing at 4 frames per second:
        for _ in range(frame_interval - 1):
            cap.read()

        ### preprocess the frame
        image = preprocess(frame)

        ### pass the frame through the model
        result = reader.readtext(image)

        ### first log: draw bounding boxes for detected text
        draw_boxes(result, image, f"raw_data/{vid_name}", frame_count)

        ### extract text from results
        data_extract = extract(result)

        ### second log : get raw extracted data from the model in a csv
        create_raw_data_log(data_extract)

        ### post process:
        data = remove_commas(data_extract)
        data = change_obvious_letters_to_numbers(data)
        data = remove_specific_symbols(data)
        final_number_data = final_number(data)

        ### prepare 3rd log:
        damage_lists.append(final_number_data)

        ### finish post processing:
        final_sum = sum(final_number_data)

        ### 3rd log: get processed extracted data in another csv log file
        create_processed_data_log(final_number_data)

        ### Store frame_damage:
        frame_damage.append(final_sum)

        ### Store data for graph:
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_time = current_frame / fps
        time_stamps.append(current_time)
        damage_values.append(final_sum)

    ### Close video capture
    cap.release()

    #### Delete duplicate damage values across frames
    final_result = delete_duplicates(damage_lists)

    #### Calculate DPS
    dps = []
    for x in range(0, len(frame_damage), 5):
        dps.append(sum(frame_damage[x:x+5]))

    ### Calculate Average DPS
    duration_seconds = total_frames / fps
    average_per_second = final_result / duration_seconds

    # ### Create plot
    plt_image = create_plot(time_stamps, damage_values)

    return f"Total damage in clip: {final_result}\nDamage per second: {int(average_per_second)}", plt_image
