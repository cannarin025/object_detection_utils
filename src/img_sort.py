import os
import cv2
import sys

root_dir = "L:\Code\Shuttleworth_imgs"

print(os.listdir(root_dir))

def sort_dir(root, exclude_list=[None]):  # need to modify this so that I go through only files in the Vis folders instead of Vis and IR
    for subdir in os.listdir(root):
        if subdir not in ["good", "bad", "maybe"]:  # prevents algorithm from searching in "sorted" folders
            sub_path = root + "//" + subdir
            if os.path.isdir(sub_path):
                #print(sub_path, "is_dir")
                if os.path.basename(sub_path) not in exclude_list:  # prevents algorithm from searching in certain folders.
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

sort_dir(root_dir, ["IR"])