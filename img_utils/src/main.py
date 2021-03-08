from numpy.lib.type_check import imag
from labelled_img import Labelled_Img

img_path = "L://Code//cat_imgs//labelled//video5_frame600_resized.jpg"
label_path = "L://Code//cat_imgs//labelled//video5_frame600_resized.xml"

image = Labelled_Img(img_path, label_path)
image.show_img()
image.resize_img(1000, 1000)
image.reflect_y()
image.warmImage(0.7, graph = True)
image.show_img()
print(image.get_transformations())