import os
from typing import Tuple
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.interpolate import UnivariateSpline
from util import get_substring

class Labelled_Img:
    """
    A class that reads in an image and its label in pascal voc format, applies various transformations and saves a new transformed image/labels in pascal voc or YOLO formet.
    """
    def __init__(self, img_path, label_path = None) -> None:

        self._transformations = []
        
        self._img = cv2.imread(img_path)
        self._labels = None

        if label_path is not None:
            self._labels = []
            with open(label_path, "r") as fp:
                self._label_xml = fp.read()

            # generating list of labels

            label_count = self._label_xml.count("<name>")

            # getting image size
            xdim = int(get_substring(self._label_xml, "<width>", "</width>"))
            ydim = int(get_substring(self._label_xml, "<height>", "</height>"))

            search_start = 0
            xml = self._label_xml
            for i in range(label_count):
                xml = xml[search_start:]

            # finds min coords of bounding box
                name = get_substring(xml, "<name>", "</name>")
                x_min = int(get_substring(xml, "<xmin>", "</xmin>"))
                y_min = int(get_substring(xml, "<ymin>", "</ymin>"))
                x_max = int(get_substring(xml, "<xmax>", "</xmax>"))
                y_max = int(get_substring(xml, "<ymax>", "</ymax>"))

                self._labels.append([name, (x_min, y_min), (x_max, y_max)])

                search_start = xml.find("</ymax>") + len("</ymax>")  # checks following text next iteration.

    # getter methods
    def show_img(self, show_labels = True):
        if not show_labels or self._labels is None:
            cv2.imshow("img", self._img)
            cv2.waitKey(0)

        else:
            labelled_img = copy.copy(self._img)
            for label in self._labels:
                labelled_img = cv2.rectangle(labelled_img, label[1], label[2], thickness=2, color=(255,0,0))
            
            cv2.imshow("labelled", labelled_img)
            cv2.waitKey(0)

    def get_img(self):
        return self._img

    def get_labels(self):
        return self._labels

    def get_transformations(self):
        return self._transformations

    

    # image resizer
    def resize_img(self, target_width_px, target_height_px, resize_labels = True, transformation = True):
        if transformation:
            self._transformations.append("resized")

        if self._labels is None:
            resize_labels = False  # will not resize label if label does not exist

        img_height_px, img_width_px = np.shape(self._img)[:2]
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

        if resize_labels:
            resized_labels = []
            # crops to include as much of labels as possible
            label_max_x = 0
            label_max_y = 0
            label_min_x = img_width_px
            label_min_y = img_height_px

            for label in self._labels:
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


            for label in self._labels:
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

            self._labels = resized_labels
        
        else:
            # crops around centre of image
            left = int(diff_x / 2)
            right = int(img_width_px - diff_x / 2)
            bottom = int(img_height_px - diff_y / 2)
            top = int(diff_y / 2)

        cropped = self._img[top:bottom, left:right]

        # Image and target aspect ratios are now identical. Resize.
        new_size = (target_width_px, target_height_px)
        self._img = cv2.resize(cropped, new_size)



    # image transformation methods
    def reflect_x(self):
        self._img = cv2.flip(self._img, 1)
        self._transformations.append("reflect_x")

        #transforming labels
        if self._labels is not None:
            reflected = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_max = img_x - label[1][0]
                x_min = img_x - label[2][0]
                y_max = label[2][1]
                y_min = label[1][1]

                reflected.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = reflected


    def reflect_y(self):
        self._img = cv2.flip(self._img, 0)
        self._transformations.append("reflect_y")

        #transforming labels
        if self._labels is not None:
            reflected = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_max = label[1][0]
                x_min = label[2][0]
                y_max = img_y - label[1][1]
                y_min = img_y - label[2][1]

                reflected.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = reflected

    # clockwise rotations
    def rot_90(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        self._transformations.append("rot_90")

        #transforming labels
        if self._labels is not None:
            rotated = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_min = img_x - label[2][1]
                x_max = img_x - label[1][1]
                y_max = label[2][0]
                y_min = label[1][0]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated

    def rot_180(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_180)
        self._transformations.append("rot_180")

        #transforming labels
        if self._labels is not None:
            rotated = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_min = img_x - label[1][0]
                x_max = img_x - label[2][0]
                y_max = img_y - label[2][1]
                y_min = img_y - label[1][1]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated

    def rot_270(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
        self._transformations.append("rot_270")

        #transforming labels
        if self._labels is not None:
            rotated = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_min = label[1][1]
                x_max = label[2][1]
                y_max = img_y - label[1][0]
                y_min = img_y - label[2][0]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated

    # stretches
    def stretch_x(self, factor):
        self._transformations.append(f"stretch_x{factor}")
        h, w = np.shape(self._img)[:2]
        scaled_w = int(w * (1+factor))
        self._img = cv2.resize(self._img, (scaled_w, h), interpolation=cv2.INTER_AREA)
        self._img = self.resize_img(w, h, resize_labels=False, transformation=False)

        if self._labels is not None:
            stretched = []
            img_y, img_x = np.shape(self._img)
            for label in self._labels:
                pass

    def stretch_y(self, factor):
        self._transformations.append(f"stretch_y{factor}")
        h, w = np.shape(self._img)[:2]
        scaled_h = int(h * (1+factor))
        self._img = cv2.resize(self._img, (w, scaled_h), interpolation=cv2.INTER_AREA)
        self._img = self.resize_img(w, h, resize_labels=False, transformation=False)

        if self._labels is not None:
            pass

    # colour effects
    def spreadLookupTable(self, x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))
  
    def warmImage(self, strength, graph = False):
        if strength >= 0 and abs(strength) <= 1:
            self._transformations.append(f"warm{strength}")
            increase_x_points = [0, 64, 128, 192, 224, 255]
            increase_y_points = [0, 64 * (1+strength), 128 * (1+0.75*strength), 192*(1+0.3*strength),224*(1+0.135*strength), 255]
            decrease_x_points = [0, 64, 128, 192, 224, 255]
            decrease_y_points = [0, 64 * (1-0.9*strength), 128 * (1-0.75*strength), 192*(1-0.3*strength),224*(1-0.135*strength), 255]

            increaseLookupTable = self.spreadLookupTable(increase_x_points, increase_y_points)
            decreaseLookupTable = self.spreadLookupTable(decrease_x_points, decrease_y_points)

            blue_channel, green_channel, red_channel = cv2.split(self._img)
            red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)

            if graph:
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle("Warm graphs")
                ax1.plot(increaseLookupTable, label = "filter")
                ax1.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax1.axhline(y=255, color='r', linestyle='-')
                ax1.plot(increase_x_points, increase_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax1.title.set_text("Red curve")

                ax2.plot(decreaseLookupTable, label = "filter")
                ax2.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax2.plot(decrease_x_points, decrease_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax2.axhline(y=255, color='r', linestyle='-')
                ax2.title.set_text("Blue curve")

                plt.legend(loc="lower center", bbox_to_anchor=(0, -0.15), ncol= 3)
                plt.show()

            self._img = cv2.merge((blue_channel, green_channel, red_channel)) 
        else:
            print("strength ratio must be a decimal value between 0-1")

    def coolImage(self, strength, graph = False):
        if strength >= 0 and abs(strength) <= 1:
            self._transformations.append(f"cool{strength}")
            increase_x_points = [0, 64, 128, 192, 224, 255]
            increase_y_points = [0, 64 * (1+strength), 128 * (1+0.75*strength), 192*(1+0.3*strength),224*(1+0.135*strength), 255]
            decrease_x_points = [0, 64, 128, 192, 224, 255]
            decrease_y_points = [0, 64 * (1-0.9*strength), 128 * (1-0.75*strength), 192*(1-0.3*strength),224*(1-0.135*strength), 255]

            increaseLookupTable = self.spreadLookupTable(increase_x_points, increase_y_points)
            decreaseLookupTable = self.spreadLookupTable(decrease_x_points, decrease_y_points)

            blue_channel, green_channel, red_channel = cv2.split(self._img)
            red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)

            if graph:
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle("Cool graphs")
                ax1.plot(increaseLookupTable, label = "filter")
                ax1.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax1.plot(increase_x_points, increase_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax1.axhline(y=255, color='r', linestyle='-')
                ax1.title.set_text("Blue curve")
                
                ax2.plot(decreaseLookupTable, label = "filter")
                ax2.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax2.plot(decrease_x_points, decrease_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax2.axhline(y=255, color='r', linestyle='-')
                ax2.title.set_text("Red curve")

                plt.legend(loc="lower center", bbox_to_anchor=(0, -0.15), ncol= 3)
                plt.show()
    
            self._img = cv2.merge((blue_channel, green_channel, red_channel))  
        else:
            print("strength ratio must be a decimal value between 0-1")
            