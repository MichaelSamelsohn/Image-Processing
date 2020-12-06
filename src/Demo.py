from APOD import getAstronomyPictureOfTheDay
from EPIC import getNasaEpicImage
from EarthObservation import getEarthObservationImage
from ImageLibrary import getNasaLibraryImages
from MarsRovers import getMarsRoverImages

# TODO: Set the directory paths according to your system
from TechTransfer import getTechTransferInformation

APOD_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/ApodImages"
NASA_EPIC_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaEpicImages"
MARS_ROVER_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/MarsRoverImages"
NASA_LIBRARY_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaLibraryImages"
EARTH_OBSERVATION_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/EarthObservationImages"

# TODO: Set the parameters for the relevant functions.
# APOD image parameters.
APOD_DATE = "2020-12-05"  # Acceptable format - YYYY-MM-DD.
HD = True

# Earth observation images parameters.
LAT = 34.79
LON = 31.97
DIM = 0.1
EARTH_OBSERVATION_DATE = "2020-11-11"
DIRECT_METHOD = True  # Two ways to retrieve the image.

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
    getAstronomyPictureOfTheDay(image_directory=APOD_IMAGES,
                                date=APOD_DATE,
                                hd=HD)

    getEarthObservationImage(image_directory=EARTH_OBSERVATION_IMAGES,
                             lat=LAT,
                             lon=LON,
                             dim=DIM,
                             date=EARTH_OBSERVATION_DATE,
                             direct_method=DIRECT_METHOD)

    getTechTransferInformation(parameter=QUERY_TYPE, query=QUERY_TECH_TRANSFER)

    getNasaEpicImage(image_directory=NASA_EPIC_IMAGES)

    getMarsRoverImages(image_directory=MARS_ROVER_IMAGES,
                       rover=ROVER,
                       sol=SOL,
                       date=MARS_DATE)

    getNasaLibraryImages(image_directory=NASA_LIBRARY_IMAGES,
                         q=SEARCH_QUERY,
                         mediaType=MEDIA_TYPE,
                         startYear=START_YEAR,
                         endYear=END_YEAR)


if __name__ == "__main__":
    main()
