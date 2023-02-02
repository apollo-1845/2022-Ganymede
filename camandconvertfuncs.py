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

    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        camera.exif_tags['sunlight'] = True
    else:
        camera.exif_tags['sunlight'] = False

    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    camera.capture(image)
