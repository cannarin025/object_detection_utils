import cv2
import numpy as np

img_path = "C://Users//canna//Desktop//FLIR_snap3.jpg"
test_path = "C://Users//canna//Desktop//FLIR_snap4.jpg"
img = cv2.imread(img_path)
test = cv2.imread(test_path)
a = 2
greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def to_greyscale(img):
    """
    In-house function to convert an image to greyscale. Accounts for eye's perception of colour channel intensities and normalisation
    """
    my_grey = []
    for col in img:
        new_col = []
        for pix in col:
            intensity = np.sqrt((0.144*pix[0])**2 + (0.587*pix[1])**2 + (0.299*pix[2])**2)/0.6744  # constants to account for eye's perception of intensity and normalisation.
            new_col.append(intensity.astype(np.uint8))
        
        my_grey.append(np.array(new_col))

    my_grey = np.array(my_grey)
    return my_grey

cv2.imshow("original", img)
cv2.imshow("conv_grey", greyscale)
cv2.imshow("FLIR_grey", test)
cv2.imshow("my_grey", to_greyscale(img))
cv2.waitKey(0)


