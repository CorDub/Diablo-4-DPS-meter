from PIL import Image, ImageEnhance
import numpy as np

def preprocess(frame):
    image = Image.fromarray(frame)
    img_enhancer = ImageEnhance.Brightness(image)
    enhanced_output = img_enhancer.enhance(0.25)
    contrast_enhancer = ImageEnhance.Contrast(enhanced_output)
    contrasted = contrast_enhancer.enhance(10)
    sharpness_enhancer = ImageEnhance.Sharpness(contrasted)
    sharp = sharpness_enhancer.enhance(2.5)
    return np.array(sharp)
