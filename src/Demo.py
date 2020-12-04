import Nasa

# TODO: Set the directory paths according to your system
NASA_EPIC_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaEpicImages"
MARS_ROVER_IMAGES_DIRECTORY = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/MarsRoverImages"
NASA_LIBRARY_IMAGES = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/NasaLibraryImages"
LENA_IMAGE_PATH = "/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Images/Lena.png"

# TODO: Set the parameters for the NASA Mars rover, image library and image processing functions.
# Mars rover parameters.
ROVER = "curiosity"
SOL = True
DATE = 1000

# Library image parameters.
SEARCH_QUERY = ["Orion", "nebula"]
MEDIA_TYPE = "image"  # Currently, the only one working. DO NOT CHANGE!
START_YEAR = "1920"
END_YEAR = "2020"


def main():
    Nasa.getNasaEpicImage(image_directory=NASA_EPIC_IMAGES)

    Nasa.getMarsRoverImages(image_directory=MARS_ROVER_IMAGES_DIRECTORY,
                            rover=ROVER, sol=SOL, date=DATE)

    Nasa.getNasaLibraryImages(image_directory=NASA_LIBRARY_IMAGES,
                              q=SEARCH_QUERY,
                              mediaType=MEDIA_TYPE,
                              startYear=START_YEAR,
                              endYear=END_YEAR)


if __name__ == "__main__":
    main()
