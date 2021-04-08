from os import terminal_size
from re import A
from numpy.lib.type_check import imag
from labelled_img import Labelled_Img
import util
import numpy as np

dir_path = "L://Code//IR_imgs//IR_imgs_labelled_(untransformed)//Pigeon"
img_path = "L://Code//IR_imgs//IR_imgs_labelled_(untransformed)//Pigeon//16_36_000054_FLIR.jpg"
label_path = "L://Code//IR_imgs//IR_imgs_labelled_(untransformed)//Pigeon//16_36_000054_FLIR.xml"

image = Labelled_Img(img_path, label_path)
image.show()
print(np.shape(image.get_img())[:2])
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
image.rot_180()
image.stretch_x(1.5)
image.show()

#image.show()
#image.save(savedir = "L://Code//labelled_img_test", custom_name = "size_test")
#image.save()
#print(np.shape(image.get_img())[:2])
print(image.get_transformations())