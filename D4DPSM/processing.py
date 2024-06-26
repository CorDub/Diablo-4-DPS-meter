import easyocr
import cv2
from D4DPSM.pre_processing import preprocess
from D4DPSM.post_processing import extract, change_obvious_letters_to_numbers, remove_commas, remove_specific_symbols, final_number, delete_duplicates, create_plot

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

        ### extract text from results
        data_extract = extract(result)

        ### post process:
        data = remove_commas(data_extract)
        data = change_obvious_letters_to_numbers(data)
        data = remove_specific_symbols(data)
        final_number_data = final_number(data)

        ### prepare log:
        damage_lists.append(final_number_data)

        ### finish post processing:
        final_sum = sum(final_number_data)

        ### Store frame_damage:
        frame_damage.append(final_sum)

        ### Store data for graph:
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_time = current_frame / fps
        time_stamps.append(current_time)
        damage_values.append(final_sum)

    ### Close video capture
    cap.release()

    #### Delete duplicate damage values across frames to get final result and convert it in readable format
    final_result = delete_duplicates(damage_lists)
    final_result_formatted = "{:,}".format(final_result)

    #### Calculate DPS
    dps = []
    for x in range(0, len(frame_damage), 4):
        dps.append(sum(frame_damage[x:x+4]))

    ### Calculate Average DPS
    average_per_second = int(final_result / (total_frames/fps))
    adps_formatted = "{:,}".format(average_per_second)

    # ### Create plot
    plt_image = create_plot(time_stamps, damage_values)

    return f"Total damage in clip: {final_result_formatted}\nDamage per second: {adps_formatted}", plt_image
