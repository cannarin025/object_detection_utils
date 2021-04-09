import os
import re
from labelled_img import Labelled_Img 

"""
A file for carrying out operations on files contained within directories
"""

def count_objects(dirpath, label_format = "pascal_voc", class_file_path = None):
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

pascal_dir = "L:\Code\labelled_img_test"
yolo_dir = "L://Code//YOLOv4_detection//all_data//Vis//test"
class_count = count_objects(yolo_dir, label_format="yolo", class_file_path="L://Code//YOLOv4_detection//all_data//Vis//obj.names")
print(class_count)