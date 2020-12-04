import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
EPIC_BASE_URL = "https://epic.gsfc.nasa.gov/"
MARS_ROVER_PHOTOS_BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/"
NASA_LIBRARY_BASE_URL = "https://images-api.nasa.gov/search?"
NUMBER_OF_PHOTOS_TO_COLLECT = 4


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


def getMarsRoverImages(image_directory, rover, sol, date):
    log.debug("Retrieving Mars rover images")
    log.info("The options for the Mars rovers are - Spirit/Opportunity/Curiosity")
    log.info("The selected directory is - {}".format(image_directory))
    log.info("The selected rover is - {}".format(rover))
    log.info("The selected sol (day) is - {}".format(date))
    log.info("The selected date format (Earth/Mars dates) is - {}".format(sol))

    photos_url = getMarsRoverImagesUrl(getMarsRoverManifest(rover), sol, date)
    i = 0
    log.debug("Changing command line working directory to given directory")
    os.chdir(image_directory)
    log.info("Images will be saved as .JPG files")
    for url in photos_url:
        log.debug("Current image number is - {}".format(i + 1))
        log.info("Current image URL is - {}".format(url))
        CommandLine.runCmd(["wget", "-O", "MARS_" + str(i) + ".JPG", url])
        i = i + 1

    log.info("For full API documentation - https://api.nasa.gov/")


def getMarsRoverImagesUrl(photo_manifest, sol, date):
    log.debug("Using API GET request to receive the JSON with the relevant information")
    url_list = []

    log.debug("Diffrentiating the URL component depending on the date format (Earth/Mars)")
    if sol:
        url_complement = "rovers/" + photo_manifest["rover"] + "/photos?sol=" + str(date) + "&" + API_KEY
    else:
        url_complement = "rovers/" + photo_manifest["rover"] + "/photos?earth_date=" + str(date) + "&" + API_KEY
    log.debug("The URL component is - {}".format(url_complement))

    r = requests.get(MARS_ROVER_PHOTOS_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    log.debug("Compiling a URL list of images to retrieve")
    json_object = r.json()
    json_array = json_object["photos"]
    for i in range(0, min(NUMBER_OF_PHOTOS_TO_COLLECT, len(json_array))):
        photo = json_array[i]
        url_list.append(photo["img_src"])

    return url_list


def getMarsRoverManifest(rover):
    log.debug("Retrieve the Mars rover manifest")
    url_complement = "manifests/" + rover + "?" + API_KEY
    log.debug("The API request is - {}".format(MARS_ROVER_PHOTOS_BASE_URL + url_complement))
    r = requests.get(MARS_ROVER_PHOTOS_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    json_manifest = r.json()
    json_photo_manifest = json_manifest["photo_manifest"]
    landing_date = json_photo_manifest["landing_date"]
    log.info("Landing date is - {}".format(landing_date))
    max_date = json_photo_manifest["max_date"]
    log.info("Maximum date is - {}".format(max_date))
    max_sol = json_photo_manifest["max_sol"]
    log.info("Maximum sol is - {}".format(max_sol))
    status = json_photo_manifest["status"]
    log.info("The current status of the rover is - {}".format(status))
    total_photos = json_photo_manifest["total_photos"]
    log.info("The total amount of photos taken by the rover is - {}".format(total_photos))

    log.debug("returning a dictionary with the rover manifest")
    return {"rover": rover, "landing_date": landing_date, "max_date": max_date, "max_sol": max_sol,
            "status": status, "total_photos": total_photos}


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
