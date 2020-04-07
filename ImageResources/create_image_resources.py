#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
With executing this script you convert the current logo (logo.svg) to all
the needed png and ico files.
To convert the svg file you need to have inkscape installed on your system.
'''

import os
import subprocess
from shutil import copyfile

from PIL import Image, ImageEnhance

# current directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

COMMAND_INKSCAPE = 'inkscape'


def convert_svg_2_png(input_filename, output_filename, width=None, height=None):
    """Convert a svg file to a png file."""

    if not os.path.isabs(input_filename):
        source_file = os.path.abspath(input_filename)
    else:
        source_file = input_filename
    if not os.path.isabs(output_filename):
        output_file = os.path.abspath(output_filename)
    else:
        output_file = output_filename

    # change directory to the inkscape directory
    # os.chdir(DIR_INKSCAPE)

    if width is None and height is None:
        pro = subprocess.Popen([
            COMMAND_INKSCAPE,
            "-o", output_file,
            source_file
        ], stdout=subprocess.PIPE)
    elif height is None:
        pro = subprocess.Popen([
            COMMAND_INKSCAPE,
            f"--export-width={width}",
            "-o", output_file,
            source_file
        ], stdout=subprocess.PIPE)
    elif width is None:
        pro = subprocess.Popen([
            COMMAND_INKSCAPE,
            f"--export-height={height}",
            "-o", output_file,
            source_file
        ], stdout=subprocess.PIPE)
    else:
        pro = subprocess.Popen([
            COMMAND_INKSCAPE,
            f"--export-width={width}", f"--export-height={height}",
            "-o", output_file,
            source_file
        ], stdout=subprocess.PIPE)
    while pro.poll() is None:
        print('', end='')
        # wait till the process is ready

    print(pro.communicate()[0].decode("utf-8"))

    print(f"- '{source_file}' was converted to '{output_file}'")

    # os.chdir(DIR_PATH)


def create_png_favicons(favicon_directory_path, source_file):
    """Creates all the html favicons."""

    # create the directory if there is no such directory
    if not os.path.exists(favicon_directory_path):
        os.makedirs(favicon_directory_path)

    # all the sizes we want:
    favicon_sizes = [16, 32, 48, 64, 94, 128, 160, 180, 194, 256, 512]

    for favicon_size in favicon_sizes:
        output_path = os.path.join(
            favicon_directory_path,
            f"favicon-{favicon_size}x{favicon_size}.png"
        )
        convert_svg_2_png(source_file, output_path, favicon_size, favicon_size)


def create_installer_icons(icon_directory_path, source_file):
    """Creates all the ico icons."""

    # create the directory if there is no such directory
    if not os.path.exists(icon_directory_path):
        os.makedirs(icon_directory_path)

    output_name = "icon"
    output_path_png = os.path.join(icon_directory_path, f"{output_name}.png")
    output_path_ico = os.path.join(
        icon_directory_path, f"{output_name}_install.ico")
    output_path_ico_2 = os.path.join(
        icon_directory_path, f"{output_name}_uninstall.ico")
    output_path_ico_3 = os.path.join(
        icon_directory_path, f"{output_name}.ico")

    convert_svg_2_png(source_file, output_path_png, 255, 255)

    img = Image.open(output_path_png)
    img.save(output_path_ico)

    print(f"- '{output_path_png}' was converted to '{output_path_ico}")

    img.save(output_path_ico_3)

    print(f"- '{output_path_png}' was converted to '{output_path_ico_3}")

    make_grey(img).save(output_path_ico_2)

    print(f"- '{output_path_png}' was converted to '{output_path_ico_2}")

    if os.path.exists(output_path_png):
        os.remove(output_path_png)


def create_installer_pages(pages_directory_path, source_file):
    """Creates all the ico icons."""

    # create the directory if there is no such directory
    if not os.path.exists(pages_directory_path):
        os.makedirs(pages_directory_path)

    output_name = "picture_left_"
    output_path_inst_png = os.path.abspath(os.path.join(
        pages_directory_path, f"{output_name}installer.png"))
    output_path_inst = os.path.abspath(os.path.join(
        pages_directory_path, f"{output_name}installer.bmp"))
    output_path_uninst = os.path.abspath(os.path.join(
        pages_directory_path, f"{output_name}uninstaller.bmp"))

    convert_svg_2_png(source_file, output_path_inst_png, 164, 314)

    img = Image.open(output_path_inst_png)
    img.save(output_path_inst)

    print(f"- '{output_path_inst_png}' was converted to '{output_path_inst}'")

    make_grey(img).save(output_path_uninst)

    print(f"- '{output_path_inst_png}' was converted to '{output_path_uninst}'")

    os.remove(output_path_inst_png)


def create_program_icon(icon_directory_path, source_file):
    """Creates all the ico icons."""

    if os.path.exists(source_file):
        # create the directory if there is no such directory
        if not os.path.exists(icon_directory_path):
            os.makedirs(icon_directory_path)

        output_name = "icon"
        output_path_png = os.path.abspath(os.path.join(
            icon_directory_path, output_name + ".png"))
        output_path_ico = os.path.abspath(os.path.join(
            icon_directory_path, output_name + ".ico"))

        convert_svg_2_png(source_file, output_path_png, 255, 255)

        img = Image.open(output_path_png)
        img.save(output_path_ico)

        print(f"- '{output_path_png}' was converted to '{output_path_ico}'")

        os.remove(output_path_png)


def make_grey(source_image):
    """Add a slight greyscale to the image."""

    # Found here:
    # https://stackoverflow.com/questions/16070078/change-saturation-with-imagekit-pil-or-pillow/16070333#16070333

    return ImageEnhance.Color(source_image).enhance(0.2)


def copy_svg_icon(destination_file, source_file):
    """Copies svg icon to images."""

    # check if the source exists
    if os.path.exists(source_file):
        # check if the destination exists
        copyfile(source_file, destination_file)
        print(f"- '{source_file}' was copied to '{destination_file}'")


def create_menu_icons(destination_directory, source_file_directory):
    """Creates all menu icon images (.png)."""

    # check if the source exists
    if os.path.exists(source_file_directory):
        # create the directory if there is no such directory
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        # check if the destination is a directory
        if os.path.isdir(source_file_directory):
            for file in os.listdir(source_file_directory):
                file = os.path.join(source_file_directory, file)
                if not os.path.isabs(file):
                    file = os.path.abspath(file)
                filename, file_extension = os.path.splitext(file)
                if file_extension == ".svg":
                    convert_svg_2_png(file, os.path.join(
                        destination_directory, os.path.basename(filename) + ".png"), 15, 15)
    print("All menu icons were created")


def create_preload_image(destination_path, source_file):
    """Creates preload image (.png)."""

    if os.path.exists(source_file):
        convert_svg_2_png(source_file, destination_path, 500, 350)
        print("Preloader image was created")


if __name__ == '__main__':
    """Creates all images."""

    srcDir = os.path.join(DIR_PATH, "..", "DesktopClient")
    winInstallDir = os.path.join(DIR_PATH, "..", "WindowsInstaller")
    srcImagesDir = os.path.join(srcDir, "res", "images")

    create_png_favicons(
        os.path.join(srcImagesDir, "favicons"),
        "logo.svg"
    )
    create_installer_pages(
        os.path.join(winInstallDir, "pictures"),
        "installer.svg"
    )
    create_installer_icons(
        os.path.join(winInstallDir, "icons"),
        "logo.svg"
    )
    create_program_icon(
        os.path.join(srcImagesDir, "favicons"),
        "logo.svg"
    )
    copy_svg_icon(
        os.path.join(srcImagesDir, "favicons", "favicon.svg"),
        "logo.svg"
    )
    create_menu_icons(
        os.path.join(srcImagesDir, "icons"),
        "icons"
    )
    create_preload_image(
        os.path.join(srcImagesDir, "preload.png"),
        "preloader.svg"
    )

    print("Ready!")
