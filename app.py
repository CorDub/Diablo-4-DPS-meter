import gradio as gr
import easyocr
import numpy as np
import post_processing
import cv2

reader = easyocr.Reader(['en'], gpu=True)

def process_video_and_display_results(video):
    if isinstance(video, str):
        cap = cv2.VideoCapture(video)
    else:
        cap = cv2.VideoCapture(video.name)

    frames = []
    frame_count = 0

    frame_results = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 6 == 0:  # 6 fotogramas
            result = reader.readtext(frame)
            data_extract = post_processing.extract(result)
            data = post_processing.remove_commas(data_extract)
            final_number = post_processing.final_number(data)
            frame_results[frame_count] = final_number
        frame_count += 1

    cap.release()

    total_sum = sum(frame_results.values())
    average_sum = total_sum / len(frame_results)

    return f"Total: {total_sum}\nAverage: {average_sum}"

iface = gr.Interface(fn=process_video_and_display_results, inputs="video", outputs="text",
                     title="EasyOCR - Video", description="Upload a video and detect text every 6 frames.")
iface.launch(share=True)
