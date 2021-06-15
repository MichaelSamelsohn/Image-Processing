import logging

import pytest
import requests
import os.path
from os import path

from APOD import getAstronomyPictureOfTheDayUrl, getAstronomyPictureOfTheDay

API_KEY = "api_key=fymalkzvEUpMBhhBIpi39IQu0zqsjMy7K2AYhiwJ"
APOD_BASE_URL = "https://api.nasa.gov/planetary/apod?"


@pytest.fixture
def supply_APOD_Date():
    correct_formatted_date = "2000-04-27"
    wrong_formatted_date = "27-04-2000"
    non_existing_date = "2100-04-27"
    return [correct_formatted_date, wrong_formatted_date, non_existing_date]


def test_APOD_API_ReturnsCorrectResult(supply_APOD_Date):
    r = requests.get(APOD_BASE_URL + "date=" + supply_APOD_Date[0] + "&" + API_KEY)
    assert r.status_code == 200, r.status_code

    json_object = r.json()
    assert json_object["date"] == supply_APOD_Date[0]
    assert json_object["hdurl"] == "https://apod.nasa.gov/apod/image/0004/iosouth_gal_big.jpg"
    assert json_object["media_type"] == "image"
    assert json_object["service_version"] == "v1"
    assert json_object["title"] == "Calderas And Cliffs Near Io's South Pole"
    assert json_object["url"] == "https://apod.nasa.gov/apod/image/0004/iosouth_gal.jpg"


def test_APOD_API_BadDateFormatReturns400(supply_APOD_Date):
    r = requests.get(APOD_BASE_URL + "date=" + supply_APOD_Date[1] + "&" + API_KEY)
    assert r.status_code == 400, r.status_code


def test_APOD_API_NonExistingDateReturns400(supply_APOD_Date):
    r = requests.get(APOD_BASE_URL + "date=" + supply_APOD_Date[2] + "&" + API_KEY)
    assert r.status_code == 400, r.status_code


def test_APOD_getAstronomyPictureOfTheDayUrl_HdTrue(supply_APOD_Date):
    image_url = getAstronomyPictureOfTheDayUrl(supply_APOD_Date[0], True)
    assert image_url == "https://apod.nasa.gov/apod/image/0004/iosouth_gal_big.jpg"


def test_APOD_getAstronomyPictureOfTheDayUrl_HdFalse(supply_APOD_Date):
    image_url = getAstronomyPictureOfTheDayUrl(date=supply_APOD_Date[0], hd=False)
    assert image_url == "https://apod.nasa.gov/apod/image/0004/iosouth_gal.jpg"


def test_APOD_ImageIsSavedToCorrectDirectory(supply_APOD_Date, tmpdir):
    image_directory = tmpdir.mkdir("Images")
    getAstronomyPictureOfTheDay(image_directory=image_directory, date=supply_APOD_Date[0], hd=True)
    assert len(image_directory.listdir()) == 1
    assert path.exists(image_directory + "/APOD_" + supply_APOD_Date[0] + ".JPG")
