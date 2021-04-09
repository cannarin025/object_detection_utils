import os
import re
import sys
import random
import cv2
from bs4 import BeautifulSoup
from labelled_img import Labelled_Img 

"""
A file for carrying out operations on files contained within directories
"""

def sort_dir(root, exclude_list=[None]):
    """
    A function to sort quickly images for use in computer vision datasets based on user input.
    Iterates over all image (.jpg or .png) files contained within a directory and it's subdirectories (ignores any directories in list).
    Creates "good", "bad" and "maybe" directories within the original directories of each file and moves them based on user input ("y", "n", "m")
    """
    print("Sorting... press q to quit!")
    for subdir in os.listdir(root):
        if subdir not in ["good", "bad", "maybe"]:  # prevents algorithm from searching in "sorted" folders
            sub_path = root + "//" + subdir
            if os.path.isdir(sub_path):
                #print(sub_path, "is_dir")
                if os.path.basename(sub_path) not in exclude_list:  # will not search in subdir if dirname is in exclude_list
                    sort_dir(sub_path, exclude_list)
                else:
                    print(subdir, "ignoring directory")

            else:
                if os.path.splitext(sub_path)[-1] == ".jpg" or os.path.splitext(sub_path)[-1] == ".png":  # only does sorting if file has correct ext, else ignore.
                    dir_path = os.path.dirname(sub_path)
                    good_path = dir_path + "//good"
                    bad_path = dir_path + "//bad"
                    maybe_path = dir_path + "//maybe"
                    sort_list = [good_path, bad_path, maybe_path]
                    
                    for path in sort_list:    
                        if not os.path.exists(path):
                            os.mkdir(path)

                    img_name = os.path.basename(sub_path)
                    img = cv2.imread(sub_path)
                    print("now viewing:", sub_path)
                    cv2.imshow("img", img)

                    wait_key = True

                    while wait_key:  # checks user input and sorts accordingly
                        key = cv2.waitKey(0)
                        if key == ord("y"):
                            os.rename(sub_path, good_path + "//" + img_name)
                            wait_key = False
                        elif key == ord("n"):
                            os.rename(sub_path, bad_path + "//" + img_name)
                            wait_key = False
                        elif key == ord("m"):
                            os.rename(sub_path, maybe_path + "//" + img_name)
                            wait_key = False
                        elif key == ord("q"):  
                            sys.exit("quitting...")
                        elif key == ord("s"):  
                            print("skip")
                            break
                        elif key is not None:
                            print('Please press a valid key: "y" to keep, "n" to discard, "m" for maybe and "q" to quit')
                            key = None


def count_objects(dirpath, label_format = "pascal_voc", class_file_path = None):
    """
    A function to count the number of each class in a directory
    """
    class_count = {}
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        filename, ext = os.path.splitext(file)
        if ext in [".jpg", ".png"]:  # only selects image files
            if label_format == "pascal_voc":
                label_path = os.path.join(dirpath, filename + ".xml")
                if os.path.exists(label_path): 
                    img = Labelled_Img(filepath, label_path)
                    for label in img.get_labels():
                        if label.class_name in class_count.keys():
                            class_count[label.class_name] += 1
                        else:
                            class_count[label.class_name] = 1
            
            elif label_format == "yolo":
                label_path = os.path.join(dirpath, filename + ".txt")
                if class_file_path is None:
                    print("Please provide path to class file")
                if os.path.exists(label_path) and filename != os.path.splitext(os.path.basename(class_file_path)):  # checks that file is not the class file
                    with open(class_file_path) as fp:
                        classes = fp.readlines()
                    classes = [x.strip() for x in classes]  # cleaning up strings
                    
                    with open(label_path) as fp:
                        label_txt = fp.read().strip()
                    label_indices = re.findall(r"^[0-9]+|\n[0-9]+", label_txt)
                    label_indices = [x.strip() for x in label_indices]
                    
                    for index in label_indices:
                        index = int(index)
                        if classes[index] in class_count.keys():
                            class_count[classes[index]] += 1
                        else:
                            class_count[classes[index]] = 1
    return class_count

def rename_label(dir_path, target, replace):
    """
    A function to rename an incorrect class name in pascal_voc format
    """
    for filename in os.listdir(dir_path):
        if filename.split(".")[-1] == "xml":
            filepath = dir_path + filename
            with open(filepath, "r") as fp:
                new = fp.read().replace(f"<name>{target}</name>",f"<name>{replace}</name>")  # old label --> new label 
        
            with open(filepath, "w+") as fp:
                fp.write(new)

    print("Done!")
    return



