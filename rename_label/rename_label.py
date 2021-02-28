import os

dir_path = "L://Code//RealTimeObjectDetection//Tensorflow//workspace//images//test//"

target = "car"
replace = "cat"

for filename in os.listdir(dir_path):
    if filename.split(".")[-1] == "xml":
        filepath = dir_path + filename
        with open(filepath, "r") as fp:
            new = fp.read().replace(f"<name>{target}</name>",f"<name>{replace}</name>")  # old label --> new label 
        
        with open(filepath, "w+") as fp:
            fp.write(new)

print("Done!")
        