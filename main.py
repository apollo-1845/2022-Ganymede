import imageTaker
import measuringPlantHealth
import countryWorkerOuter
from exif import Image

noOfImagesTaken = imageTaker.takeImages()
array = []

for i in range(0, noOfImagesTaken):
    path = '{imageTaker.base_folder}/images/image_{i:03d}.jpg'
    with open(path, 'rb') as _image:
        image = Image(_image)
        coordinates = [image.GPS.GPSLatitude, image.GPS.GPSLatitudeRef, image.GPS.GPSLongitude, image.GPS.GPSLongitudeRef]
        NVDIVal = measuringPlantHealth.calculateNVDI(path)
        array.append([NVDIVal, coordinates, path])



