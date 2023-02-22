import imageTaker
from exif import Image
import csv
import reverse_geocoder as rg
import cv2
import numpy as np
from exif import Image
from picamera import PiCamera
from pathlib import Path
from time import sleep
from datetime import datetime, timedelta
from orbit import ISS, ephemeris
from skyfield.api import load

timescale = load.timescale()

base_folder = Path(__file__).parent.resolve()

#takes the images and stores them
def takeImages():

    camera = PiCamera()
    camera.resolution = (2592, 1944)

    startTime = datetime.now()
    timeNow = datetime.now()
    i = 0
    
    array = []
    
    while (timeNow < startTime + timedelta(minutes=1)):
        path = f'{base_folder}/images/image_{i:03d}.jpg'
        t = timescale.now()
        #waits until the iss is in sunlight
        while ISS.at(t).is_sunlit(ephemeris) == False:
            t = timescale.now()
        point = ISS.coordinates()
        coordinates = (point.latitude.degrees, point.longitude.degrees)
        camera.capture(path)
        NVDIVal = calculateNVDI(path)
        #adds the data to an array to save into a csv later
        array.append([NVDIVal, coordinates, path])
        i = i + 1
        sleep(3)
    return array

#measuring plant health
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
    b, _, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

#converts coordinates to the name of the country the coordinates correspond to
def coordinateToCountry(coordinates):
    results = rg.search(coordinates)
    country = results.cc
    return country

#argument is a 2d Array
def convertToCSV(array):
    with open('data.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['NDVI', 'image path', 'raw coordinate', 'country'])
        for i in range(0, len(array)):
            country, city = coordinateToCountry(array[i][1])
            filewriter.writerow([array[i][0], array[i][1], array[i][2], country])

array = imageTaker.takeImages() #takes images for the duration of the flight 
convertToCSV(array)




