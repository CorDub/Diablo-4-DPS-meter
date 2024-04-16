import gradio as gr
from D4DPSM.processing import process_video_and_display_results

# Gradio interface code with custom CSS
iface = gr.Interface(theme=gr.themes.Monochrome(), fn=process_video_and_display_results, inputs="video", outputs=["text", "image"],
                     title="Diablo 4 DPS meter", description="Upload a video to know how much damage you are dealing.")
iface.launch(share=True)
