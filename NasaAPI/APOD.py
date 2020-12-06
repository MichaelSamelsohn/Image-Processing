import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
APOD_BASE_URL = "https://api.nasa.gov/planetary/apod?"
NUMBER_OF_PHOTOS_TO_COLLECT = 1


# ************************************************************************************************************** #

def getAstronomyPictureOfTheDay(image_directory, date, hd):
    log.debug("Retrieving APOD (Astronomy Picture Of the Day) image")
    log.info("The selected directory is - {}".format(image_directory))
    log.info("Selected date is - {}".format(date))
    log.warning("Date format has to be YYYY-MM-DD of an existing date")
    log.info("HD version of the image - {}".format(hd))

    url = getAstronomyPictureOfTheDayUrl(date, hd)
    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.info("Images will be saved as .JPG files")
    log.info("Image URL is - {}".format(url))
    CommandLine.runCmd(["wget", "-O", "APOD_" + date + ".JPG", url])

    log.info("For full API documentation - https://api.nasa.gov/")


def getAstronomyPictureOfTheDayUrl(date, hd):
    log.debug("Using API GET request to receive the JSON with the relevant information")

    url_complement = "date=" + date + "&" + "hd=" + str(hd) + "&" + API_KEY
    log.debug("The API request is - {}".format(APOD_BASE_URL + url_complement))
    r = requests.get(APOD_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    if r.status_code == 400:
        log.warning("Perhaps bad date format or non-existing date given?")
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    log.debug("Compiling a URL list of the images to retrieve")
    json_object = r.json()
    log.debug(json_object)

    print("\nIMAGE INFORMATION:")
    copy_right = json_object["copyright"]
    print("Copyright - {}".format(copy_right))
    date = json_object["date"]
    print("Date - {}".format(date))
    explanation = json_object["explanation"]
    print("explanation - {}".format(explanation))
    media_type = json_object["media_type"]
    print("media_type - {}".format(media_type))
    service_version = json_object["service_version"]
    print("service_version - {}".format(service_version))
    title = json_object["title"]
    print("title - {}".format(title))
    url = json_object["url"]
    print("url - {}".format(url) + "\n")

    return url

# ************************************************************************************************************** #
