import requests
import os
import CommandLine
import logging as log
import Logging

EPIC_BASE_URL = "https://epic.gsfc.nasa.gov/"
NUMBER_OF_PHOTOS_TO_COLLECT = 1


# ************************************************************************************************************** #

def getNasaEpicImage(image_directory):
    log.debug("Retrieving Nasa EPIC (Earth Polychromatic Imaging Camera) images")
    log.info("The selected directory is - {}".format(image_directory))

    url_list = getNasaEpicImagesUrl()
    i = 0
    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.info("Images will be saved as .png files")
    for url in url_list:
        log.debug("Current image number is - {}".format(i + 1))
        log.info("Current image URL is - {}".format(url))
        CommandLine.runCmd(['curl', '-o', "EPIC_" + str(i) + ".png ", url])
        i = i + 1

    log.info("For full API documentation - https://epic.gsfc.nasa.gov/about/api")


def getNasaEpicImagesUrl():
    log.debug("Using API GET request to receive the JSON with the relevant information")
    url_list = []
    url_complement = "api/images.php"
    log.debug("The API request is - {}".format(EPIC_BASE_URL + url_complement))
    r = requests.get(EPIC_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    log.debug("Compiling a URL list of the images to retrieve")
    json_array = r.json()
    log.debug(json_array)
    log.info("Number of photos to collect is - {}".format(min(NUMBER_OF_PHOTOS_TO_COLLECT, len(json_array))))
    for i in range(0, min(NUMBER_OF_PHOTOS_TO_COLLECT, len(json_array))):
        log.debug("Current image number is - {}".format(i + 1))
        image = json_array[i]
        image_id = image["image"]
        year, month, day = reformatImagesUrl(image["date"])
        url_list.append(
            EPIC_BASE_URL + "archive/natural/" + year + "/" + month + "/" + day + "/png/" + image_id + ".png")
    return url_list


def reformatImagesUrl(image_date):
    log.debug("Extracting date and time information for image URL")
    date_and_time = image_date.split(" ")
    date_only = date_and_time[0].split("-")
    year = date_only[0]
    month = date_only[1]
    day = date_only[2]
    return year, month, day

# ************************************************************************************************************** #
