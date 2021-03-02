import os

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


dir_path = "L://Code//cat_imgs//yolo//cats_labelled//"
target = "car"
replace = "cat"

rename_label(dir_path, target, replace)
        