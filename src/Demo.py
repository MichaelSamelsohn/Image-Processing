import NasaAPI

from APOD import getAstronomyPictureOfTheDay
from EPIC import getNasaEpicImage
from ImageLibrary import getNasaLibraryImages
from MarsRovers import getMarsRoverImages

# TODO: Set the directory paths according to your system
from TechTransfer import getTechTransferInformation

APOD_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/ApodImages"
NASA_EPIC_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaEpicImages"
MARS_ROVER_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/MarsRoverImages"
NASA_LIBRARY_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaLibraryImages"
LENA_IMAGE_PATH = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/Lena.png"

# TODO: Set the parameters for the relevant functions.
# APOD image parameters.
APOD_DATE = "2020-12-05"  # Acceptable format - YYYY-MM-DD.
HD = True

# Tech transfer information parameters.
QUERY_TYPE = "software"  # Options are - patent/patent_issued/software/Spinoff.
QUERY_TECH_TRANSFER = ""  # Can be left empty.

# Mars rover parameters.
ROVER = "curiosity"
SOL = True
MARS_DATE = 1000

# Library image parameters.
SEARCH_QUERY = ["Orion", "Nebula"]
MEDIA_TYPE = "image"  # Currently, the only one working. DO NOT CHANGE!
START_YEAR = "1920"
END_YEAR = "2020"


def main():
    # getAstronomyPictureOfTheDay(image_directory=APOD_IMAGES,
    #                             date=APOD_DATE,
    #                             hd=HD)

    getTechTransferInformation(parameter=QUERY_TYPE, query=QUERY_TECH_TRANSFER)

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


if __name__ == "__main__":
    main()
