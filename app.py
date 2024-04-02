import gradio as gr
import easyocr
from processing import process_video_and_display_results

#Start model
reader = easyocr.Reader(['en'], gpu=True)

###Gradio interface code
iface = gr.Interface(fn=process_video_and_display_results, inputs="video", outputs=["text", "image"],
                     title="Diablo 4 DPS meter", description="Upload a video and detect text every 4 frames per second.")
iface.launch(share=True)
