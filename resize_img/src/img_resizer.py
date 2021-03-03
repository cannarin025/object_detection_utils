from PIL import Image
import cv2
import numpy as np
import os
import glob

img = cv2.imread("C://Users//canna//Desktop//Screenshot_2.png")

def resize_img(target_width_px, target_height_px, img):
    print(np.shape(img))
    img_height_px, img_width_px = np.shape(img)[:2]
    img_aspect_ratio = img_width_px / img_height_px
    target_aspect_ratio = target_width_px / target_height_px

    left = 0
    right = img_width_px
    bottom = img_height_px
    top = 0

    # Determine dimensions of image to ensure same aspect ratio as original
    if img_aspect_ratio < target_aspect_ratio:  # height of original image needs to be reduced
        while img_aspect_ratio < target_aspect_ratio:
            bottom -= 1
            img_aspect_ratio = right / bottom


    elif img_aspect_ratio > target_aspect_ratio:  # width of original image needs to be reduced
        while img_aspect_ratio > target_aspect_ratio:
            right -= 1
            img_aspect_ratio = right / bottom

    diff_y = img_height_px - bottom
    diff_x = img_width_px - right

    left = int(diff_x / 2)
    right = int(img_width_px - diff_x / 2)
    bottom = int(img_height_px - diff_y / 2)
    top = int(diff_y / 2)

    cropped = img[top:bottom][left:right]

    # Image and target aspect ratios are now identical. Resize.
    new_size = (target_width_px, target_height_px)
    resized = cv2.resize(cropped, new_size)
    return resized