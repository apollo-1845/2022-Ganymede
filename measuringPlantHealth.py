import cv2
import numpy as np
from exif import Image

def increaseContrast(path):
    OGImageim = cv2.imread(path) #read the image
    OGImage = np.array(OGImageim, dtype=float)/float(255) #convert into an array so maths can work

    inMinC = np.percentile(OGImage, 5) #min brightness in the image
    inMaxC = np.percentile(OGImage, 95) #max brightness in the image

    out_min = 0.0
    out_max = 255.0

    outputImage = OGImage - inMinC 
    outputImage *= ((out_min - out_max) / (inMinC - inMaxC)) #multiply the image by the ration between the desired range of brightness by the actual range of brightness
    outputImage += inMinC 

    return outputImage

def calculateNVDI(path):
    image = increaseContrast(path)
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi