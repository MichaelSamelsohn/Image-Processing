import logging as log

from scipy.signal import convolve2d

import Logging
import cv2 as cv
import numpy as np

from Common import extractNeighborhood
from DataProcessing.ImageProcessing.Decorators import BookImplementation
from SpatialFiltering import gaussianFilter


def threshold(image, threshold_val, max_val, type_code):
    # threshold_val - The threshold value.
    # max_val - The value pixels above the threshold turn into.
    # type_code - The type of the thresholding. E.g. cv.THRESH_BINARY.

    log.debug("Applying an image threshold")
    log.info("Selected threshold value is - {}".format(threshold_val))
    log.info("Selected max value is - {}".format(max_val))
    log.info("Selected type code is - {}".format(type_code))

    thresh, threshold_image = cv.threshold(src=image,
                                           thresh=threshold_val,
                                           maxval=max_val,
                                           type=type_code)

    log.debug("Finished applying an image threshold")
    return threshold_image


def adaptiveThreshold(image, max_val, adaptive_method, threshold_type, block_size, c):
    # max_val - The value pixels above the threshold turn into.
    # adaptive_method - Which method is used for the thresholding. E.g. cv.ADAPTIVE_THRESH_MEAN.
    # threshold_type - The type of the thresholding. E.g. cv.THRESH_BINARY.
    # block_size - Neighborhood for the adaptive_method. Has to be an odd integer.
    # c - A constant subtracted from the mean.

    log.debug("Applying an image adaptive threshold")
    log.info("Selected max value is - {}".format(max_val))
    log.info("Selected adaptive method is - {}".format(adaptive_method))
    log.info("Selected threshold type is - {}".format(threshold_type))
    log.info("Selected block size is - {}".format(block_size))
    log.info("Selected c value is - {}".format(c))

    adaptive_threshold_image = cv.adaptiveThreshold(src=image,
                                                    maxValue=max_val,
                                                    adaptiveMethod=adaptive_method,
                                                    thresholdType=threshold_type,
                                                    blockSize=block_size, C=c)

    log.debug("Applying an image adaptive threshold")
    return adaptive_threshold_image


def sobelGradient(image, ddepth, kernel_size, direction):
    log.debug("Applying a Sobel gradient on an image")
    log.info("Selected ddpeth is - {}".format(ddepth))
    log.info("Selected kernel_size is - {}".format(kernel_size))
    log.info("Selected direction is - {}".format(direction))

    if direction == "X":
        sobel_image = cv.Sobel(image, ddepth, 1, 0, kernel_size)
    elif direction == "Y":
        sobel_image = cv.Sobel(image, ddepth, 0, 1, kernel_size)
    else:
        sobel_image = cv.Sobel(image, ddepth, 1, 1, kernel_size)

    log.debug("Finished applying a Sobel gradient on an image")
    return sobel_image


