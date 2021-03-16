import os

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

    class_list = []
    entries = []

    #generating all entries
    for filename in os.listdir(dir_path):
        if os.path.splitext(filename)[-1] == ".xml":
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

                entry.append(os.path.splitext(filename)[0])  # stores filename in 1st element of list for later use. 
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

dir_path = "L://Code//cat_imgs//yolo//cats_labelled//"
pascal_voc_to_yolo(dir_path)