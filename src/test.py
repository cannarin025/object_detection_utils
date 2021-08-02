import os
from re import A
from numpy.lib.type_check import imag
#from labelled_img import Labelled_Img
from labelled_img import Labelled_Img
import numpy as np
import cv2

dir_path = "L:/Code/YOLOv4_detection/multimodal_detection/to_resize"
img_path = "L:/Code/YOLOv4_detection/toad_no_background.png"
label_path = "L://Code//IR_imgs//IR_imgs_labelled_(untransformed)//Pigeon//16_36_000054_FLIR.xml"

image = Labelled_Img(img_path, label_path)

image = Labelled_Img(img_path)
image.rot_90()
image.downscale(0.2)
image.show()
image.save()
# for filename in os.listdir(dir_path):
#     #if filename.count("vis") >= 1 and filename.endswith((".png", ".jpg")):
#     if filename.endswith((".jpg", ".png")):
#         img_path = os.path.join(dir_path, filename)
#         image = Labelled_Img(img_path)
#         #image.show()
#         #print(np.shape(image.get_img())[:2])
#         image.resize_img(240, 320)
#         image.rot_270()
#         image.save(savedir = "L:/Code/YOLOv4_detection/multimodal_detection/to_resize/resized")
#image.save(savedir = "L:/Code/YOLOv4_detection/multimodal_detection")
#image.resize_img(50, 50)
#image.random_transform()
#image.stretch_y(2).rot_270()
#image.stretch_x(20)
#image.stretch_y(1.5)

#no issue here as resize is before rotate (10px border thing)
# image.stretch_x(1.3)
# image.rot_180()
# image.show()

#issue here as resize after rotate so applies 10px border thing 
#image.rot_90()
#image.stretch_x(1.5)
#image.greyscale()
#image.show()

#image.show()
#image.save(savedir = "L://Code//labelled_img_test", custom_name = "size_test")
#image.save()
#print(np.shape(image.get_img())[:2])
#print(image.get_transformations())