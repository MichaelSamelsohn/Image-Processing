import logging as log
import Logging
import cv2 as cv
import numpy as np

from Common import extractNeighborhood
from Decorators import BookImplementation


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


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.328")
def geometricMeanFilter(image, padding_type, kernel_size):
    log.debug("Applying geometric mean filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)
    padded_normalized_image = cv.normalize(padded_image, None, 1, 0, cv.NORM_MINMAX, cv.CV_32F)

    log.debug("Scanning the image and calculating the geometric mean for each neighborhood")
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    geometric_constant = np.power(float(kernel_size), -2)
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_normalized_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            product = np.prod(neighborhood)
            post_filter_image[row][col] = np.power(product, geometric_constant)
    log.debug("Finished scanning the image and calculating the geometric mean for each neighborhood")

    return_image = cv.normalize(post_filter_image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)

    log.debug("Finished applying geometric mean filter")
    return return_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.329")
def contraHarmonicMeanFilter(image, padding_type, kernel_size, order):
    log.debug("Applying contra harmonic mean filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)
    padded_normalized_image = cv.normalize(padded_image, None, 1, 0, cv.NORM_MINMAX, cv.CV_32F)

    log.debug("Scanning the image and calculating the contra harmonic mean for each neighborhood")
    log.info("Selected order is - {}".format(order))
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_normalized_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            denominator = np.sum(np.power(neighborhood, order))
            if denominator == 0 is True:
                post_filter_image[row][col] = 1
                continue
            numerator = np.sum(np.power(neighborhood, order + 1))
            post_filter_image[row][col] = numerator / denominator
    log.debug("Finished scanning the image and calculating the geometric mean for each neighborhood")

    return_image = cv.normalize(post_filter_image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)

    log.debug("Finished applying contra harmonic mean filter")
    return return_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.330-332")
def medianFilter(image, padding_type, kernel_size):
    log.debug("Applying median filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)

    log.debug("Scanning the image and sorting each neighborhood")
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    median_constant = np.power(kernel_size, 2) // 2
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            sorted_neighborhood = neighborhood.flatten()
            sorted_neighborhood = np.sort(sorted_neighborhood)
            post_filter_image[row][col] = sorted_neighborhood[median_constant]
    log.debug("Finished scanning the image and sorting each neighborhood")

    log.debug("Finished applying median filter")
    return post_filter_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.332")
def minmaxFilter(image, padding_type, kernel_size, min_or_max):
    log.debug("Applying min/max filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    options = {"min": np.min, "max": np.max}

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)

    log.debug("Scanning the image and sorting each neighborhood")
    log.info("Selected option (min/max) is - {}".format(min_or_max))
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            post_filter_image[row][col] = options[min_or_max](neighborhood)
    log.debug("Finished scanning the image and sorting each neighborhood")

    log.debug("Finished applying min/max filter")
    return post_filter_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.332")
def midpointFilter(image, padding_type, kernel_size):
    log.debug("Applying midpoint filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)

    log.debug("Scanning the image and sorting each neighborhood")
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            post_filter_image[row][col] = 0.5 * (np.min(neighborhood) + np.max(neighborhood))
    log.debug("Finished scanning the image and sorting each neighborhood")

    log.debug("Finished applying midpoint filter")
    return post_filter_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 5.3 - Restoration in the Presence of Noise Only—Spatial Filtering, p.332-333")
def alphaTrimmedMeanFilter(image, padding_type, kernel_size, trim_factor):
    # TODO: Add check that trim factor is an integer (between 0 and (filtersize^2 - 1) /2)
    log.debug("Applying alpha trimmed mean filter")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Chosen kernel size is - {}".format(kernel_size))

    padded_image = cv.copyMakeBorder(image,
                                     kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                                     padding_type)

    log.debug("Scanning the image and sorting each neighborhood")
    width, height = image.shape
    post_filter_image = np.zeros((width, height))
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=padded_image,
                                               row=row + kernel_size // 2, col=col + kernel_size // 2,
                                               neighborhood_size=kernel_size)
            sorted_neighborhood = neighborhood.flatten()
            sorted_neighborhood = np.sort(sorted_neighborhood)
            post_filter_image[row][col] = np.sum(sorted_neighborhood[trim_factor:-trim_factor]) \
                                          / (len(sorted_neighborhood) - 2 * trim_factor)
    log.debug("Finished scanning the image and sorting each neighborhood")

    log.debug("Finished applying alpha trimmed mean filter")
    return post_filter_image
