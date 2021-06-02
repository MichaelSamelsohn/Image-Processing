import logging as log
import Logging
import cv2 as cv
import numpy as np


def erosion(image, kernel, iterations):
    log.debug("Performing erosion on an image")
    log.info("Selected number of iterations is  - {}".format(iterations))

    eroded_image = cv.erode(image, kernel=kernel, iterations=iterations)

    log.debug("Performing erosion on an image")
    return eroded_image


def dilation(image, kernel, iterations):
    log.debug("Performing dilation on an image")
    log.info("Selected number of iterations is  - {}".format(iterations))

    dilated_image = cv.dilate(image, kernel=kernel, iterations=iterations)

    log.debug("Performing dilation on an image")
    return dilated_image


def opening(image, kernel):
    log.debug("Performing opening on an image")

    opened_image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel=kernel)

    log.debug("Performing opening on an image")
    return opened_image


def closing(image, kernel):
    log.debug("Performing closing on an image")

    closed_image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel=kernel)

    log.debug("Performing closing on an image")
    return closed_image


def morphGradient(image, kernel):
    log.debug("Performing morphological gradient on an image")

    morph_gradient = cv.morphologyEx(image, cv.MORPH_GRADIENT, kernel=kernel)

    log.debug("Performing morphological gradient on an image")
    return morph_gradient
