import gradio as gr
import easyocr
import cv2
import matplotlib.pyplot as plt
import numpy as np
import post_processing
from io import BytesIO
from PIL import Image

reader = easyocr.Reader(['en'], gpu=True)

def process_video_and_display_results(video):
    if isinstance(video, str):
        cap = cv2.VideoCapture(video)
    else:
        cap = cv2.VideoCapture(video.name)

    frame_damage = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(fps / 4), 1)  # 4 frames per second
    time_stamps = []
    damage_values = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result = reader.readtext(frame)
        data_extract = post_processing.extract(result)
        data = post_processing.remove_commas(data_extract)
        final_number = post_processing.final_number(data)
        frame_damage.append(final_number)

        for _ in range(frame_interval - 1):
            cap.read()

        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_time = current_frame / fps
        time_stamps.append(current_time)
        damage_values.append(final_number)

    cap.release()

    dps = []
    for x in range(0, len(frame_damage), 5):
        dps.append(sum(frame_damage[x:x+5]))

    total_sum = sum(dps)
    duration_seconds = total_frames / fps
    average_per_second = total_sum / duration_seconds

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

    return f"Total damage in clip: {total_sum}\nDamage per second: {int(average_per_second)}", plt_image

iface = gr.Interface(fn=process_video_and_display_results, inputs="video", outputs=["text", "image"],
                     title="Diablo 4 DPS meter", description="Upload a video and detect text every 4 frames per second.")
iface.launch(share=True)
