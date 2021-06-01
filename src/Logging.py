import logging as log
import CommandLine

# TODO: Check if there is a better way to retrieve time from command line.

# date = CommandLine.runCmd("date")
# time = date.split(" ")[4]

# TODO: Need to make the log file path configurable.
log.basicConfig(
    # filename="/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Logs/ImageProcessing_" + time + ".txt",
    filename="/Users/michaelsamelsohn/PycharmProjects/Nasa_Images/Logs/Log.txt",
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s', level=log.DEBUG)
