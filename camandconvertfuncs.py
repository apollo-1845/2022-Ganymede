from orbit import ISS, ephemeris
from pathlib import Path
from skyfield.api import load
import numpy as np


timescale = load.timescale()

base_folder = Path(__file__).parent.resolve()

def convert(angle):
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle


def capture(camera, image):
    point = ISS.coordinates()

    s, latitude = convert(point.latitude)
    w, longitude = convert(point.longitude)
    
    south = "north"
    if s:
        south = "south"
    
    west = "east"
    if w:
        west = "west"
    
    t = timescale.now()
    sunlight = False
    if ISS.at(t).is_sunlit(ephemeris):
        sunlight = True
        
    camera.capture(image)
    return longitude, latitude, south, west
