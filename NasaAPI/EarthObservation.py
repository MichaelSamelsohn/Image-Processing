import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
EARTH_OBSERVATION_ASSETS_BASE_URL = "https://api.nasa.gov/planetary/earth/assets?"
EARTH_OBSERVATION_IMAGERY_BASE_URL = "https://api.nasa.gov/planetary/earth/imagery?"


# ************************************************************************************************************** #

def getEarthObservationImage(image_directory, lat, lon, dim, date, direct_method):
    # TODO: Add explanation to the difference between the methods (direct/indirect).
    log.debug("Retrieving Earth observation information and images")
    log.info("The selected directory is - {}".format(image_directory))
    log.info("Selected latitude is - {}".format(lat))
    log.info("Selected longitude is - {}".format(lon))
    log.info("Selected dimension (width and height of image in degrees) is - {}".format(dim))
    log.info("Selected date is - {}".format(date))
    log.warning("Format for date is - YYYY-MM-DD")
    log.debug("Will use direct method - {}".format(direct_method))

    if direct_method is False:
        url = getEarthObservationImageUrl(lat=lat,
                                          lon=lon,
                                          dim=dim,
                                          date=date)
    else:
        url = EARTH_OBSERVATION_IMAGERY_BASE_URL + formatUrlComplement(lat=lat,
                                                                       lon=lon,
                                                                       dim=dim,
                                                                       date=date)

    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.info("Images will be saved as .png files")

    log.info("Image URL is - {}".format(url))
    CommandLine.runCmd(['curl', '-o',
                        "EARTH_" + str(lat) + "_" + str(lon) + "_" + str(dim) + "_" + str(date) +
                        ".png ", url])

    log.info("For full API documentation - https://api.nasa.gov/")


def getEarthObservationImageUrl(lat, lon, dim, date):
    log.debug("Using API GET request to receive the JSON with the relevant information")
    url_complement = formatUrlComplement(lat=lat,
                                         lon=lon,
                                         dim=dim,
                                         date=date)
    log.debug("The API request is - {}".format(EARTH_OBSERVATION_ASSETS_BASE_URL + url_complement))
    r = requests.get(EARTH_OBSERVATION_ASSETS_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    json_object = r.json()
    log.debug(json_object)
    url = json_object["url"]
    return url


def formatUrlComplement(lat, lon, dim, date):
    url_complement = "lat=" + str(lat) + \
                     "&" + "lon=" + str(lon) + \
                     "&" + "dim=" + str(dim) + \
                     "&" + "date=" + date
    return url_complement + "&" + API_KEY

# ************************************************************************************************************** #
