import imageTaker
import measuringPlantHealth
from exif import Image
import convertToCSV

array = imageTaker.takeImages()

convertToCSV.convertToCSV(array)





