import cv2
import numpy as np
from util import get_substring

def get_label_coords(label_path):
    coords = []
    with open(label_path, "r") as fp:
        text = fp.read()
        #getting number of labels
        obj_count = text.count("<name>")

        #getting image size
        img_x = int(get_substring(text, "<width>", "</width>"))
        img_y = int(get_substring(text, "<height>", "</height>"))
        coords.append((img_x, img_y))

        entry = []
        search_start = 0
        for i in range(obj_count):
            text = text[search_start:]

        #finds min coords of bounding box
            name = get_substring(text, "<name>", "</name>")
            x_min = int(get_substring(text, "<xmin>", "</xmin>"))
            y_min = int(get_substring(text, "<ymin>", "</ymin>"))
            x_max = int(get_substring(text, "<xmax>", "</xmax>"))
            y_max = int(get_substring(text, "<ymax>", "</ymax>"))

            coords.append([name, (x_min, y_min), (x_max, y_max)])

            search_start = text.find("</ymax>") + len("</ymax>")  # checks following text next iteration.

    return coords


def resize_img_labelled(target_width_px, target_height_px, img_path, label_path):
    resized_labels = []
    img = cv2.imread(img_path)
    img_height_px, img_width_px = np.shape(img)[:2]
    img_aspect_ratio = img_width_px / img_height_px
    target_aspect_ratio = target_width_px / target_height_px

    left = 0
    right = img_width_px
    top = 0
    bottom = img_height_px
    
    # Determine dimensions of image to ensure same aspect ratio as original
    if img_aspect_ratio < target_aspect_ratio:  # height of original image needs to be reduced
        bottom = right / target_aspect_ratio


    elif img_aspect_ratio > target_aspect_ratio:  # width of original image needs to be reduced
        right = bottom * target_aspect_ratio

    diff_y = img_height_px - bottom
    diff_x = img_width_px - right

    #  crops to include as much of labels as possible
    label_max_x = 0
    label_max_y = 0
    label_min_x = img_width_px
    label_min_y = img_height_px
    
    label_coords = get_label_coords(label_path)

    test = cv2.imread(img_path)
    for label in label_coords[1:]:
        test = cv2.rectangle(test, label[1], label[2], thickness=4, color=(255,0,0))
        cv2.imshow("test", test)
        cv2.waitKey(0)


    for label in label_coords[1:]:
        if label[2][0] > label_max_x:
            label_max_x = label[2][0]
        
        if label[1][0] < label_min_x:
            label_min_x = label[1][0]

        if label[2][1] > label_max_y:
            label_max_y = label[2][1]
        
        if label[1][1] < label_min_y:
            label_min_y = label[1][1]

    x_factor = target_width_px / (right - left)
    y_factor = target_height_px / (bottom - top)

    headroom = 10
    x_max = label_max_x + headroom
    y_max = label_max_y + headroom

    if diff_x > 0:
        if img_width_px - diff_x > x_max:
            right = int(img_width_px - diff_x)

        else:
            right = label_max_x + headroom  # allows headroom (px) between label and image border
            left = int(diff_x - (img_width_px - right))
        
    if diff_y > 0:
        if img_height_px - diff_y > y_max:
            bottom = int(img_height_px - diff_y)
        
        else:
            bottom = label_max_y + headroom
            top = int(diff_y - (img_height_px - bottom))


    for label in label_coords[1:]:
        if label[1][0] > left:
            label_x1 = label[1][0] - left
        else: 
            label_x1 = 0
        
        if label[1][1] > top:
            label_y1 = label[1][1] - top
        else:
            label_y1 = 0

        label_x2 = label[2][0] - left
        label_y2 = label[2][1] - top

        resized_labels.append([label[0], (int(label_x1 * x_factor), int(label_y1 * y_factor)), (int(label_x2 * x_factor), int(label_y2 * y_factor))])
    
    cropped = img[top:bottom, left:right]

    # Image and target aspect ratios are now identical. Resize.
    new_size = (target_width_px, target_height_px)
    resized = cv2.resize(cropped, new_size)

    for label in resized_labels:
        labelled_img = cv2.rectangle(resized, label[1], label[2], thickness=4, color=(255,0,0))
        cv2.imshow("labelled", labelled_img)
        cv2.waitKey(0)

    # cv2.imshow("labelled", labelled_img)
    # cv2.waitKey(0)
    
    return resized

img_path = "L://Code//cat_imgs//labelled//video5_frame600_resized.jpg"
label_path = "L://Code//cat_imgs//labelled//video5_frame600_resized.xml"

resize_img_labelled(300,310,img_path,label_path)