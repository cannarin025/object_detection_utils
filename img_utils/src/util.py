import os
import random
from re import X
from bs4 import BeautifulSoup

def get_substring(text, start, end):
    """
    Function to get all text between 1st occurence of start and end strings
    """
    start_marker = text.find(start)
    end_marker = text.find(end)
    return text[start_marker + len(start) : end_marker]

def rename_label(dir_path, target, replace):


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
    Function to convert Pascal_Voc label format to YOLO label format
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
    if not os.path.exists(dir_path + "//train"):
            os.mkdir(dir_path +"//train")
    if not os.path.exists(dir_path + "//test"):
        os.mkdir(dir_path +"//test")
    if not os.path.exists(dir_path + "//eval"):
        os.mkdir(dir_path +"//eval")
    txt_list = os.listdir(dir_path)
    txt_list = list(filter(lambda x: x.endswith(".txt") ,txt_list))
    txt_list.remove("classes.txt")
    random.shuffle(txt_list)
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
    

def create_empty_labels(dir_path, label_type):
    '''
    A function to generate an emtpy label xml file for any images with no classes.
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


#dir_path = "L://Code//YOLOv4_detection//all_data//IR//data_v3"
#pascal_voc_to_yolo(dir_path)
#create_empty_labels(dir_path, "yolo")
#yolo_data_split(dir_path, img_ext=".jpg", train_split=0.8, test_split=0.20)