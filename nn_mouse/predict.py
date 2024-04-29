from pathlib import Path
from typing import List
from typing import Tuple

import cv2
import numpy as np
from cv2.dnn import Net

BASE_DIR = Path(__file__).parent
path_model = cv2.dnn.readNetFromONNX(str(BASE_DIR / "path.onnx"))
time_model = cv2.dnn.readNetFromONNX(str(BASE_DIR / "time.onnx"))


def predict(model: Net, x: float, y: float):
    value = np.array([[x, y]])
    model.setInput(value)
    outputs = model.forward()
    return outputs


def get_path(x: int, y: int, x1: int, y1: int, w: int, h: int):
    """
    Returns a list of tuple (x, y, t) where x, y is
    the location and t is the time to stay on each location

    :param x: x coordinate of current mouse position
    :param y: y coordinate of current mouse position
    :param x1: x coordinate of target mouse position
    :param y1: y coordinate of target mouse position
    :param w: width of the monitor
    :param h: height of the monitor
    """
    dx, dy = (x1 - x) / w, (y1 - y) / h
    path = predict(path_model, dx, dy)
    time = predict(time_model, dx, dy)
    output: List[Tuple[float, float, float]] = []
    for (x2, y2), [t] in zip(path[0], time[0]):
        output.append((x + x2 * w, y + y2 * h, t / 100_000))
    return output
