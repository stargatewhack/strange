#python -m pip install --user numpy
import numpy as np
import cv2
from time import sleep

#Unfortunatley, the rotate function can only handle individual degrees
#We can grab all 360 degrees, and then later, use skipped data to get
# the 240 desired segments.
na = 360
angle = 1

pixel_w = 80
pixel_h = 80

# Creating the POV image (at this point) is a half-manual, half-automatic
#    process. Since the POV only contains 40 LEDs, the resolution will not
#    be so high as to be able to simply transform a normal image.
# Since we want to optimize the image quality on the POV, we will need to
#    do some manual tweaking.
# Do each step of the process individually, commenting out all other steps
#    they are run.

# To comment out sections, highlight and use ctrl+3. (ctrl + 4 to unhighlight)

def main():

##    # Step 0: Load and view image
##    img = cv2.imread('shieldSquare2.png',0)
##    cv2.imshow('image',img)
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()

    
##    # Step 1: Load an color image in grayscale. Threshold the image
##    #           to get a solid black/white contrast
##    img = cv2.imread('shieldSquare2.png',0)
##    step1_CreateThesholdImage(img)


##    # Step 2: Edit threshold image in Paint/Gimp to fill all
##    #           lines that were missed.
    

##    # Step 3: Scan filled image and transform to POV image. (unscaled)
##    img = cv2.imread('bwShieldFilled.png',0)
##    step3_ScanFlattenImage(img, 1)

##    # Step 4: At this point the image isn't good enough to display...
##    #           Need some manual clean up, not sure how to do that
##    #           programatically. Do it manually for now to optimize
##    #           the 40 pixels we have to play with.
    
    # Step 5: Resize image to 40x360 resolution for POV
    #resizedImage = cv2.resize(pixelMatrix, (360, 40)) 
    #cv2.imshow('image',resizedImage)
    #cv2.imwrite('resized_image.png',resizedImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def step1_CreateThesholdImage(img):

    # Taking B/W Image and making a B/W threshold for distinct lines
    threshImg = thresholdImage(img)
    cv2.imshow('B/W Threshold',threshImg)
    cv2.waitKey(0)
    cv2.imwrite('bwThreshold.png',threshImg)
    cv2.destroyAllWindows()

def step3_ScanFlattenImage(img, preview):

    var = img.shape
    height = var[0]
    width = var[1]
    half_w = width/2
    half_h = height/2

    # Creates a list containing na lists, each of height/2 items, all set to 0
    w, h = na, height/2;
    #pixelMatrix = [[0 for x in range(w)] for y in range(h)] 
    pixelMatrix = np.zeros((w, h))

    for x in range(0, na):

        #Rotate Image and grab line of pixels
        imgRot = rotateImage(img, angle*x)
        pixelMatrix[x] = imgRot[half_w, 0:half_h]

        #Preview what's happening
        if(preview):
            viewScanPreview(imgRot, half_w, half_h)

    cv2.destroyAllWindows()

    pixelMatrix = np.transpose(pixelMatrix)
    cv2.imshow('POV Flat Image',pixelMatrix)
    cv2.imwrite('povFlatImage.png',pixelMatrix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def thresholdImage(image):
    ret, threshImg = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    return threshImg
  
def viewScanPreview(image,half_w,half_h):
    imgPrev = image
    imgPrev[half_w, 0:half_h] = 250
    cv2.imshow('Scanning Image',imgPrev)
    cv2.waitKey(10)

if __name__ == '__main__':
    main()
