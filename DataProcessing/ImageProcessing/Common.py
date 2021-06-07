import cv2 as cv
import logging as log
import Logging
import numpy as np


def imageDisplay(window_name, image):
    # Display the given image with the given title.
    log.info("The exit key is set to - esc")
    while True:
        cv.imshow(winname=window_name, mat=image)

        if cv.waitKey(delay=1) & 0xFF == 27:
            log.debug("Exit key was pressed")
            break

    log.debug("Destroying all windows")
    cv.destroyAllWindows()


def extractNeighborhood(matrix, row, col, neighborhood_size):
    # Extract the neighborhood from the given matrix.
    # The center of the neighborhood is indexed by row/col.
    neighborhood = matrix[
                   row - (neighborhood_size // 2):row + (neighborhood_size // 2) + 1,
                   col - (neighborhood_size // 2):col + (neighborhood_size // 2) + 1]
    return neighborhood


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
