from os import stat_result
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.type_check import imag

from scipy.interpolate import UnivariateSpline

img_path = "C://Users//canna//Desktop//Screenshot_2.png"

img = cv2.imread(img_path)

rotated = cv2.rotate(img, rotateCode=cv2.ROTATE_90_CLOCKWISE)
flipped = cv2.flip(img, 1)

#reflections
def reflect_x(img):
    return cv2.flip(img, 1)

def reflect_y(img):
    return cv2.flip(img, 0)

#clockwise rotations
def rot_90(img):
    return cv2.rotate(img, rotateCode=cv2.ROTATE_90_CLOCKWISE)

def rot_180(img):
    return cv2.rotate(img, rotateCode=cv2.ROTATE_180)

def rot_270(img):
    return cv2.rotate(img, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)

#warmth
def spreadLookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))
  
def warmImage(image, strength, graph = False):
    if strength > 0 and abs(strength) <= 1:
        increase_x_points = [0, 64, 128, 255]
        increase_y_points = [0, 64 * (1+strength), 128 * (1+strength), 255]
        decrease_x_points = [0, 64, 128, 255]
        decrease_y_points = [0, 64 * (1-strength), 128 * (1-strength), 255]

        increaseLookupTable = spreadLookupTable(increase_x_points, increase_y_points)
        decreaseLookupTable = spreadLookupTable(decrease_x_points, decrease_y_points)

        blue_channel, green_channel, red_channel = cv2.split(image)
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

        return cv2.merge((blue_channel, green_channel, red_channel)) 
    else:
        print("strength ratio must be a decimal value between 0-1")

def coldImage(image, strength, graph = False):
    if strength > 0 and abs(strength) <= 1:
        increase_x_points = [0, 64, 128, 255]
        increase_y_points = [0, 64 * (1+strength), 128 * (1+strength), 255]
        decrease_x_points = [0, 64, 128, 255]
        decrease_y_points = [0, 64 * (1-strength), 128 * (1-strength), 255]

        increaseLookupTable = spreadLookupTable(increase_x_points, increase_y_points)
        decreaseLookupTable = spreadLookupTable(decrease_x_points, decrease_y_points)

        blue_channel, green_channel, red_channel = cv2.split(image)
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
   
        return cv2.merge((blue_channel, green_channel, red_channel))
    else:
        print("strength ratio must be a decimal value between 0-1")

#cv2.imshow("test", colour_test(img))
cv2.imshow("cold gabe", coldImage(img, 0.30, graph=True))
cv2.imshow("hot gabe", warmImage(img, 0.30, graph=True))

cv2.imshow("gabe", flipped)
cv2.waitKey(0)