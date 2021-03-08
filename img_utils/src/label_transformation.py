import os
from typing import List, Tuple
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
            x_min = int(get_substring(text, "<xmin>", "</xmin>"))
            y_min = int(get_substring(text, "<ymin>", "</ymin>"))
            x_max = int(get_substring(text, "<xmax>", "</xmax>"))
            y_max = int(get_substring(text, "<ymax>", "</ymax>"))

            coords.append([(x_min, y_min), (x_max, y_max)])

            search_start = text.find("</ymax>") + len("</ymax>")  # checks following text next iteration.

    return coords

def os_test(path):
    a = os.path.basename(path)
    b = os.path.dirname(path)
    return a

#label manipulation
def transform_label(label_path, transformation, parameter = None, dst = None):
    filename = os.path.basename(label_path).split(".")[0]
    dir = os.path.dirname(label_path)
    with open(label_path, "r") as fp:
        text = fp.read()
        img_w = None 
        img_h = None
        coords = None
        labels = None  # generate in form [[(xmin, ymax), (xmax, ymin)], [...] for each label in img]. remember to use relative coords

    transformed, transform_type = transformation(labels, parameter)
    transformed_text = None  # remember to convert back from relative to absolute coordinates

    if dst is not None:
        dir = dst
    
    with open(f"{dir}//{filename}_{transform_type}", "w+"):
        fp.write(transformed_text)
    
    return
    

def reflect_x_coords(labels : List[List[Tuple]], parameter) -> List[List[Tuple]]:
    """
    Takes normalised label coordinates of form [[(xmin, ymin), (xmax, ymax)]] 
    returns reflected coordinates
    """
    transform_type = "reflect_x"
    reflected = []
    for label in labels:
        x_max = 1 - label[0][0]
        x_min = 1 - label[1][0]
        y_max = label[1][1]
        y_min = label[0][1]

        reflected.append([(x_min, y_min), (x_max, y_max)])
    
    return reflected, transform_type

def reflect_y_label(labels, parameter):
    """
    Takes normalised label coordinates of form [[(xmin, ymax), (xmax, ymin)]]. 
    returns reflected coordinates.
    """
    transform_type = "reflect_y"
    reflected = []
    for label in labels:
        x_max = label[0][0]
        x_min = label[1][0]
        y_max = 1 - label[0][1]
        y_min = 1 - label[1][1]

        reflected.append([(x_min, y_min), (x_max, y_max)])
    
    return reflected, transform_type

def rot_90_label(labels, parameter):
    """
    Takes normalised label coordinates.
    returns coordinates rotated by 90 degrees clockwise.
    """
    transform_type = "rotate_90"
    rotated = []
    for label in labels:
        x_min = label[1][1]
        x_max = label[0][1]
        y_max = label[1][0]
        y_min = label[0][0]

        rotated.append([(x_min, y_min), (x_max, y_max)])
    
    return rotated, transform_type

def rot_180_label(labels, parameter):
    """
    Takes normalised label coordinates.
    returns coordinates rotated by 180 degrees clockwise.
    """
    transform_type = "rotate_180"
    rotated = []
    for label in labels:
        x_min = 1 - label[0][0]
        x_max = 1 - label[1][0]
        y_max = 1 - label[1][1]
        y_min = 1 - label[0][1]

        rotated.append([(x_min, y_min), (x_max, y_max)])
    
    return rotated, transform_type

def rot_270_label(labels, parameter):
    """
    Takes normalised label coordinates.
    returns coordinates rotated by 270 degrees clockwise.
    """
    transform_type = "rotate_270"
    rotated = []
    for label in labels:
        x_min = label[0][1]
        x_max = label[1][1]
        y_max = label[0][0]
        y_min = label[1][0]

        rotated.append([(x_min, y_min), (x_max, y_max)])
    
    return rotated, transform_type

def resize_label(label_path, factor):
    return

def stretch_x_label(label_path, factor):
    if factor == None:
        print("Please specify a stretch factor")
        return

    x_min = None

    return


def stretch_y_label(label_path, factor):
    pass



#label conversion
def pascal_voc_to_yolo(dir_path, move = True):
    """
    Function to convert Pascal_Voc label format to YOLO label format
    """

    class_list = []
    entries = []

    #generating all entries
    for filename in os.listdir(dir_path):
        if filename.split(".")[-1] == "xml":
            filepath = dir_path + filename
            with open(filepath, "r") as fp:
                text = fp.read()
                #getting number of labels
                obj_count = text.count("<name>")

                #getting image size
                img_x = int(get_substring(text, "<width>", "</width>"))
                img_y = int(get_substring(text, "<height>", "</height>"))

                entry = []
                search_start = 0
                for i in range(obj_count):
                    text = text[search_start:]
                    class_name = get_substring(text, "<name>", "</name>")
                    if class_name not in class_list:
                        class_list.append(class_name)
                    
                    #finds min coords of bounding box
                    x_min = int(get_substring(text, "<xmin>", "</xmin>"))
                    y_min = int(get_substring(text, "<ymin>", "</ymin>"))
                    x_max = int(get_substring(text, "<xmax>", "</xmax>"))
                    y_max = int(get_substring(text, "<ymax>", "</ymax>"))

                    centre_x = x_min + ((x_max - x_min) / 2)
                    centre_y = y_min + ((y_max - y_min) / 2)

                    #works out bounding box dims
                    box_width = x_max - x_min
                    box_height = y_max - y_min

                    search_start = text.find("</ymax>") + len("</ymax>")  # checks following text next iteration.
                    
                    entry.append({"class_id" : class_list.index(class_name),
                                    "centre_x" : centre_x / img_x,
                                    "centre_y" : centre_y / img_y, 
                                    "box_w" : box_width / img_x,
                                    "box_h" : box_height / img_y})

                entry.append(filename.split(".")[0])  # stores filename in 1st element of list for later use. 
                entries.append(entry)

            if move:
                new_dir = dir_path + "pascal_voc_labels//"
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                os.rename(filepath, new_dir + filename)

    #writing classes.txt
    with open(dir_path + "classes.txt", "w+") as fp:
        for class_name in class_list:
            fp.write(class_name + "\n")


    #writing label.txt files
    for entry in entries:
        with open(dir_path + entry[-1] + ".txt", "w+") as fp:
            for label_dict in entry[0:-1]:
                class_id = label_dict["class_id"]
                centre_x = label_dict["centre_x"]
                centre_y = label_dict["centre_y"]
                box_w = label_dict["box_w"]
                box_h = label_dict["box_h"]
                fp.write(f"{class_id} {centre_x} {centre_y} {box_w} {box_h}" + "\n")

    print("Done!")
    return

# dir_path = "L://Code//cat_imgs//yolo//cats_labelled//"
# pascal_voc_to_yolo(dir_path)

os_test("L://Code//cat_imgs//pascal_voc//cats_labelled//video0_frame0_resized.jpg")