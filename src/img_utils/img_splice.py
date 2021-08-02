import cv2
import numpy as np

img1 = "L://Code//YOLO_detection//all_IR_imgs_labelled_yolo//eval//13_22_000011_FLIR.jpg"
img2 = "L://Code//YOLO_detection//all_IR_imgs_labelled_yolo//eval//16_42_000321_FLIR.jpg"

im1 = cv2.imread(img1)
im2 = cv2.imread(img2)

cropped1 = im1[:, :int(np.shape(im1)[1]/2)]
cropped2 = im2[:, :int(np.shape(im2)[1]/2)]
combined = cv2.hconcat([cropped1, cropped2])
cv2.imshow("test",combined)
cv2.imwrite("L://Code//YOLO_detection//all_IR_imgs_labelled_yolo//eval//combined//toad_pigeon.jpg", combined)
cv2.waitKey(0)