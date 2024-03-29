from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import cv2
from starlette.responses import Response
import numpy as np
import processing

app = FastAPI()
app.state.model = easyocr.Reader(['en'], gpu=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.post("/upload_image")
async def receive_image(img: UploadFile=File(...)):
    ### Receiving and decoding the image
    contents = await img.read()

    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray

    ### Do cool stuff with your image.... For example face detection
    final_number = processing.process(cv2_img)

    ### Encoding and responding with the image
    # im = cv2.imencode('.png', cv2_img)[1] # extension depends on which format is sent from Streamlit
    return str(final_number) # Response(content=im.tobytes(), media_type="image/png")

@app.post("/upload_video")
async def create_upload_file(file: UploadFile):
    return {"filename": file.content_type}
