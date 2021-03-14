from PIL import Image, ImageOps
import cv2
import numpy as np


def get_output(label, pos, image):
    X, Y, endX, endY = pos

    # Blue color in BGR
    color = (255, 0, 0)
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    image = cv2.rectangle(image, (X, Y), (endX, endY), color, thickness)

    image = cv2.putText(image, label, (X, Y-5), font,
                        fontScale, color, thickness, cv2.LINE_AA)

    return image


def load_image_file(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array + rotate
    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    im = Image.open(file)
    if mode:
        im = im.convert(mode)
    im = ImageOps.exif_transpose(im)
    return np.array(im)
