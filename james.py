import os
from typing import Tuple
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.interpolate import UnivariateSpline
import glob
import random
from bs4 import BeautifulSoup
import re
import shutil

class Labelled_Img:
    """
    A class that reads in an image and its label in pascal voc format, applies various transformations and saves a new transformed image/labels in pascal voc or YOLO formet.
    """
    def __init__(self, img_path, label_path = None) -> None:

        self._transformations = []
        self._img_path = img_path
        self._label_path = label_path
        self._img = cv2.imread(img_path)
        self._origimg = cv2.imread(img_path)
        self._labels = None

        if label_path is not None:
            self._labels = []
            with open(label_path, "r") as fp:
                label_xml = fp.read()

            self._soup = BeautifulSoup(label_xml, "xml")
            for object in self._soup.findAll("object"):
                name = object.find("name").string
                x_min = int(object.find("xmin").string)
                y_min = int(object.find("ymin").string)
                x_max = int(object.find("xmax").string)
                y_max = int(object.find("ymax").string)

                self._labels.append([name, (x_min, y_min), (x_max, y_max)])
        
        self._origlabels = self._labels.copy()

    # getter methods
    def show(self, show_labels = True):
        if not show_labels or self._labels is None:
            cv2.imshow("img", self._img)
            cv2.waitKey(0)

        else:
            labelled_img = copy.copy(self._img)
            for label in self._labels:
                labelled_img = cv2.rectangle(labelled_img, label[1], label[2], thickness=2, color=(0,0,255))
            
            cv2.imshow("labelled", labelled_img)
            cv2.waitKey(0)

    def get_img(self):
        return self._img

    def get_labels(self):
        return self._labels

    def get_transformations(self):
        return self._transformations
    
    def reset(self):
        self._img = self._origimg
        self._labels = self._origlabels
        self._transformations = []


    # image resizer
    def resize_img(self, target_width_px, target_height_px, resize_labels = True, transformation = True, discard_small = True, discard_threshold = 0.5):
        if transformation:
            self._transformations.append("resized")

        if self._labels is None:
            resize_labels = False  # will not resize label if label does not exist

        img_height_px, img_width_px = np.shape(self._img)[:2]  # [:2] is to disregard colour channels dimension to only get dimensions of image
        img_aspect_ratio = img_width_px / img_height_px
        target_aspect_ratio = target_width_px / target_height_px

        left = 0
        right = img_width_px
        top = 0
        bottom = img_height_px
        
        # Determine dimensions of image to ensure same aspect ratio as original
        if img_aspect_ratio < target_aspect_ratio:  # height of original image needs to be reduced
            bottom = right / target_aspect_ratio


        elif img_aspect_ratio > target_aspect_ratio:  # width of original image needs to be reduced
            right = bottom * target_aspect_ratio

        diff_y = img_height_px - bottom
        diff_x = img_width_px - right

        if resize_labels:
            resized_labels = []
            # crops to include as much of labels as possible
            label_max_x = 0
            label_max_y = 0
            label_min_x = img_width_px
            label_min_y = img_height_px

            for label in self._labels:
                if label[2][0] > label_max_x:
                    label_max_x = label[2][0]
                
                if label[1][0] < label_min_x:
                    label_min_x = label[1][0]

                if label[2][1] > label_max_y:
                    label_max_y = label[2][1]
                
                if label[1][1] < label_min_y:
                    label_min_y = label[1][1]

            x_factor = target_width_px / (right - left)
            y_factor = target_height_px / (bottom - top)

            headroom = 0  # headroom set to 0 as it causes issues for images on border
            x_max = label_max_x + headroom
            y_max = label_max_y + headroom

            if diff_x > 0:
                if img_width_px - diff_x > x_max:
                    right = int(img_width_px - diff_x)

                else:
                    right = label_max_x + headroom  # allows headroom (px) between label and image border
                    left = int(diff_x - (img_width_px - right))
                
            if diff_y > 0:
                if img_height_px - diff_y > y_max:
                    bottom = int(img_height_px - diff_y)
                
                else:
                    bottom = label_max_y + headroom
                    top = int(diff_y - (img_height_px - bottom))


            for label in self._labels:
                if discard_small:
                    orig_x1 = label[1][0]
                    orig_x2 = label[2][0]
                    orig_y1 = label[1][1]
                    orig_y2 = label[2][1]

                if label[1][0] > left:
                    label_x1 = label[1][0] - left
                else: 
                    label_x1 = 0
                
                if label[1][1] > top:
                    label_y1 = label[1][1] - top
                else:
                    label_y1 = 0

                label_x2 = label[2][0] - left
                label_y2 = label[2][1] - top
                
                valid_label = all([True if item >= 0 else False for item in [label_x1, label_x2, label_y1, label_y2]])
                
                if valid_label:
                    label_x1 = int(label_x1 * x_factor)
                    label_y1 = int(label_y1 * y_factor)
                    label_x2 = int(label_x2 * x_factor)
                    label_y2 = int(label_y2 * y_factor)

                    if discard_small:
                        orig_area = img_height_px * img_width_px
                        resized_area = target_height_px * target_width_px
                        orig_label_area = (orig_x2 - orig_x1) * (orig_y2 - orig_y1) / orig_area
                        trans_label_area = (label_x2 - label_x1) * (label_y2 - label_y1) / resized_area
                        if trans_label_area <= discard_threshold * orig_label_area:
                            pass
                        else:
                            resized_labels.append([label[0], (label_x1, label_y1), (label_x2, label_y2)])
                    
                    else:
                        resized_labels.append([label[0], (label_x1, label_y1), (label_x2, label_y2)])

            self._labels = resized_labels
        
        else:
            # crops around centre of image
            left = int(diff_x / 2)
            right = int(img_width_px - diff_x / 2)
            bottom = int(img_height_px - diff_y / 2)
            top = int(diff_y / 2)

        cropped = self._img[top:bottom, left:right]

        # Image and target aspect ratios are now identical. Resize.
        new_size = (target_width_px, target_height_px)
        self._img = cv2.resize(cropped, new_size)
        return self



    # image transformation methods
    def reflect_x(self):
        self._img = cv2.flip(self._img, 1)
        self._transformations.append("reflectX")

        #transforming labels
        if self._labels is not None:
            reflected = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_max = img_x - label[1][0]
                x_min = img_x - label[2][0]
                y_max = label[2][1]
                y_min = label[1][1]

                reflected.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = reflected
        return self


    def reflect_y(self):
        self._img = cv2.flip(self._img, 0)
        self._transformations.append("reflectY")

        #transforming labels
        if self._labels is not None:
            reflected = []
            img_y, img_x = np.shape(self._img)[:2]
            for label in self._labels:
                name = label[0]
                x_max = label[2][0]
                x_min = label[1][0]
                y_max = img_y - label[1][1]
                y_min = img_y - label[2][1]

                reflected.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = reflected
        return self

    # clockwise rotations
    def rot_90(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        self._transformations.append("rot90")
        img_y, img_x = np.shape(self._img)[:2]

        #transforming labels
        if self._labels is not None:
            rotated = []

            for label in self._labels:
                name = label[0]
                x_min = img_x - label[2][1]
                x_max = img_x - label[1][1]
                y_max = label[2][0]
                y_min = label[1][0]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated
            self.resize_img(img_x, img_y, transformation=False)
        
        else:
            self.resize_img(img_x, img_y, resize_labels=False, transformation=False)
        return self

    def rot_180(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_180)
        self._transformations.append("rot180")
        img_y, img_x = np.shape(self._img)[:2]

        #transforming labels
        if self._labels is not None:
            rotated = []
            for label in self._labels:
                name = label[0]
                x_min = img_x - label[2][0]
                x_max = img_x - label[1][0]
                y_max = img_y - label[1][1]
                y_min = img_y - label[2][1]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated
            self.resize_img(img_x, img_y, transformation=False)
        
        else:
            self.resize_img(img_x, img_y, resize_labels=False, transformation=False)
        return self

    def rot_270(self):
        self._img = cv2.rotate(self._img, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
        self._transformations.append("rot270")
        img_y, img_x = np.shape(self._img)[:2]

        #transforming labels
        if self._labels is not None:
            rotated = []
            for label in self._labels:
                name = label[0]
                x_min = label[1][1]
                x_max = label[2][1]
                y_max = img_y - label[1][0]
                y_min = img_y - label[2][0]

                rotated.append([name, (x_min, y_min), (x_max, y_max)])
            self._labels = rotated
            self.resize_img(img_x, img_y, transformation=False)
        
        else:
            self.resize_img(img_x, img_y, resize_labels=False, transformation=False)
        return self

    # stretches
    def __stretch_coordinate(self, coord, midpoint, factor, axis):
        assert (type(axis) == int and axis in range(0,2)) 
        if type(coord) != tuple or type(midpoint) != tuple:
            print("Please give coordinates as tuples")
            return
        
        stretch = [coord[0], coord[1]]
        stretch[axis] = coord[axis] * factor
        return (int(stretch[0]), int(stretch[1]))

    def stretch_x(self, factor = None):
        if factor == None:
            factor = np.random.normal(1,0.2)
            while np.abs(factor) < 0.05:
                factor = np.random.normal(1,0.2)
        factor = np.abs(factor)
        
        self._transformations.append(f"stretchX-{round(factor, 3)}")
        img_y, img_x = np.shape(self._img)[:2]
        midpoint = (img_x / 2, img_y / 2)
        scaled_x = int(img_x * factor)
        self._img = cv2.resize(self._img, (scaled_x, img_y), interpolation=cv2.INTER_AREA)

        if self._labels is not None:
            stretched = []
            for label in self._labels:
                name = label[0]
                stretched.append([name, self.__stretch_coordinate(label[1], midpoint, factor, axis = 0),
                                 self.__stretch_coordinate(label[2], midpoint, factor, axis = 0)])
            self._labels = stretched
            self.resize_img(img_x, img_y, transformation=False)

        else:
            self.resize_img(img_x, img_y, resize_labels=False, transformation=False)
        return self

    def stretch_y(self, factor = None):
        if factor == None:
            factor = np.random.normal(1,0.2)
            while np.abs(factor) < 0.05:
                factor = np.random.normal(1,0.2)
        factor = np.abs(factor)
        
        self._transformations.append(f"stretchY-{round(factor, 3)}")
        img_y, img_x = np.shape(self._img)[:2]
        midpoint = (img_x / 2, img_y / 2)
        scaled_y = int(img_y * factor)
        self._img = cv2.resize(self._img, (img_x, scaled_y), interpolation=cv2.INTER_AREA)

        if self._labels is not None:
            stretched = []
            for label in self._labels:
                name = label[0]
                stretched.append([name, self.__stretch_coordinate(label[1], midpoint, factor, axis = 1),
                                 self.__stretch_coordinate(label[2], midpoint, factor, axis = 1)])
            self._labels = stretched
            self.resize_img(img_x, img_y, transformation=False)
        
        else:
            self.resize_img(img_x, img_y, resize_labels=False, transformation=False)
        return self
    
    
    # colour effects
    def __spreadLookupTable(self, x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))
  
    def warm_image(self, strength = None, graph = False):
        if strength == None:
            strength = np.random.rand()
        
        if strength >= 0 and abs(strength) <= 1:
            self._transformations.append(f"warm-{round(strength, 3)}")
            increase_x_points = [0, 64, 128, 192, 224, 255]
            increase_y_points = [0, 64 * (1+strength), 128 * (1+0.75*strength), 192*(1+0.3*strength),224*(1+0.135*strength), 255]
            decrease_x_points = [0, 64, 128, 192, 224, 255]
            decrease_y_points = [0, 64 * (1-0.9*strength), 128 * (1-0.75*strength), 192*(1-0.3*strength),224*(1-0.135*strength), 255]

            increaseLookupTable = self.__spreadLookupTable(increase_x_points, increase_y_points)
            decreaseLookupTable = self.__spreadLookupTable(decrease_x_points, decrease_y_points)

            blue_channel, green_channel, red_channel = cv2.split(self._img)
            red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)

            if graph:
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle("Warm graphs")
                ax1.plot(increaseLookupTable, label = "filter")
                ax1.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax1.axhline(y=255, color='r', linestyle='-')
                ax1.plot(increase_x_points, increase_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax1.title.set_text("Red curve")

                ax2.plot(decreaseLookupTable, label = "filter")
                ax2.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax2.plot(decrease_x_points, decrease_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax2.axhline(y=255, color='r', linestyle='-')
                ax2.title.set_text("Blue curve")

                plt.legend(loc="lower center", bbox_to_anchor=(0, -0.15), ncol= 3)
                plt.show()

            self._img = cv2.merge((blue_channel, green_channel, red_channel)) 
            return self
        else:
            print("strength ratio must be a decimal value between 0-1")

    def cool_image(self, strength = None, graph = False):
        if strength == None:
            strength = np.random.rand()
        if strength >= 0 and abs(strength) <= 1:
            self._transformations.append(f"cool-{round(strength, 3)}")
            increase_x_points = [0, 64, 128, 192, 224, 255]
            increase_y_points = [0, 64 * (1+strength), 128 * (1+0.75*strength), 192*(1+0.3*strength),224*(1+0.135*strength), 255]
            decrease_x_points = [0, 64, 128, 192, 224, 255]
            decrease_y_points = [0, 64 * (1-0.9*strength), 128 * (1-0.75*strength), 192*(1-0.3*strength),224*(1-0.135*strength), 255]

            increaseLookupTable = self.__spreadLookupTable(increase_x_points, increase_y_points)
            decreaseLookupTable = self.__spreadLookupTable(decrease_x_points, decrease_y_points)

            blue_channel, green_channel, red_channel = cv2.split(self._img)
            red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)

            if graph:
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle("Cool graphs")
                ax1.plot(increaseLookupTable, label = "filter")
                ax1.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax1.plot(increase_x_points, increase_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax1.axhline(y=255, color='r', linestyle='-')
                ax1.title.set_text("Blue curve")
                
                ax2.plot(decreaseLookupTable, label = "filter")
                ax2.plot([0,255],[0,255], "g", linestyle="--", label = "no filter")
                ax2.plot(decrease_x_points, decrease_y_points, "r", marker = "x", linestyle="None", label = "interpolation points")
                ax2.axhline(y=255, color='r', linestyle='-')
                ax2.title.set_text("Red curve")

                plt.legend(loc="lower center", bbox_to_anchor=(0, -0.15), ncol= 3)
                plt.show()
    
            self._img = cv2.merge((blue_channel, green_channel, red_channel))  
            return self
        else:
            print("strength ratio must be a decimal value between 0-1")
            
    def rand_overlay(self, graph = False):
        overlays = os.listdir('Overlays')
        overlay_imgpath = os.path.join('Overlays',overlays[np.random.randint(0,len(overlays))])
        overlay_img = cv2.imread(overlay_imgpath)
        self._transformations.append("Overlay({})".format(overlay_imgpath))
        ycrop = np.random.randint(0, overlay_img.shape[0] - self._img.shape[0])
        xcrop = np.random.randint(0, overlay_img.shape[1] - self._img.shape[1])
        
        overlay_crop = overlay_img[ycrop:ycrop+self._img.shape[0], xcrop:xcrop+self._img.shape[1]]
        
        P = 1
        while P >= 1:
            P = np.random.normal(0.75,0.05)
        Q = 1-P
        self._img = cv2.addWeighted(self._img,P,overlay_crop,Q,0)
        return self
        
    def rand_trans(self,transforms = None, probs = None):#,self.rot_90,self.rot_270,self.stretch_y,self.stretch_x]):
        
        if transforms == None:
            transforms = [self.rand_overlay,self.cool_image,self.warm_image,self.rot_180,self.reflect_x,self.reflect_y,self.stretch_y,self.stretch_x]#,self.rot_90,self.rot_270]
        if probs == None:
            # probs = [0.28,0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08]
            probs = [0.3,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        
        transformtype = np.random.choice(a=transforms,p=probs)
        transformtype()
        return self
    
    def rand_colour(self):
        
        if np.random.rand() >= 0.5:
            self.cool_image()
        else:
            self.warm_image()
        return self
    
    def rand_rot(self):
        rotchoice = np.random.rand()
        refchoice = np.random.rand()
        if rotchoice >= 0.75:
            self.rot_180()
        elif rotchoice >= 0.5:
            # self.rot_90()
            None
        elif rotchoice >= 0.25:
            # self.rot_270()
            None
            
        if refchoice >= 0.7:
            self.reflect_x()
        elif refchoice >= 0.4:
            self.reflect_y()
        else:
            None
        return self
    
    def rand_scale(self):
        if np.random.rand() >= 0.5:
            self.stretch_x()
        else:
            self.stretch_y()
        return self
    
    #output methods
    def save(self, custom_name = None, savedir = None):
        """
        Please pass in custom_name without an extension
        """
        img_ext = os.path.splitext(self._img_path)[1]

        transform_string = ""
        for transform in self._transformations:
                transform_string += f"_{transform}"

        if custom_name is None:
            if savedir is None:
                save_path = os.path.splitext(self._img_path)[0]
            else:
                filename = os.path.splitext(os.path.basename(self._img_path))[0]
                save_path = savedir + "//" + filename

            save_path += transform_string
        
        else:
            if savedir is None:
                save_path = os.path.dirname(self._img_path) + "//" + custom_name
            else:
                save_path = savedir + "//" + custom_name

        img_path = save_path + img_ext
        cv2.imwrite(img_path, self._img)  

        if self._labels is not None:
            #setting common tags
            xml_path = save_path + ".xml"

            self._soup.find("path").string = img_path
            self._soup.find("filename").string = os.path.basename(img_path) 
            self._soup.find("folder").string = os.path.basename(os.path.dirname(img_path))
            self._soup.find("height").string = str(np.shape(self._img)[0])
            self._soup.find("width").string = str(np.shape(self._img)[1])
            self._soup.find("depth").string = str(np.shape(self._img)[2])  # need to deal with case when image is not 3 channel (this won't work)
            objects = self._soup.findAll("object")
            #setting object tags
            for i, label in enumerate(self._labels):
                objects[i].find("name").string = label[0]
                objects[i].find("xmin").string = str(label[1][0])
                objects[i].find("ymin").string = str(label[1][1])
                objects[i].find("xmax").string = str(label[2][0])
                objects[i].find("ymax").string = str(label[2][1])

            for j, object in enumerate(objects):
                if j > i:
                    object.extract() 

            with open(xml_path, "w+") as fp:
                fp.write(re.sub(r".*\n", "", self._soup.prettify(), 1))
                fp.seek(0,2)
                fp.write("\n" + f"<!--{transform_string[1:]}-->")
            
                
        
        
#%% 
   
def show_labelled(outputs):
    labelled_imgs = []
    for img in outputs:
        
        labelled_img = copy.copy(img._img)
        for label in img._labels:
            labelled_img = cv2.rectangle(labelled_img, label[1], label[2], thickness=2, color=(0,0,255))
        labelled_imgs.append(labelled_img)
    concat = cv2.hconcat(labelled_imgs)
    cv2.imshow('output',concat)
    
def rand_chain(img_path,label_path,num_outputs = 6, num_passes = 1, show = False, debug = False):
        
    orig = Labelled_Img(img_path,label_path)
    outputs = [orig]
    
    # overlayed = False
    
    for output in range(num_outputs):
        image = Labelled_Img(img_path,label_path)
        # num_passes = np.abs(int(np.random.normal(num_transforms,0.5)))
        transformtypes = [image.rand_rot,image.rand_colour,image.rand_overlay,image.rand_scale]
        random.shuffle(transformtypes)

        for transform in range(num_passes):
            transformtypes[0]()
            transformtypes[1]()
            transformtypes[2]()
            transformtypes[3]()
        if debug:
            print(image._transformations,'\n')
            
        outputs.append(image) # save image
        
        if show:
            # for i in range(len(outputs)):
                # cv2.imshow('window{}'.format(i),outputs[i]._img)
            show_labelled(outputs)

    return outputs
        
        
def rand_folder(folder_path = None,file_type = '.jpg', num_outputs = 6, num_passes = 1, debug = False):
    '''This is a supervised randomisation process which waits for confirmation'''
    if folder_path is not None:
        # print(folder_path + '/*' + file_type)
        load_folder = folder_path + ' (Unprocessed Originals)'
        if not os.path.exists(load_folder):
            shutil.copytree(folder_path, load_folder)
        save_folder = folder_path + ' (Processed Transformed)'
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        move_folder = folder_path + ' (Processed Originals)'
        if not os.path.exists(move_folder):
            os.mkdir(move_folder)
        problem_folder = folder_path + ' (Problematic Originals)'
        if not os.path.exists(problem_folder):
            os.mkdir(problem_folder)
            
        file_paths = load_folder + '/*' + file_type
        
        print('Starting. Filepath:\n')
        print(file_paths+'\n')  
        
        for file_name in glob.glob(file_paths):
            print(file_name+'\n')
            xml_path = file_name[:-len(file_type)] + '.xml'
            confirmed = False
            while not confirmed:
                
                img_set = rand_chain(file_name, xml_path, num_outputs = num_outputs, num_passes = num_passes,debug = debug)
                
                show_labelled(img_set)
                if cv2.waitKey(0) & 0xFF == ord('y'):
                    for i in range(len(img_set)):
                        img_set[i].save(custom_name = '_v{}'.format(i+1), savedir=save_folder)
                    shutil.move(file_name, move_folder)
                    shutil.move(xml_path, move_folder)
                    confirmed = True
                elif cv2.waitKey(0) & 0xFF == ord('r'):
                    None
                elif cv2.waitKey(0) & 0xFF == ord('n'):
                    confirmed = True
                    shutil.move(file_name, problem_folder)
                    shutil.move(xml_path, problem_folder)
                
        
        