import requests
import os
import CommandLine
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
TECH_TRANSFER_BASE_URL = "https://api.nasa.gov/techtransfer/"


# ************************************************************************************************************** #

def getTechTransferInformation(parameter, query):
    log.debug("Retrieving information of innovations developed for exploration and discovery")
    log.info("The selected parameter (query type) is - {}".format(parameter))
    log.info("Selected query is - {}".format(query))

    if query is not "":
        url_complement = parameter + "/?" + query + "&" + API_KEY
    else:
        url_complement = parameter + "/?" + API_KEY

    log.debug("The API request is - {}".format(TECH_TRANSFER_BASE_URL + url_complement))
    r = requests.get(TECH_TRANSFER_BASE_URL + url_complement)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)

    log.debug("Printing retrieved information")
    json_object = r.json()
    log.debug(json_object)

    results_array = json_object["results"]
    num_of_objects = len(results_array)
    log.info("Total amount of objects found is - {}".format(num_of_objects))
    for result in results_array:
        print("TECHNOLOGY INFORMATION:")
        for info in result:
            if info is not "" or None:
                print(info)
        print("\n")

    log.info("For full API documentation - https://api.nasa.gov/")
