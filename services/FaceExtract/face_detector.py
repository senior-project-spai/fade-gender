
import cv2
import numpy as np

from config import settings
from utils import load_image_file

def detect_face(img_path: str):
    image = load_image_file(img_path)
    net = cv2.dnn.readNetFromCaffe(settings.FACE_POS_DEPLOY_TXT,
                                   settings.FACE_POS_WEIGHT)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    face_index = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.8:
            face_index.append(i)
    pos = []

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    emotion_faces = np.empty((len(face_index), 48, 48, 1))
    age_gender_faces = np.empty((len(face_index), 224, 224, 3))
    faces = np.empty((len(face_index), 160, 160, 3))

    for i in face_index:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        # y = startY - 10 if startY - 10 > 10 else startY + 10
        pos.append((startX, startY, endX, endY))

        roi_gray = gray_img[startY:endX, startX:endX]
        roi_gray = cv2.normalize(
            roi_gray, None, alpha=0, beta=1,
            norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        cropped_img = np.expand_dims(
            np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        emotion_faces[i, :, :, :] = cropped_img

        f_img = image[startY:endX, startX:endX, :]
        age_gender_faces[i, :, :, :] = cv2.resize(f_img, (224, 224))
        age_gender_faces[i, :, :, :] = age_gender_faces[i, :, :, :]/255.0

        faces[i, :, :, :] = cv2.resize(f_img, (160, 160))
        faces[i, :, :, :] = faces[i, :, :, :]/255.0

    return len(faces), emotion_faces, age_gender_faces, faces, pos
