import requests
import os
import CommandLine
import logging as log
import Logging

NASA_LIBRARY_BASE_URL = "https://images-api.nasa.gov/search?"
NUMBER_OF_PHOTOS_TO_COLLECT = 1


# ************************************************************************************************************** #

def getNasaLibraryImages(image_directory, q, mediaType, startYear, endYear):
    log.debug("Retrieving NASA library images using a query")
    log.info("Provided query is - {}".format(q))
    log.info("Selected media type is - {}".format(mediaType))
    log.info("Selected start/end years are - {} - {}".format(startYear, endYear))

    photos_url = getNasaLibraryDataUrl(q, mediaType, startYear, endYear)
    i = 0
    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.info("Images will be saved as .JPG files")
    for url in photos_url:
        log.debug("Current image number is - {}".format(i + 1))
        log.info("Current image URL is - {}".format(url))
        CommandLine.runCmd(["wget", "-O", "NASA_" + str(i) + ".JPG", url])
        i = i + 1

    log.info("For full API documentation - https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf")


def getNasaLibraryDataUrl(q, mediaType, startYear, endYear):
    log.debug("Formatting a URL for the API request")
    url_list = []
    url_complement = "q=" + formatStringWithSpace(q, "%20")
    url_complement = url_complement + "&" + "media_type=" + mediaType
    url_complement = url_complement + "&" + "year_start=" + startYear + "&" + "year_end=" + endYear

    log.debug("The API request is - {}".format(NASA_LIBRARY_BASE_URL + url_complement))
    r = requests.get(NASA_LIBRARY_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    json_object = r.json()
    log.debug(json_object)
    collection = json_object["collection"]
    items = collection["items"]

    log.info("Number of photos to collect is - {}".format(min(NUMBER_OF_PHOTOS_TO_COLLECT, len(items))))
    for i in range(0, min(NUMBER_OF_PHOTOS_TO_COLLECT, len(items))):
        item = items[i]
        links = item["links"]
        sub_item = links[0]
        url_list.append(sub_item["href"])

    return url_list


def formatStringWithSpace(strings, separator):
    formatted_string = ""
    for string in strings[:-1]:
        formatted_string = formatted_string + string + separator
    formatted_string = formatted_string + strings[-1]
    return formatted_string

# ************************************************************************************************************** #
