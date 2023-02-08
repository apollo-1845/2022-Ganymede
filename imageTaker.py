from picamera import PiCamera
from pathlib import Path
from time import sleep
import camandconvertfuncs as cam
from datetime import datetime, timedelta
import measuringPlantHealth
from exif import Image

base_folder = Path(__file__).parent.resolve()

def takeImages():

    camera = PiCamera()
    camera.resolution = (2592, 1944)

    startTime = datetime.now()
    timeNow = datetime.now()
    i = 0
    
    array = []
    
    while (timeNow < startTime + timedelta(minutes=1)):
        path = f'{base_folder}/images/image_{i:03d}.jpg'
        long, lat, NS, EW = cam.capture(camera, path) 
        i = i + 1
        with open(path, 'rb') as _image:
            image = Image(_image)
            coordinates = [long, lat, NS, EW]
            NVDIVal = measuringPlantHealth.calculateNVDI(path)
            array.append([NVDIVal, coordinates, path])
        sleep(5)
    return array