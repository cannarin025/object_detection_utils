from src import img_resizer
from argparse import ArgumentParser
import glob
import cv2
import os

parser = ArgumentParser(description="Symmetrically resizes images at supplied path and creates directory for result")
parser.add_argument("width", help="Desired width in pixels")
parser.add_argument("height", help = "Desired height in pixels")
parser.add_argument("img_path", help = "Path to image directory")

parse = parser.parse_args()

width = int(parse.width)
height = int(parse.height)
path = parse.img_path

if width == None:
    raise ValueError("Please input a valid width")

if height == None:
    raise ValueError("Please input a valid height")

# reads all images at directory "path" and resizes them
if not os.path.exists(path + '/resized'): 
    os.makedirs(path + '/resized')
    for filepath in glob.iglob(path + "/*.jpg", recursive = True):
        file_name = filepath.split('.')[-2].split("\\")[-1]
        img = cv2.imread(filepath)
        resized = img_resizer.resize_img(width, height, img)
        resized.save(f"{path}/resized/{file_name}"+"_resized.jpg")