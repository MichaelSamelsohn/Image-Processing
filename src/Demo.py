from APOD import getAstronomyPictureOfTheDay
from DataProcessing.src import Image
from DataProcessing.src.Image import Image
from EPIC import getNasaEpicImage
from EarthObservation import getEarthObservationImage
from ImageLibrary import getNasaLibraryImages
from MWSA import getMarsWeatherServiceInformation
from MarsRovers import getMarsRoverImages
import cv2 as cv

# TODO: Set the directory paths according to your system
from TechTransfer import getTechTransferInformation

APOD_IMAGES = "/Users/michaelsamelsohn/Desktop/"
NASA_EPIC_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaEpicImages"
MARS_ROVER_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/MarsRoverImages"
NASA_LIBRARY_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaLibraryImages"
EARTH_OBSERVATION_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/EarthObservationImages"

# TODO: Set the parameters for the relevant functions.
# APOD image parameters.
APOD_DATE = "1996-04-27"  # Acceptable format - YYYY-MM-DD.
HD = True

# Earth observation images parameters.
LAT = 1.5
LON = 100.75
DIM = 0.025
EARTH_OBSERVATION_DATE = "2020-12-08"
DIRECT_METHOD = True  # Two ways to retrieve the image.

# Tech transfer information parameters.
QUERY_TYPE = "patent"  # Options are - patent/patent_issued/software/Spinoff.
QUERY_TECH_TRANSFER = "spacecraft"  # Can be left empty.

# Mars rover parameters.
ROVER = "curiosity"
SOL = True
MARS_DATE = 1000

# Library image parameters.
SEARCH_QUERY = ["Planet", "Earth"]
MEDIA_TYPE = "image"  # Currently, the only one working. DO NOT CHANGE!
START_YEAR = "2019"
END_YEAR = "2020"


def main():
    # getAstronomyPictureOfTheDay(image_directory=APOD_IMAGES,
    #                             date=APOD_DATE,
    #                             hd=HD)

    # getEarthObservationImage(image_directory=EARTH_OBSERVATION_IMAGES,
    #                          lat=LAT,
    #                          lon=LON,
    #                          dim=DIM,
    #                          date=EARTH_OBSERVATION_DATE,
    #                          direct_method=DIRECT_METHOD)
    #
    # getMarsWeatherServiceInformation()
    #
    # getTechTransferInformation(parameter=QUERY_TYPE, query=QUERY_TECH_TRANSFER)
    #
    # getNasaEpicImage(image_directory=NASA_EPIC_IMAGES)
    #
    # getMarsRoverImages(image_directory=MARS_ROVER_IMAGES,
    #                    rover=ROVER,
    #                    sol=SOL,
    #                    date=MARS_DATE)
    #
    # getNasaLibraryImages(image_directory=NASA_LIBRARY_IMAGES,
    #                      q=SEARCH_QUERY,
    #                      mediaType=MEDIA_TYPE,
    #                      startYear=START_YEAR,
    #                      endYear=END_YEAR)

    test = Image(
        filename="/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/DataProcessing/Images/Lena.png")
    # test.convertToGrayscale()
    test.showChannelHistogram(1)


if __name__ == "__main__":
    main()
