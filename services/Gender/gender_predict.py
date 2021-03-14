from time import time
from typing import Tuple

from pathlib import Path

import cv2
import numpy as np
from loguru import logger

from config import settings
from services.Gender import get_gender_class
from services.FaceExtract import detect_face
from services.restful_caller import prediction_call


def predict_gender(image_path) -> Tuple[list, dict]:
    try:
        assert image_path != None
    except AssertionError:
        logger.error(f"No such a file {str(image_path)}")
    try:
        t = time()
        _, _, face, _, pos = detect_face(image_path)
    except Exception as e:
        logger.error(f"Error during face extraction, {type(e).__name__}")
        return [], {}
    try:
        prediction = prediction_call(settings.genderurl, data=face)
        tdelta = time() - t
        logger.info("Inference time: {}".format(tdelta))
        gender_class = get_gender_class()
        # for i in prediction:
        #     print(i)
        #     print(gender_class[np.argmax(i)])
        try:
            result = [gender_class[np.argmax(p)] for p in prediction]
        except KeyError:
            logger.error(f"Prediction error result unexpected: {prediction}")
            raise KeyError
        res_detail = {
            index: {
                "gender_p": {gender_class[_index]: str(p) for _index, p in enumerate(p_array)},
                "position": {"x1": str(pos[index][0]), "y1": str(pos[index][1]), "x2": str(pos[index][2]), "y2": str(pos[index][3])},
            }
            for index, p_array in enumerate(prediction)
        }
        return result, res_detail
    except Exception as e:
        logger.error(f"Given data {face}. Error Occurred.")
        return [], {}
