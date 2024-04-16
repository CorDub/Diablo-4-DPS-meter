from PIL import Image, ImageEnhance
import numpy as np

#Function to preprocess a frame image.
def preprocess(frame):
    image = Image.fromarray(frame)

    # Enhance the brightness of the image
    img_enhancer = ImageEnhance.Brightness(image)
    enhanced_output = img_enhancer.enhance(0.25)

    # Increase the contrast of the image
    contrast_enhancer = ImageEnhance.Contrast(enhanced_output)
    contrasted = contrast_enhancer.enhance(10)

    # Increase the sharpness of the image
    sharpness_enhancer = ImageEnhance.Sharpness(contrasted)
    sharp = sharpness_enhancer.enhance(2.5)
    return np.array(sharp)