def pascal_voc_to_yolo(dir_path, move = True):
    """
    Function to convert labels in directory from Pascal_Voc label format to YOLO label format
    """

    label_paths = []
    classes = set({})
    entries = []

    #generating class list
    for filename in os.listdir(dir_path):
        if os.path.splitext(filename)[-1] == ".xml":
            label_path = dir_path + "//" + filename
            label_paths.append(label_path)
            with open(label_path, "r") as fp:
                label_xml = fp.read()
            soup = BeautifulSoup(label_xml, "xml")
            
            for object in soup.findAll("object"):  # adds each unique class_name to set to preserve uniqueness
                class_name = object.find("name").string
                classes.add(class_name)
            
    classes = sorted(list(classes))  # sorts list alphabetically to ensure consistency

    #writing classes.txt
    with open(dir_path + "//classes.txt", "w+") as fp:
        for class_name in classes:
            fp.write(class_name + "\n")

    #generating label txt files
    for label_path in label_paths:
        with open(label_path, "r") as fp:
            label_xml = fp.read()
        soup = BeautifulSoup(label_xml, "xml")
        filename = os.path.splitext(soup.find("filename").string)[0]
        entry = {"filename" : filename}  # gets filename only, no ext

        img_w = int(soup.find("width").string)
        img_h = int(soup.find("height").string)

        labels = []
        for object in soup.findAll("object"):  # adds each unique class_name to set to preserve uniqueness
            #finds min coords of bounding box
            class_name = object.find("name").string
            x_min = int(object.find("xmin").string)
            y_min = int(object.find("ymin").string)
            x_max = int(object.find("xmax").string)
            y_max = int(object.find("ymax").string)

            centre_x = x_min + ((x_max - x_min) / 2)
            centre_y = y_min + ((y_max - y_min) / 2)

            #works out bounding box dims
            box_width = x_max - x_min
            box_height = y_max - y_min

            labels.append({"class_id" : classes.index(class_name),
                           "centre_x" : centre_x / img_w,
                           "centre_y" : centre_y / img_h, 
                           "box_w" : box_width / img_w,
                           "box_h" : box_height / img_h})
        
        entry["labels"] = labels

        #writing label.txt files
        with open(dir_path + "//" + entry["filename"] + ".txt", "w+") as fp:
            for label_dict in entry["labels"]:
                class_id = label_dict["class_id"]
                centre_x = label_dict["centre_x"]
                centre_y = label_dict["centre_y"]
                box_w = label_dict["box_w"]
                box_h = label_dict["box_h"]
                fp.write(f"{class_id} {centre_x} {centre_y} {box_w} {box_h}" + "\n")
        
        #moving old labels to new directory
        if move:
            new_dir = dir_path + "//" + "pascal_voc_labels//"
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            os.rename(label_path, new_dir + filename + ".xml")
        
        a = 1

    print("Done!")
        


def yolo_data_split(dir_path, img_ext = ".jpg", train_split = 0.75, test_split = 0.20):
    """
    A function to sort a directory full of images into training, testing and evaluation data.
    Split is done based on inputted probabilites.
    Remaining files become evaluation data.
    """
    if train_split + test_split <= 1:
        if not os.path.exists(dir_path + "//train"):
                os.mkdir(dir_path +"//train")
        if not os.path.exists(dir_path + "//test"):
            os.mkdir(dir_path +"//test")
        if not os.path.exists(dir_path + "//eval"):
            os.mkdir(dir_path +"//eval")
        txt_list = os.listdir(dir_path)
        txt_list = list(filter(lambda x: x.endswith(".txt") ,txt_list))
        txt_list.remove("classes.txt")
        random.shuffle(txt_list)  # randomises order of files 
        img_count = len(txt_list)
        train_count = int(train_split * img_count)
        test_count = int(test_split * img_count)
        eval_count = int((1 - (train_split + test_split)) * img_count)
        #train
        for filename in txt_list[:train_count]:
            no_ext = os.path.splitext(filename)[0]
            os.rename(dir_path + "//" + filename, dir_path + "//train//" + filename)
            os.rename(dir_path + "//" + no_ext + img_ext, dir_path + "//train//" + no_ext + img_ext)
            txt_list.remove(filename)
        #test
        for filename in txt_list[:test_count]:
            no_ext = os.path.splitext(filename)[0]
            os.rename(dir_path + "//" + filename, dir_path + "//test//" + filename)
            os.rename(dir_path + "//" + no_ext + img_ext, dir_path + "//test//" + no_ext + img_ext)
            txt_list.remove(filename)
        #eval
        for filename in txt_list[:eval_count]:
            no_ext = os.path.splitext(filename)[0]
            os.rename(dir_path + "//" + filename, dir_path + "//eval//" + filename)
            os.rename(dir_path + "//" + no_ext + img_ext, dir_path + "//eval//" + no_ext + img_ext)
            txt_list.remove(filename)
        print("Done!")
    else:
        print("Please ensure split fractions sum to <= 1")
    


def create_empty_labels(dir_path, label_type):
    '''
    A function to generate an emtpy label file for any images with no classes.
    label_type = "pascal_voc" for Pascal Voc datasets
    label_type = "yolo" for YOLO datasets 
    NOTE: PASCAL VOC WON'T WORK AS IT REQUIRES THE XML TO HAVE THE PATH TAGS ETC (CAN'T SIMPLY GENERATE BLANK XML.) NEED TO FIX
    '''
    # todo: add some verification incase there are no .xml files in the whole dir etc to make sure wrong label_type was not chosen.
    if label_type == "pascal_voc":
        label_ext = ".xml"
    if label_type == "yolo":
        label_ext = ".txt"

    for filename in os.listdir(dir_path):
        if os.path.splitext(filename)[-1] == ".jpg" or os.path.splitext(filename)[-1] == ".png":
            if not os.path.exists(dir_path + "//" + os.path.splitext(filename)[0] + label_ext):
                open(dir_path + "//" + os.path.splitext(filename)[0] + label_ext, "w")
    
    print("Done!")

pascal_dir = "L:\Code\labelled_img_test"
yolo_dir = "L://Code//YOLOv4_detection//all_data//Vis//test"
yolo_dir2 = "L://Code//YOLOv4_detection//all_data//IR//tmp"
class_count = count_objects(yolo_dir2, label_format="yolo", class_file_path="L://Code//YOLOv4_detection//all_data//Vis//obj.names")
print(class_count)