def laplacianGradient(image, ddepth):
    log.debug("Applying a Laplacian gradient on an image")
    log.info("Selected ddpeth is - {}".format(ddepth))

    laplacian_gradient = cv.Laplacian(image, ddepth)

    log.debug("Finished applying a Laplacian gradient on an image")
    return laplacian_gradient


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.175-182")
def laplacianGradientExtended(image, padding_type, diagonal_terms, contrast_stretch, override):
    log.debug("Applying Laplacian filter to channel array")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Kernel will include diagonal terms - {}".format(diagonal_terms))

    # Step 0 - Prepare the kernels for filtering.
    log.debug("Preparing Laplacian kernels (with/without) diagonal terms")
    # Generating a Lapalcian kernel (without diagonal terms).
    laplacian_kernel_without_diagonal = np.array([[0, 1, 0],
                                                  [1, -4, 1],
                                                  [0, 1, 0]])
    # Generating a Lapalcian kernel (with diagonal terms).
    laplacian_kernel_with_diagonal = np.array([[1, 1, 1],
                                               [1, -8, 1],
                                               [1, 1, 1]])

    # Step I - Apply the filters with or without diagonal terms.
    if diagonal_terms is True:
        filtered_image = convolve2d(in1=image,
                                    in2=laplacian_kernel_with_diagonal,
                                    mode="same",
                                    boundary=padding_type)
    else:
        filtered_image = convolve2d(in1=image,
                                    in2=laplacian_kernel_without_diagonal,
                                    mode="same",
                                    boundary=padding_type)

    log.info(
        "Override selected for treating with post filter array negative/saturated values - {}".format(override))
    # overrride = True, meant to leave the post filter matrix as is.
    # Should be True only for Marr-Hildreth filter, otherwise False.
    if override is True:
        log.warning(
            "Overriding post filter array negative values handling (array may contain negative/saturated values)."
            " Should only be done for Marr-Hildreth/Sobel-Prewitt filter")
        return filtered_image

    # Deal with negative/saturated values. Either stretch the value range or cutoff saturated values.
    log.info("Contrast stretch will be performed upon filtering completion - {}".format(contrast_stretch))
    if contrast_stretch is True:
        return_image = cv.normalize(filtered_image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
    else:
        return_image = cv.convertScaleAbs(filtered_image)

    return return_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 10.2 - Point, Line, and Edge Detection, p.706-707")
def isolatedPointDetection(image, padding_type, threshold_value):
    log.debug("Performing isolated point detection")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Selected threshold is - {}".format(threshold_value))

    # Step I - Filter the image with the second derivative (Laplacian kernel).
    filtered_image = laplacianGradientExtended(image=image,
                                               padding_type=padding_type,
                                               diagonal_terms=True,
                                               contrast_stretch=False,
                                               override=True)

    # Step II - Threshold the absolute value of the pixels.
    log.debug("Thresholding the absolute values of the pixels")
    thresholded_image = (np.abs(filtered_image) > threshold) * 255
    return_image = cv.convertScaleAbs(thresholded_image)

    log.debug("Finished performing isolated point detection")
    return return_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 10.2 - Point, Line, and Edge Detection, p.707-710")
def lineDetection(image, padding_type, direction, threshold_value):
    log.debug("Performing line detection")
    log.info("Selected padding type is - {}".format(padding_type))
    log.info("Selected direction is - {}".format(direction))
    log.info("Selected threshold is - {}".format(threshold_value))

    # Step 0 - Prepare the directional kernels.
    log.debug("Preparing directional kernels")
    horizontal_kernel = np.array([[-1, -1, -1],
                                  [2, 2, 2],
                                  [-1, -1, -1]])
    plus_45_kernel = np.array([[2, -1, -1],
                               [-1, 2, -1],
                               [-1, -1, 2]])
    vertical_kernel = np.array([[-1, 2, -1],
                                [-1, 2, -1],
                                [-1, 2, -1]])
    minus_45_kernel = np.array([[-1, -1, 2],
                                [-1, 2, -1],
                                [2, -1, -1]])
    options = {"horizontal": horizontal_kernel,
               "plus45": plus_45_kernel,
               "vertical": vertical_kernel,
               "minus45": minus_45_kernel
               }

    # StepI - Filter the image with the specified kernel.
    filtered_image = convolve2d(in1=image,
                                in2=options[direction],
                                mode="same",
                                boundary=padding_type)

    # Step II - Threshold the absolute value of the pixels.
    log.debug("Thresholding the absolute values of the pixels")
    thresholded_image = (np.abs(filtered_image) > threshold) * 255
    return_image = cv.convertScaleAbs(thresholded_image)

    log.debug("Finished performing line detection")
    return return_image


@BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                    reference="Chapter 10.2 - Point, Line, and Edge Detection, p.720-722")
def edgeDetectionKirsch(image, padding_type, direction, contrast_stretch):
    log.debug("Performing edge detection using Kirsch model")
    log.info("Selected padding type is - {}".format(padding_type))

    # Step 0 - Prepare the directional kernels.
    log.debug("Preparing directional kernels")
    kernel_n = np.array([[-3, -3, 5],
                         [-3, 0, 5],
                         [-3, -3, 5]])
    kernel_nw = np.array([[-3, 5, 5],
                          [-3, 0, 5],
                          [-3, -3, -3]])
    kernel_w = np.array([[5, 5, 5],
                         [-3, 0, -3],
                         [-3, -3, -3]])
    kernel_sw = np.array([[5, 5, -3],
                          [5, 0, -3],
                          [-3, -3, -3]])
    kernel_s = np.array([[5, -3, -3],
                         [5, 0, -3],
                         [5, -3, -3]])
    kernel_se = np.array([[-3, -3, -3],
                          [5, 0, -3],
                          [5, 5, -3]])
    kernel_e = np.array([[-3, -3, -3],
                         [-3, 0, -3],
                         [5, 5, 5]])
    kernel_ne = np.array([[-3, -3, -3],
                          [-3, 0, 5],
                          [-3, 5, 5]])
    kernels = {"N": kernel_n,
               "NW": kernel_nw,
               "W": kernel_w,
               "SW": kernel_sw,
               "S": kernel_s,
               "SE": kernel_se,
               "E": kernel_e,
               "NE": kernel_ne}

    post_filter_arrays = {"N": None,
                          "NW": None,
                          "W": None,
                          "SW": None,
                          "S": None,
                          "SE": None,
                          "E": None,
                          "NE": None}

    # Step I - Scale the channel array to be with values 0-1.
    scaled_image = cv.normalize(image, None, 1, 0, cv.NORM_MINMAX, cv.CV_32F)

    # Step II - Apply the filter with every directional kernel.
    for kernel in kernels:
        post_filter_arrays[kernel] = convolve2d(in1=scaled_image,
                                                in2=kernels[kernel],
                                                mode="same",
                                                boundary=padding_type)

    # Step III - Amass a max values array (to be used later for comparison with specific post kernel result).
    width, height = image.shape
    max_value_matrix = np.zeros((width, height))
    for array in post_filter_arrays:
        max_value_matrix = (post_filter_arrays[array] > max_value_matrix) * post_filter_arrays[array]

    # Step IV - Compare post filter array (in selected direction) with max values array.
    log.info("Selected direction is - {}".format(direction))
    non_scaled_image = (post_filter_arrays[direction] <= max_value_matrix) * post_filter_arrays[direction]
    # return_array = scaleMatrix(matrix=return_array, scaling_factor=(1.0 / 255.0))

    # Deal with negative/saturated values. Either stretch the value range or cutoff saturated values.
    log.info("Contrast stretch will be performed upon filtering completion - {}".format(contrast_stretch))
    if contrast_stretch is True:
        return_image = cv.normalize(non_scaled_image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
    else:
        return_image = cv.convertScaleAbs(non_scaled_image)

    log.debug("Finished performing edge detection using Kirsch model")
    return return_image


def edgeDetectionMarrHildreth(image, padding_type1, padding_type2, padding_type3,
                              kernel_size, sigma, threshold_value):
    log.debug("Performing edge detection using Marr-Hildreth model (LoG)")
    log.info("Chosen kernel size is - {}".format(kernel_size))
    log.info("Selected deviation (to be used in the Gaussian filter) is - {}".format(sigma))

    # Step I - Smooth the image with a Gaussian low-pass kernel.
    post_gaussian_filter = gaussianFilter(image=image, border_type=padding_type1,
                                          kernel_size=kernel_size, sigma=sigma)

    # Step II - Compute the Laplacian of the image resulting from step I.
    post_laplacian_filter = laplacianGradientExtended(image=post_gaussian_filter, padding_type=padding_type2,
                                                      diagonal_terms=True, contrast_stretch=False,
                                                      override=True)

    post_filter_array = cv.copyMakeBorder(post_laplacian_filter, 1, 1, 1, 1, padding_type3)

    # Step III - Find the zero-crossing of the image from step II.
    log.debug("Performing zero crossing for the post Gaussian-Laplacian filters")
    log.info("Selected threshold is - {}".format(threshold_value))
    width, height = image.shape
    return_array = np.zeros((width, height))
    for row in range(width):
        for col in range(height):
            neighborhood = extractNeighborhood(matrix=post_filter_array,
                                               row=row + 1, col=col + 1,
                                               neighborhood_size=3)
            return_array[row][col] = zeroCrossing(neighborhood=neighborhood, threshold_value=threshold_value)

    return_array = cv.convertScaleAbs(return_array)
    log.debug("Finished performing edge detection using Marr-Hildreth model")
    return return_array


def zeroCrossing(neighborhood, threshold_value):
    # Check if a zero crossing occurs in the 3x3 neighborhood (dictated by the threshold).
    zero_crossing = 0
    if (neighborhood[0, 0] * neighborhood[2, 2] < 0) \
            & (np.abs(neighborhood[0, 0] - neighborhood[2, 2]) > threshold_value):
        zero_crossing = 255
    if (neighborhood[2, 0] * neighborhood[0, 2] < 0) \
            & (np.abs(neighborhood[2, 0] - neighborhood[0, 2]) > threshold_value):
        zero_crossing = 255
    if (neighborhood[1, 0] * neighborhood[1, 2] < 0) \
            & (np.abs(neighborhood[1][0] - neighborhood[1][2]) > threshold_value):
        zero_crossing = 255
    if (neighborhood[0, 1] * neighborhood[2, 1] < 0) \
            & (np.abs(neighborhood[0, 1] - neighborhood[2, 1]) > threshold_value):
        zero_crossing = 255
    return zero_crossing
