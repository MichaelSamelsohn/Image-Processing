import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
APOD_BASE_URL = "https://api.nasa.gov/planetary/apod?"


# ************************************************************************************************************** #

def getAstronomyPictureOfTheDay(image_directory, date, hd):
    log.debug("Retrieving APOD (Astronomy Picture Of the Day) image")
    log.debug("The selected directory is - {}".format(image_directory))
    log.debug("Selected date is - {}".format(date))
    log.warning("Date format has to be YYYY-MM-DD of an existing date")
    log.debug("HD version of the image - {}".format(hd))

    url = getAstronomyPictureOfTheDayUrl(date, hd)
    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.debug("Images will be saved as .JPG files")
    log.debug("Image URL is - {}".format(url))
    CommandLine.runCmd(["wget", "-O", "APOD_" + date + ".JPG", url])

    log.info("For full API documentation - https://api.nasa.gov/")


def getAstronomyPictureOfTheDayUrl(date, hd):
    log.debug("Using API GET request to receive the JSON with the relevant information")

    url_complement = "date=" + date + "&" + API_KEY
    log.debug("The API request is - {}".format(APOD_BASE_URL + url_complement))
    r = requests.get(APOD_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    if r.status_code == 400:
        log.warning("Perhaps bad date format or non-existing date given?")
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    log.debug("Compiling a URL list of the images to retrieve")
    json_object = r.json()
    log.info(json_object)

    log.debug("IMAGE INFORMATION:")
    for data in json_object:
        print("{} - {}".format(data.upper(), json_object[data]))

    return json_object["hdurl"] if hd is True else json_object["url"]

# ************************************************************************************************************** #
