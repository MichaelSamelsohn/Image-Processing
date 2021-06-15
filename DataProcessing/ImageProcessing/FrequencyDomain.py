import logging as log

import Logging
import cv2 as cv
import numpy as np

from IntensityTransformations import convertToGrayscale


def imageMagnitudeSpectrum(image):
    log.debug("Calculating the magnitude spectrum of the provided image")
    dft_shift = imageDFT(image=image)  # Calculate the DFT
    magnitude_spectrum = 20 * np.log(cv.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

    log.debug("Finished calculating the magnitude spectrum of the provided image")
    return magnitude_spectrum


def imageDFT(image):
    log.debug("Computing the DFT (Discrete Fourier Transform) of the provided image")

    grayscale_image = convertToGrayscale(image=image)

    dft = cv.dft(np.float32(grayscale_image), flags=cv.DFT_COMPLEX_OUTPUT)  # Calculate the DFT.
    dft_shift = np.fft.fftshift(dft)
    # Zero frequency component (DC component) will be at top left corner. In order to bring it to center,
    # it the result needs to be shifted by N/2 in both directions.

    log.debug("Finished computing the DFT of the provided image")
    return dft_shift


def imageIDFT(frequency_filtered_image):
    log.debug("Computing the IDFT (Inverse Discrete Fourier Transform) of the provided image")

    f_ishift = np.fft.ifftshift(frequency_filtered_image)
    result_image = cv.idft(f_ishift)
    result_image = cv.magnitude(result_image[:, :, 0], result_image[:, :, 1])

    result_image = cv.normalize(result_image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
    log.debug("Finished computing the IDFT of the provided image")
    return result_image


def frequencyFilter(image, frequency_filter):
    log.debug("Filtering provided image in the frequency domain")

    dft_image = imageDFT(image=image)  # Calculate the DFT.

    frequency_filtered_image = dft_image * frequency_filter  # Apply filter.

    return_image = imageIDFT(frequency_filtered_image=frequency_filtered_image)  # # Calculate the IDFT.

    log.debug("Finished filtering provided image in the frequency domain")
    return return_image
