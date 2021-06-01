import logging as log
import Logging
import cv2 as cv
import numpy as np
from scipy.signal import convolve2d


def useLookupTable(channel_array, lookup_table):
    log.debug("Applying lookup table to the image")
    new_image = channel_array.copy()
    new_image[:, :] = lookup_table[channel_array[:, :]]
    log.debug("Finished applying lookup table to the image")
    return new_image


def contrastStretch(channel_array):
    # Stretches the array values to fit the 0-255 bounds.
    log.debug("Performing contrast stretch")

    # Calculating the min/max pixel values in given array.
    min_value = np.min(channel_array)
    log.info("Calculated min value is - {}".format(min_value))
    max_value = np.max(channel_array)
    log.info("Calculated max value is - {}".format(max_value))

    # Calculating new line coefficients.
    m = 255.0 / (max_value - min_value)
    c = 255.0 - m * max_value
    log.info("Calculated coefficients: m={}, c={}".format(m, c))

    # Stretching the array values using the new coefficients.
    stretched_array = channel_array.copy()
    stretched_array[:, :] = m * channel_array[:, :] + c
    log.debug("Finished performing contrast stretch")
    return stretched_array


def fixSaturatedValues(channel_array):
    # Function for dealing with saturated values.
    log.debug("Fixing saturated values")
    fixed_array = channel_array.copy()
    fixed_array[fixed_array < 0] = 0
    fixed_array[fixed_array > 255] = 255
    log.debug("Finished fixing saturated values")
    return fixed_array


