import logging as log
import Logging
import cv2 as cv
import numpy as np


def boxFilter(image, kernel_size, border_type):
    log.debug("Applying a box filter to an image")
    log.info("Selected kernel size is - {}".format(kernel_size))
    log.info("Selected border type is - {}".format(border_type))

    box_image = cv.blur(image, (kernel_size, kernel_size), borderType=border_type)

    log.debug("Finished applying a box filter to an image")
    return box_image


def gaussianFilter(image, kernel_size, sigma, border_type):
    log.debug("Applying a Gaussian filter to an image")
    log.info("Selected kernel size is - {}".format(kernel_size))
    log.info("Selected Sigma value is - {}".format(sigma))
    log.info("Selected border type is - {}".format(border_type))

    gaussian_image = cv.GaussianBlur(image, (kernel_size, kernel_size), sigma, borderType=border_type)

    log.debug("Finished applying a Gaussian filter to an image")
    return gaussian_image


def medianFilter(image, kernel_size):
    log.debug("Applying a median filter to an image")
    log.info("Selected kernel size is - {}".format(kernel_size))

    median_image = cv.medianBlur(image, kernel_size)

    log.debug("Finished applying a median filter to an image")
    return median_image


def bilateralFilter(image, kernel_size, sigma_color, sigma_space, border_type):
    log.debug("Applying a bilateral filter to an image")
    log.info("Selected kernel size is - {}".format(kernel_size))
    log.info("Selected Sigma color is - {}".format(sigma_color))
    log.info("Selected Sigma space is - {}".format(sigma_space))
    log.info("Selected border type is - {}".format(border_type))

    bilateral_image = cv.bilateralFilter(image, kernel_size,
                                         sigmaColor=sigma_color, sigmaSpace=sigma_space,
                                         borderType=border_type)

    log.debug("Finished applying a bilateral filter to an image")
    return bilateral_image
