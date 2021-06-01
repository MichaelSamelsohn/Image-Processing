import functools

import cv2 as cv
import numpy
import numpy as np
import logging as log

from scipy.signal import convolve2d

import Logging
import matplotlib.pyplot as plt


def BookImplementation(book, reference):
    def decorator_BookImplementation(func):
        @functools.wraps(func)
        def wrapper_BookImplementation(*args, **kwargs):
            log.info("The following method is referenced from the book - {}".format(book))
            log.info("Reference for the implementation - {}".format(reference))
            return func(*args, **kwargs)

        return wrapper_BookImplementation

    return decorator_BookImplementation


class Image:
    def __init__(self, filename):
        log.debug("Creating an object of type Image")
        log.debug("The selected filename is - {}".format(filename))
        self.original_image = cv.imread(filename=filename)
        if type(self.original_image) is not numpy.ndarray:
            log.error("Unable to read the provided filename. Either there is not such file or it is not an image")
            exit(1)
        self.image = self.original_image.copy()  # Creating a copy of the original image.
        log.debug("Finished creating the object")

    def resetToOriginal(self):
        log.debug("Resetting the processed image back to the original one")
        self.image = self.original_image.copy()
        log.debug("Image reset")

    def showOriginalImage(self, window_name):
        log.debug("Displaying the original image")
        log.info("The exit key is set to - esc")
        while True:
            cv.imshow(winname=window_name, mat=self.original_image)

            if cv.waitKey(delay=1) & 0xFF == 27:
                break

        log.debug("Destroying all windows")
        cv.destroyAllWindows()

    def showImage(self, window_name):
        log.debug("Displaying the current image")
        log.info("The exit key is set to - esc")
        while True:
            cv.imshow(winname=window_name, mat=self.image)

            if cv.waitKey(delay=1) & 0xFF == 27:
                break

        log.debug("Destroying all windows")
        cv.destroyAllWindows()

    def convertToGrayscale(self):
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

    def colorMapping(self, color_model):
        self.image = cv.cvtColor(src=self.image, code=color_model)

    def resizeImage(self, dsize):
        # dsize is the shape parameter (tuple) for the height and width of the reshaped image.
        # Note that dsize is in reverse order to the height and width
        # (first parameter is the width and the second one is height).

        log.debug("Resizing (by specific shape) image using OpenCV resize method")
        log.info("The new width and height are: w-{}, h-{}, respectively".format(dsize[0], dsize[1]))

        self.image = cv.resize(self.image, dsize=dsize)

        log.debug("Finished resizing (by specific shape) image using OpenCV resize method")

    def resizeImageByRatio(self, ratio):
        # ratio is the shape ratio parameter (tuple) for the height and width of the reshaped image.
        # Note that ratio is in reverse order to the height and width
        # (first parameter is the width and the second one is height).

        log.debug("Resizing (by ratio) image using OpenCV resize method")
        log.info("The new ratio for width and height is: w-{}, h-{}, respectively".format(ratio[0], ratio[1]))

        width, height = ratio
        self.image = cv.resize(self.image, (0, 0), self.image, width, height)

        log.debug("Finished resizing (by ratio) image using OpenCV resize method")

    def imageFlipping(self, flip_code):
        # The different flip codes are:
        # 0 - Flip along the horizontal axis.
        # 1 - Flip along the vertical axis.
        # -1 - Flip along both axes.

        log.debug("Flipping image using OpenCV flip method")
        log.info("Selected flip code is - {}".format(flip_code))

        self.image = cv.flip(self.image, flipCode=flip_code)

        log.debug("Finished flipping image using OpenCV flip method")

    def drawRectangle(self, pt1, pt2, color, thickness):
        # pt1 (tuple) - Top left corner of the rectangle.
        # pt2 (tuple) - Bottom right corner of the rectangle.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        log.debug("Drawing a rectangle on the image using OpenCV rectangle method")
        log.info("Top left corner of the rectangle is - ({},{})".format(pt1[0], pt1[1]))
        log.info("Bottom right corner of the rectangle is - ({},{})".format(pt2[0], pt2[1]))
        log.info("Selected color is - ({},{},{})".format(color[0], color[1], color[2]))
        log.info("Selected thickness is - {}".format(thickness))

        self.image = cv.rectangle(img=self.image,
                                  pt1=pt1, pt2=pt2,
                                  color=color, thickness=thickness)

        log.debug("Finished drawing a rectangle on the image using OpenCV rectangle method")

    def drawCircle(self, center, radius, color, thickness):
        # center (tuple) - Center of the circle.
        # radius - Radius of the circle.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        log.debug("Drawing a circle on the image using OpenCV circle method")
        log.info("Center of the circle is - ({},{})".format(center[0], center[1]))
        log.info("Radius of the circle is - {}".format(radius))
        log.info("Selected color is - ({},{},{})".format(color[0], color[1], color[2]))
        log.info("Selected thickness is - {}".format(thickness))

        self.image = cv.circle(img=self.image,
                               center=center, radius=radius,
                               color=color,
                               thickness=thickness)

        log.debug("Finished drawing a circle on the image using OpenCV circle method")

    def drawLine(self, pt1, pt2, color, thickness):
        # pt1 (tuple) - First corner of the line.
        # pt2 (tuple) - Second corner of the line.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        log.debug("Drawing a line on the image using OpenCV line method")
        log.info("First corner of the line is - ({},{})".format(pt1[0], pt1[1]))
        log.info("Second corner of the line is - ({},{})".format(pt2[0], pt2[1]))
        log.info("Selected color is - ({},{},{})".format(color[0], color[1], color[2]))
        log.info("Selected thickness is - {}".format(thickness))

        self.image = cv.line(img=self.image,
                             pt1=pt1, pt2=pt2,
                             color=color,
                             thickness=thickness)

        log.debug("Finished drawing a line on the image using OpenCV line method")

    def drawText(self, text, org, fontFace, fontScale, color, thickness):
        # text - The text to be printed on the image.
        # org - Bottom left corner of the text string in the image.
        # fontFace - The font of the text. E.g. cv.FONT_HERSHEY_SIMPLEX.
        # fontScale - Size of the font.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        log.debug("Printing text on the image using OpenCV putText method")
        log.info("The selected text is - {}}".format(text))
        log.info("Bottom left corner of the text string in the image is - ({},{})".format(org[0], org[1]))
        log.info("Selected fontface is - {}".format(fontFace))
        log.info("Selected fontScale is - {}".format(fontScale))
        log.info("Selected color is - ({},{},{})".format(color[0], color[1], color[2]))
        log.info("Selected thickness is - {}".format(thickness))

        self.image = cv.putText(img=self.image,
                                text=text, org=org,
                                fontFace=fontFace, fontScale=fontScale,
                                color=color, thickness=thickness, lineType=cv.LINE_AA)

        log.debug("Finished printing text on the image using OpenCV putText method")

    def drawCircleOnMouseCallback(self, window_title, exit_key, radius, color, thickness):
        # radius - Radius of the circle.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        # Drawing function.
        def draw_circle(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN:
                # Circle will have user selected color.
                cv.circle(self.image, (x, y), radius, color, thickness)
            elif event == cv.EVENT_RBUTTONDOWN:
                # Circle will have alternative color.
                cv.circle(self.image, (x, y), radius, np.flip(color), thickness)

        # Connecting the image display with the drawing function.
        cv.namedWindow(winname=window_title)
        cv.setMouseCallback(window_title, draw_circle)

        # Showing image with OpenCV.
        while True:
            cv.imshow(winname=window_title, mat=self.image)

            if cv.waitKey(100) & 0xFF == exit_key:
                break

        log.debug("Destroying all windows")
        cv.destroyAllWindows()

    def drawRectangleOnMouseCallback(self, window_title, exit_key, color, thickness):
        # Global variables for rectangle drawing using mouse callbacks.
        drawing = False
        ix, iy = -1, -1

        # Note: it is important to draw the rectangle from top -> bottom, left -> right.
        # color - list of three colors (R,G,B).
        # thickness - thickness of the circumference of the rectangle. -1 will fill the rectangle.

        # Drawing function.
        def draw_rectangle(event, x, y, flags, param):
            global ix, iy, drawing

            if event == cv.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y
            elif event == cv.EVENT_MOUSEMOVE:
                if drawing:
                    cv.rectangle(self.image, (ix, iy), (x, y), color, thickness)
            elif event == cv.EVENT_LBUTTONUP:
                drawing = False
                cv.rectangle(self.image, (ix, iy), (x, y), color, thickness)

        # Connecting the image display with the drawing function.
        cv.namedWindow(winname=window_title)
        cv.setMouseCallback(window_title, draw_rectangle)

        # Showing image with OpenCV.
        while True:
            cv.imshow(winname=window_title, mat=self.image)

            if cv.waitKey(100) & 0xFF == exit_key:
                break

        log.debug("Destroying all windows")
        cv.destroyAllWindows()

    def threshold(self, threshold, max_val, type_code):
        # threshold - The threshold value.
        # max_val - The value pixels above the threshold turn into.
        # type_code - The type of the thresholding. E.g. cv.THRESH_BINARY.

        log.debug("Applying an image threshold")
        log.info("Selected threshold value is - {}".format(threshold))
        log.info("Selected max value is - {}".format(max_val))
        log.info("Selected type code is - {}".format(type_code))

        thresh, threshold_image = cv.threshold(src=self.image,
                                               thresh=threshold,
                                               maxval=max_val,
                                               type=type_code)

        log.debug("Finished applying an image threshold")
        return thresh

    def adaptiveThreshold(self, max_val, adaptive_method, threshold_type, block_size, c):
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

        self.image = cv.adaptiveThreshold(src=self.image,
                                          maxValue=max_val,
                                          adaptiveMethod=adaptive_method,
                                          thresholdType=threshold_type,
                                          blockSize=block_size, C=c)

        log.debug("Applying an image adaptive threshold")

    @BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                        reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.122-123")
    def negative(self):
        # Perform image negative. Simply subtract every value of the matrix from 255.
        log.debug("Performing image negative")
        self.image = 255 - self.image
        log.debug("Finished performing image negative")

    def gammaCorrection(self, image_array, gamma):
        log.debug("Performing Gamma correction to an image")
        log.info("Selected Gamma value is - {}".format(gamma))

        gamma_correction = image_array / 255.0
        gamma_correction = np.power(gamma_correction, gamma)

        log.debug("Finished performing Gamma correction to an image")
        self.image = gamma_correction

    @BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                        reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.131-133")
    def bitPlaneReconstruction(self, degree_of_reduction):
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
        self.image = self.image // reduction_factor * reduction_factor
        log.debug("Finished performing image color reduction")

    @BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                        reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.131-133")
    def bitPlaneSlicing(self, bit_plane):
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
        self.image = useLookupTable(self.image, lookup_table)
        log.debug("Finished performing bit plane slicing")

    def boxFilter(self, kernel_size, border_type):
        log.debug("Applying a box filter to an image")
        log.info("Selected kernel size is - {}".format(kernel_size))
        log.info("Selected border type is - {}".format(border_type))

        self.image = cv.blur(self.image, (kernel_size, kernel_size), borderType=border_type)

        log.debug("Finished applying a box filter to an image")

    def gaussianFilter(self, kernel_size, sigma, border_type):
        log.debug("Applying a Gaussian filter to an image")
        log.info("Selected kernel size is - {}".format(kernel_size))
        log.info("Selected Sigma value is - {}".format(sigma))
        log.info("Selected border type is - {}".format(border_type))

        self.image = cv.GaussianBlur(self.image, (kernel_size, kernel_size), sigma, borderType=border_type)

        log.debug("Finished applying a Gaussian filter to an image")

    def medianFilter(self, kernel_size):
        log.debug("Applying a median filter to an image")
        log.info("Selected kernel size is - {}".format(kernel_size))

        self.image = cv.medianBlur(self.image, kernel_size)

        log.debug("Finished applying a median filter to an image")

    def bilateralFilter(self, kernel_size, sigma_color, sigma_space, border_type):
        log.debug("Applying a bilateral filter to an image")
        log.info("Selected kernel size is - {}".format(kernel_size))
        log.info("Selected Sigma color is - {}".format(sigma_color))
        log.info("Selected Sigma space is - {}".format(sigma_space))
        log.info("Selected border type is - {}".format(border_type))

        self.image = cv.bilateralFilter(self.image, kernel_size,
                                        sigmaColor=sigma_color, sigmaSpace=sigma_space,
                                        borderType=border_type)

        log.debug("Finished applying a bilateral filter to an image")

    def erosion(self, kernel, iterations):
        log.debug("Performing erosion on an image")
        log.info("Selected number of iterations is  - {}".format(iterations))

        self.image = cv.erode(self.image, kernel=kernel, iterations=iterations)

        log.debug("Performing erosion on an image")

    def dilation(self, kernel, iterations):
        log.debug("Performing dilation on an image")
        log.info("Selected number of iterations is  - {}".format(iterations))

        self.image = cv.dilate(self.image, kernel=kernel, iterations=iterations)

        log.debug("Performing dilation on an image")

    def opening(self, kernel):
        log.debug("Performing opening on an image")

        self.image = cv.morphologyEx(self.image, cv.MORPH_OPEN, kernel=kernel)

        log.debug("Performing opening on an image")

    def closing(self, kernel):
        log.debug("Performing closing on an image")

        self.image = cv.morphologyEx(self.image, cv.MORPH_CLOSE, kernel=kernel)

        log.debug("Performing closing on an image")

    def morphGradient(self, kernel):
        log.debug("Performing morphological gradient on an image")

        self.image = cv.morphologyEx(self.image, cv.MORPH_GRADIENT, kernel=kernel)

        log.debug("Performing morphological gradient on an image")

    def sobelGradient(self, ddepth, kernel_size, direction):
        log.debug("Applying a Sobel gradient on an image")
        log.info("Selected ddpeth is - {}".format(ddepth))
        log.info("Selected kernel_size is - {}".format(kernel_size))
        log.info("Selected direction is - {}".format(direction))

        if direction == "X":
            self.image = cv.Sobel(self.image, ddepth, 1, 0, kernel_size)
        elif direction == "Y":
            self.image = cv.Sobel(self.image, ddepth, 0, 1, kernel_size)
        else:
            self.image = cv.Sobel(self.image, ddepth, 1, 1, kernel_size)

        log.debug("Finished applying a Sobel gradient on an image")

    def laplacianGradient(self, ddepth):
        log.debug("Applying a Laplacian gradient on an image")
        log.info("Selected ddpeth is - {}".format(ddepth))

        self.image = cv.Laplacian(self.image, ddepth)

        log.debug("Finished applying a Laplacian gradient on an image")

    @BookImplementation(book="Digital Image Processing (4th edition) - Gonzales & Woods",
                        reference="Chapter 3 - Some Basic Intensity Transformation Functions, p.175-182")
    def laplacianFilter(self, padding_type, diagonal_terms, contrast_stretch, override):
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
            self.image = convolve2d(in1=self.image,
                                    in2=laplacian_kernel_with_diagonal,
                                    mode="same",
                                    boundary=padding_type)
        else:
            self.image = convolve2d(in1=self.image,
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
            return

        # Deal with negative/saturated values. Either stretch the value range or cutoff saturated values.
        log.info("Contrast stretch will be performed upon filtering completion - {}".format(contrast_stretch))
        if contrast_stretch is True:
            self.image = cv.normalize(self.image, None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
        else:
            self.image = cv.convertScaleAbs(self.image)

    def showChannelHistogram(self, channel):
        # channel - An integer indicating the channel (histogram) to display. values range - 0-2.
        log.debug("Displaying a single channel histogram")
        log.info("Selected channel is - {}".format(channel))

        channel_histogram = cv.calcHist([self.image], channels=[channel], mask=None,
                                        histSize=[256], ranges=[0, 256])

        # TODO: Display the color of the histogram as the color of the selected channel.
        plt.plot(channel_histogram)
        plt.show()

    def showHistogram(self):
        log.debug("Displaying an image histogram")

        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            channel_histogram = cv.calcHist([self.image], channels=[i], mask=None,
                                            histSize=[256], ranges=[0, 256])
            plt.plot(channel_histogram, color=col)
            plt.xlim([0, 256])

        plt.title("Histogram")
        plt.show()

    def bitwiseAndMasking(self, x1, y1, x2, y2):
        log.debug("Masking an image")
        log.info("Mask values: [{}:{},{}:{}]".format(x1, x2, y1, y2))

        # Creating the mask.
        mask = np.zeros(self.image.shape[:2], np.uint8)
        mask[x1:x2, y1:y2] = 255

        # Masking the image.
        masked_image = cv.bitwise_and(self.image, self.image, mask=mask)

        log.debug("Finished masking an image")
        return masked_image

    def histogramEqualization(self):
        log.debug("Applying histogram equalization on an image")

        hist_equalization = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        hist_equalization[:, :, 2] = cv.equalizeHist(hist_equalization[:, :, 2])
        self.image = cv.cvtColor(src=self.image, code=cv.COLOR_HSV2BGR)

        log.debug("Finished applying histogram equalization on an image")


def useLookupTable(channel_array, lookup_table):
    log.debug("Applying lookup table to the image")
    new_image = channel_array.copy()
    new_image[:, :] = lookup_table[channel_array[:, :]]
    log.debug("Finished applying lookup table to the image")
    return new_image
