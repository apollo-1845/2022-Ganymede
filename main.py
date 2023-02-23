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
    #runs f
    while (timeNow < startTime + timedelta(minutes=160)):
        try:
            path = f'{base_folder}/images/image_{i:03d}.jpg'
            #waits until the iss is in sunlight
            t = timescale.now()
            while ISS.at(t).is_sunlit(ephemeris) == False:
                t = timescale.now()
            point = ISS.coordinates()
            coordinates = (point.latitude.degrees, point.longitude.degrees)
            country = coordinateToCountry(coordinates)
            camera.capture(path)
            try:
                img = cv2.imread(path)
                x1 = 390
                x2 = 2200
                y1 = 390
                y2 = 1560
                img_cropped = img[x1:x2, y1:y2]
                cv2.imwrite(img_cropped, path)
            except:
                pass
            #adds the data to an array to save into a csv later
            with open('data.csv', 'w') as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow([coordinates, path, country])
            i = i + 1
            #waits ten seconds between each photo
            sleep(5)
            timeNow = datetime.now()
        except: 
            pass
    return

#converts coordinates to the name of the country the coordinates correspond to
def coordinateToCountry(coordinates):
    try: 
        results = rg.search(coordinates)
        country = results[0]['cc']
    except: 
        pass
    return country

#writes the csv headers
with open('data.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    filewriter.writerow(['raw-coordinate', 'image-path', 'country'])

#takes the images and saves them
takeImages()

#we will create ndvi images later in the analysis phase and compare that to the countries GDP. 
