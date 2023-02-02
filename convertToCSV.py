import csv

#argument is a 2d Array
def convertToCSV(array):
    with open('data.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['NDVI', 'image path', 'raw coordinate'])
        for i in range(0, len(array)):
            filewriter.writerow([array[i][0], array[i][1], array[i][2]])