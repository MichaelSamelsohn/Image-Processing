import logging as log
import Logging
import cv2 as cv
import numpy as np

from DataProcessing.ImageProcessing.Decorators import BookImplementation


def binarization(image, threshold_value):
    # TODO: Check if threshold values are between 0-255.
    # Transforming the image to its binary version using the provided threshold.
    # Comparing pixel values against provided threshold. If pixel value is larger, multiply by 255 (white).
    # Otherwise, leave it as zero (black).
    log.debug("Performing image thresholding")
    log.info("The provided threshold is - {}".format(threshold_value))
    threshold_image = (image > threshold_value) * 255
    log.debug("Finished performing image thresholding")
    return threshold_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.122-123")
def negative(image):
    # Perform image negative. Simply subtract every value of the matrix from 255.
    log.debug("Performing image negative")
    negative_image = 255 - image
    log.debug("Finished performing image negative")
    return negative_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="??")  # TODO: Add reference.
def gammaCorrection(image, gamma):
    log.debug("Performing Gamma correction to an image")
    log.info("Selected Gamma value is - {}".format(gamma))
    gamma_correction = image / 255.0
    gamma_correction = np.power(gamma_correction, gamma)
    log.debug("Finished performing Gamma correction to an image")
    return gamma_correction


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.131-133")
def bitPlaneReconstruction(image, degree_of_reduction):
    # Bit plane reconstruction.
    # The degree of reduction indicates how many bit planes we dismiss from the LSB.
    # If degree of reduction is 0 (minimal value), all bit planes are included (original image).
    # If degree of reduction is 1, all bit planes are included excluding the LSB.
    # If degree of reduction is 7 (maximal value), only the MSB is included.
    log.debug("Performing image color reduction")

    if type(degree_of_reduction) is not int:
        log.error("The selected bit plane is not of type integer")
        return
    if degree_of_reduction < 0 or degree_of_reduction > 7:
        log.warning("The provided degree of reduction is out of range (0-7)")
        degree_of_reduction = min(7, abs(degree_of_reduction))
        log.debug("The used degree of reduction is - {}".format(degree_of_reduction))

    reduction_factor = np.power(2, degree_of_reduction)
    log.info(
        "The provided degree of reduction is - {}({})".format(degree_of_reduction, reduction_factor))
    reconstructed_image = image // reduction_factor * reduction_factor

    log.debug("Finished performing image color reduction")
    return reconstructed_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.131-133")
def bitPlaneSlicing(image, bit_plane):
    log.debug("Performing bit plane slicing")
    log.info("The chosen bit plane is - {}".format(bit_plane))

    if type(bit_plane) is not int:
        log.error("The selected bit plane is not of type integer")
        return
    if bit_plane < 0 or bit_plane > 7:
        log.warning("The provided bit plane is out of range (0-7)")
        bit_plane = min(7, abs(bit_plane))
        log.debug("The used bit plane is - {}".format(bit_plane))

    mask = 1 << bit_plane  # Mask to filter the bits not belonging to selected bit plane.
    log.info("Using the following mask - {}".format(mask))
    log.debug("Calculating the lookup table by masking the possible values")
    lookup_table = np.zeros(256)  # Initializing zeros array.
    for i in range(256):
        bit = (i & mask) >> bit_plane
        lookup_table.put(i, bit * 255)
    bit_plane_slice = useLookupTable(image, lookup_table)

    log.debug("Finished performing bit plane slicing")
    return bit_plane_slice


def useLookupTable(image, lookup_table):
    log.debug("Applying lookup table to the image")
    new_image = image.copy()
    new_image[:, :] = lookup_table[image[:, :]]
    log.debug("Finished applying lookup table to the image")
    return new_image


def histogramEqualization(image):
    log.debug("Applying histogram equalization on an image")
    hist_equalization = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    hist_equalization[:, :, 2] = cv.equalizeHist(hist_equalization[:, :, 2])
    equalized_image = cv.cvtColor(src=image, code=cv.COLOR_HSV2BGR)
    log.debug("Finished applying histogram equalization on an image")
    return equalized_image
