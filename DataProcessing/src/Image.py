import cv2 as cv
import numpy
import numpy as np
import logging as log
import Logging
import matplotlib.pyplot as plt

CHANNELS = {"R": 0, "G": 1, "B": 2}


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

    def colorModelling(self, color_model):
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

    def singleOutChannel(self, channel):
        # Display the color version of a single channel of the image.
        log.debug("Singeling out a channel")
        log.info("Selected channel is - {}".format(channel))

        single_channel = self.image.copy()
        for i in range(3):
            # Go through the RGB channels.
            if i == CHANNELS[channel]:
                continue  # Skip the desired channel.
            single_channel[:, :, i] = 0  # zero out the other channels.

        log.debug("Finished singeling out a channel")
        self.image = single_channel

    def nullifyChannel(self, channel):
        log.debug("Nullifying out a channel")
        log.info("Selected channel is - {}".format(channel))

        null_channel = self.image.copy()
        null_channel[:, :, CHANNELS[channel]] = 0  # Nullify the selected channel.

        log.debug("Finished nullifying out a channel")
        self.image = null_channel

    def showHistogram(self):
        log.debug("Displaying an image histogram")

        if self.image.ndim == 3:
            color = ('b', 'g', 'r')
        else:
            color = ('k')
        for i, col in enumerate(color):
            channel_histogram = cv.calcHist([self.image], channels=[i], mask=None,
                                            histSize=[256], ranges=[0, 256])
            plt.plot(channel_histogram, color=col)
            plt.xlim([0, 256])

        plt.title("Histogram")
        plt.show()

    def showChannelHistogram(self, channel):
        # channel - An integer indicating the channel (histogram) to display. values range - 0-2.
        log.debug("Displaying a single channel histogram")
        log.info("Selected channel is - {}".format(channel))

        channel_histogram = cv.calcHist([self.image], channels=[CHANNELS[channel]], mask=None,
                                        histSize=[256], ranges=[0, 256])

        plt.title("{} Channel Histogram".format(channel))
        plt.plot(channel_histogram, str(channel).lower())
        plt.show()
