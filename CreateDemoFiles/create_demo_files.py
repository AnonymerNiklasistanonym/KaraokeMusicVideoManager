#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Creates music video demo video files
 - uses Pillow (pip install Pillow) to create frames with text and color
 - uses OpenCv (pip install opencv-python) to push them into one video file
 """

import random
import cv2
# pil in lowercase was necessary on Windows, if this doesn't work try in uppercase
from pil import Image, ImageDraw, ImageFont
import os


def random_color():
    """Creates an random color"""
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))


def create_image(filename, size=(1280, 720), message="Text", bg_color=random_color(), number=-1, text_color="white"):
    """Creates a image .png file with the text"""

    # create an image that we can draw on
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    # load font for the main text (message)
    font_main_text = ImageFont.truetype("FiraCode-Regular.ttf", 50)

    # get position so that the message is located in the middle of the image
    width_2, height_2 = draw.textsize(message, font=font_main_text)
    position_text = ((size[0] - width_2) / 2, (size[1] - height_2) / 2)

    # draw the text on the image
    draw.text(position_text, message, fill=text_color, font=font_main_text)

    # if wanted (number!=-1) add a sub text to the image
    if number != -1:

        # load font for the sub text
        font_sub_text = ImageFont.truetype("FiraCode-Regular.ttf", 30)

        # determine position of the sub text in the middle but slightly down
        width_2, height_2 = draw.textsize(">> Demo file #" + str(number), font=font_sub_text)
        position_text = ((size[0] - width_2) / 2, (size[1] - height_2) / 2 + 100)

        # draw the sub text on the image
        draw.text(position_text, ">> Demo file #" + str(number), fill=text_color, font=font_sub_text)

    # save draw object as a image
    draw = ImageDraw.Draw(img)
    img.save(filename)


def create_video(images, filename, framerate=1.0, seconds=1):
    """Creates a video file out of images"""

    # Determine the width and height from the first image
    frame = cv2.imread(images[0])
    height, width, channels = frame.shape

    # Define the codec and create VideoWriter object (mp4 not possible right now)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, framerate, (width, height))

    # Add all images to the video
    for image in images:
        # Added an option for longer than 1s videos
        for y in range(seconds):
            image_path = image
            frame = cv2.imread(image_path)
            out.write(frame)

    # "Release everything if job is finished" -> finish export of video
    out.release()
    cv2.destroyAllWindows()

    # Let the user know about this
    print("- Exported the video file \"{}\"".format(filename))


if __name__ == '__main__':
    """Main method: Create the demo music video files"""

    # create a directory for the files to export
    if not os.path.exists("demo_files"):
        os.makedirs("demo_files")

    # number of video files wanted
    number_of_files = 100

    # Let the user know about this
    print("Exporting {} video files:".format(number_of_files))

    # determine how many leading zeroes we need for every number
    number_of_zeroes = "%0" + str(len(str(number_of_files))) + "d"

    # create all files
    for x in range(number_of_files):

        # format the current number with the right amount of leading zeroes
        x = number_of_zeroes % (x + 1)

        # these are the images we want to create
        images = [("demo_files/start", "Hi :)", x), ("demo_files/end", "Bye!", x)]

        # create a random background color for all of the pictures
        bg_color = random_color()

        # create the images
        for image in images:
            create_image(image[0] + ".png", (1280, 720), image[1], bg_color, image[2])

        # create the video out of the created images (each image has 3s view time)
        create_video([x[0] + ".png" for x in images], "demo_files/Example Artist #" + str(x) + " - Example Title #" + str(x) + ".avi", 1.0, 3)

        # remove the created images
        for image in images:
            os.remove(image[0] + ".png")

    # create a directory for the files to export
    if not os.path.exists("demo_files_small"):
        os.makedirs("demo_files_small")

    # number of video files wanted
    number_of_files = 5

    # Let the user know about this
    print("Exporting {} video files:".format(number_of_files))

    # determine how many leading zeroes we need for every number
    number_of_zeroes = "%0" + str(len(str(number_of_files))) + "d"

    # create all files
    for x in range(number_of_files):

        # format the current number with the right amount of leading zeroes
        x = number_of_zeroes % (x + 1)

        # these are the images we want to create
        images = [("demo_files_small/start", "Hi :)", x), ("demo_files_small/end", "Bye!", x)]

        # create a random background color for all of the pictures
        bg_color = random_color()

        # create the images
        for image in images:
            create_image(image[0] + ".png", (1280, 720), image[1], bg_color, image[2])

        # create the video out of the created images (each image has 3s view time)
        create_video([x[0] + ".png" for x in images], "demo_files_small/Example Artist #" + str(x) + " - Example Title #" + str(x) + ".avi", 1.0, 3)

        # remove the created images
        for image in images:
            os.remove(image[0] + ".png")
