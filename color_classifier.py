import cv2
import numpy as np


def preprocess_car_region(car_crop):
    if car_crop is None or car_crop.size == 0:
        return None

    h, w = car_crop.shape[:2]

    # Focus on central body of car
    x1 = int(w * 0.22)
    x2 = int(w * 0.78)
    y1 = int(h * 0.38)
    y2 = int(h * 0.72)

    body_crop = car_crop[y1:y2, x1:x2]

    if body_crop.size == 0:
        return car_crop

    return body_crop


def is_blue_car(car_crop, blue_threshold=0.25):
    processed = preprocess_car_region(car_crop)
    if processed is None or processed.size == 0:
        return False, 0.0

    hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)

    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    # Stricter blue detection
    blue_hue = (h >= 100) & (h <= 135)
    strong_saturation = s >= 90
    valid_brightness = (v >= 40) & (v <= 200)

    blue_mask = blue_hue & strong_saturation & valid_brightness

    blue_mask_uint8 = (blue_mask.astype(np.uint8)) * 255

    kernel = np.ones((3, 3), np.uint8)
    blue_mask_uint8 = cv2.morphologyEx(blue_mask_uint8, cv2.MORPH_OPEN, kernel)
    blue_mask_uint8 = cv2.morphologyEx(blue_mask_uint8, cv2.MORPH_CLOSE, kernel)

    blue_pixels = np.sum(blue_mask_uint8 > 0)
    total_pixels = blue_mask_uint8.shape[0] * blue_mask_uint8.shape[1]

    if total_pixels == 0:
        return False, 0.0

    blue_ratio = blue_pixels / total_pixels

    return blue_ratio > blue_threshold, blue_ratio