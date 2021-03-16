from labelled_img import Labelled_Img
import os

dirpath = "C://Users//canna//Downloads//Lizard IR (Processed Transformed)"

for file in os.listdir(dirpath):
    if os.path.splitext(file)[1] == ".jpg":
        impath = dirpath + "//" + file
        label_path = os.path.splitext(impath)[0] + ".xml"
        labelled_img = Labelled_Img(impath, label_path)
        labelled_img.save()