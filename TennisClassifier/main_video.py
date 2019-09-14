#!/bin/env python3

import cv2
import numpy as np
from tensorflow.keras.models import load_model


def convert_to_numpy_image(image):
    image = np.asarray(image, dtype=np.float32)
    image /= 255.0
    return np.expand_dims(image, axis=0)


def convert_prediction_to_class(pred):
    pred = np.squeeze(pred)
    if pred < 0.4:
        return "Has Tennis Ball:  {:2f}%".format((1 - pred) * 100)
    else:
        return "No Tennis Ball:  {:2f}%".format((1 - pred) * 100)


def main():
    model = load_model("../saved_models/tennis_classifier.h5")

    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        np_frame = convert_to_numpy_image(frame)
        predicted = model.predict(np_frame)

        class_pred = convert_prediction_to_class(predicted)

        cv2.putText(frame, class_pred, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
