import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
MARS_ROVER_PHOTOS_BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/"
NUMBER_OF_PHOTOS_TO_COLLECT = 1


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
    log.debug(json_object)
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
    log.debug(json_manifest)
    print("\nIMAGE INFORMATION:")
    json_photo_manifest = json_manifest["photo_manifest"]
    landing_date = json_photo_manifest["landing_date"]
    print("Landing date is - {}".format(landing_date))
    max_date = json_photo_manifest["max_date"]
    print("Maximum date is - {}".format(max_date))
    max_sol = json_photo_manifest["max_sol"]
    print("Maximum sol is - {}".format(max_sol))
    status = json_photo_manifest["status"]
    print("The current status of the rover is - {}".format(status))
    total_photos = json_photo_manifest["total_photos"]
    print("The total amount of photos taken by the rover is - {}".format(total_photos) + "\n")

    log.debug("returning a dictionary with the rover manifest")
    return {"rover": rover, "landing_date": landing_date, "max_date": max_date, "max_sol": max_sol,
            "status": status, "total_photos": total_photos}

# ************************************************************************************************************** #
