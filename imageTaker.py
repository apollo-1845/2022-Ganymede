from picamera import PiCamera
from pathlib import Path
from time import sleep
import camandconvertfuncs as cam
from datetime import datetime, timedelta

base_folder = Path(__file__).parent.resolve()

def takeImages():

    camera = PiCamera()
    camera.resolution = (2592, 1944)

    startTime = datetime.now()
    timeNow = datetime.now()
    i = 0

    while (timeNow < startTime + timedelta(minutes=176)):
        cam.capture(camera, f'{base_folder}/images/image_{i:03d}.jpg') 
        i = i + 1
        sleep(5)
    return i