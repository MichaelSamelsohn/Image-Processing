import requests
import logging as log
import Logging

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
NASA_LIBRARY_BASE_URL = "https://api.nasa.gov/insight_weather/?feedtype=json&ver=1.0&"


# ************************************************************************************************************** #

def getMarsWeatherServiceInformation():
    print("\nRetrieving Mars weather service information\n")
    log.debug("Retrieving Mars weather service information")

    url = NASA_LIBRARY_BASE_URL + API_KEY
    log.debug("The URL is - {}".format(url))
    r = requests.get(url)
    log.debug("Request status code is - {}".format(r.status_code))
    assert r.status_code == 200, "Status code is " + str(r.status_code)
    json_object = r.json()

    log.debug("Printing relevant information")
    sol_keys = json_object["sol_keys"]
    for sol in sol_keys:
        print("Weather information for sol #" + sol)
        for info in json_object[sol]:
            print("{} : {}".format(info, json_object[sol][info]))
        print("\n")

    log.info(
        "For full API documentation - https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf")

# ************************************************************************************************************** #
