import Nasa

# TODO: Set the directory paths according to your system
APOD_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/ApodImages"
NASA_EPIC_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaEpicImages"
MARS_ROVER_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/MarsRoverImages"
NASA_LIBRARY_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaLibraryImages"
LENA_IMAGE_PATH = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/Lena.png"

# TODO: Set the parameters for the relevant functions.
# APOD image parameters.
APOD_DATE = "2020-12-05"  # Acceptable format - YYYY-MM-DD.
HD = True

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
    Nasa.getAstronomyPictureOfTheDay(image_directory=APOD_IMAGES,
                                     date=APOD_DATE,
                                     hd=HD)

    # Nasa.getNasaEpicImage(image_directory=NASA_EPIC_IMAGES)

    # Nasa.getMarsRoverImages(image_directory=MARS_ROVER_IMAGES,
    #                         rover=ROVER, sol=SOL, date=MARS_DATE)

    # Nasa.getNasaLibraryImages(image_directory=NASA_LIBRARY_IMAGES,
    #                           q=SEARCH_QUERY,
    #                           mediaType=MEDIA_TYPE,
    #                           startYear=START_YEAR,
    #                           endYear=END_YEAR)


if __name__ == "__main__":
    main()
