#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
With executing this script you convert all the template files in this folder as they are to
this moment into usable templates for the Java Desktop Client.
That means simply said: Change something like css in the template, double click the script
and all your changes (css, additional things) are saved in the Java project.
'''

import json
import os

PATH_HTML = "html"
HTML_FILES = ["html_static", "html_party", "html_party_live"]
HTML_HEAD = "html_head"
PATH_PHP = "php"
PHP_FILE_FORM = "form"
PHP_FILE_PROCESS = "process"
PHP_COPY_FILES = ["live", "live_without_votes", "vote"]
PATH_CSS = "css"
CSS_FILES = ["styles_static", "styles_searchable",
             "styles_party", "styles_php_form", "styles_party_live"]
PATH_JS = "js"
JS_FILES = ["jquery.min", "w3"]


def css_to_json(output_path):
    """ Save all css files in one json file """

    # create an empty (json) dictionary for the json file
    json_css = {}

    for css_file in CSS_FILES:

        # create walking string
        walking_css_string = ""

        # walk through all lines of the current css file
        for line in read_text_file_to_lines(os.path.join(PATH_CSS, css_file + ".css")):
            # strip whitespaces, tabs and paragraphs from line
            line = line.strip()
            # check if the line is neither empty nor a comment
            if line != "" and not line.startswith("/*"):
                # if yes save content in the walking string
                walking_css_string += line

        # save the css file in the dictionary
        json_css[css_file] = walking_css_string

    dictionary_to_json(output_path, json_css)


def read_text_file_to_lines(text_file_path):
    """ Read a text file and return all the lines """

    # read the file and return all the lines
    with open(text_file_path) as file:
        return file.readlines()


def dictionary_to_json(output_path, json_dictionary):
    """ Save a dictionary in a json file """

    # save the json dictionary in a json file
    with open(output_path, 'w') as outfile:
        json.dump(json_dictionary, outfile)

    # print the write process to the console
    print("- Json file exported: " + output_path)


def html_to_json(output_path):
    """ Save all html files in one json file """

    # create an empty (json) dictionary for the json file
    json_html = {}

    walking_html_string = ""

    for line in read_text_file_to_lines(os.path.join(PATH_HTML, HTML_HEAD + ".html")):
        # strip whitespaces, tabs and paragraphs from line
        line = line.strip()
        # check if the line is neither empty nor a comment
        if line != "":
            if line.startswith("<head>"):
                walking_html_string = ""
                walking_html_string_special = ""
            elif line.startswith("</head>"):
                walking_html_string_special += walking_html_string
                json_html['head'] = walking_html_string_special
            elif line.startswith("<!--"):
                # now the categories:
                if "custom-begin" in line:
                    # reset the string when the custom head begins
                    walking_html_string_special += walking_html_string
                    walking_html_string = ""
                elif "custom-end" in line:
                    walking_html_string = ""
                elif "favicon-begin" in line:
                    # reset the string when the custom head begins
                    walking_html_string_special += walking_html_string
                    walking_html_string = ""
                elif "favicon-end" in line:
                    # reset the string when the custom head begins
                    walking_html_string = ""
            else:
                walking_html_string += line

    for html_file in HTML_FILES:

        # create walking string
        walking_html_string = ""

        # walk through all lines of the current css file
        for line in read_text_file_to_lines(os.path.join(PATH_HTML, html_file + ".html")):
            # strip whitespaces, tabs and paragraphs from line
            line = line.strip()
            # check if the line is neither empty nor a comment
            if line != "":
                if line.startswith("<!--"):
                    # now the categories:
                    if "custom-head-begin" in line:
                        # reset the string when the custom head begins
                        walking_html_string = ""
                    elif "custom-head-end" in line:
                        # save the custom head
                        json_html['custom-head-' +
                                  html_file] = walking_html_string
                    elif "body-begin" in line:
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "floating-button-begin" in line:
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "floating-button-end" in line:
                        # save the first part of the floating button
                        json_html['floating-button-' +
                                  html_file] = walking_html_string
                        # reset the string when the the button ends
                        walking_html_string = ""
                    elif "begin-section-end" in line:
                        # save the first part of the floating button
                        json_html['section-start-' +
                                  html_file] = walking_html_string
                        # reset the string when the the button ends
                        walking_html_string = ""
                    elif "overlay-begin" in line:
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "overlay-end" in line:
                        # save everything before the overlay to the table
                        json_html['overlay-' + html_file] = walking_html_string
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "form-start" in line:
                        # save everything before the overlay to the table
                        json_html['form-start-' +
                                  html_file] = walking_html_string
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "table-header-begin" in line:
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "example-table-begin" in line:
                        # save everything before the overlay to the table
                        json_html['table-header-' +
                                  html_file] = walking_html_string
                    elif "example-table-end" in line:
                        # reset the string when the example table ends
                        walking_html_string = ""
                    elif "before-form-end" in line:
                        json_html['before-form-' +
                                  html_file] = walking_html_string
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "after-form-end" in line:
                        json_html['form-end-' +
                                  html_file] = walking_html_string
                        # reset the string when the the body begins
                        walking_html_string = ""
                    elif "demo-playlist-end" in line:
                        # reset the string when the the demo playlist ends
                        walking_html_string = ""
                    elif "body-end" in line:
                        # save everything after the table to the end of the body
                        json_html['after-table-' +
                                  html_file] = walking_html_string
                        walking_html_string = ""
                    elif "script-repeat" in line:
                        # save everything after the table to the end of the body
                        json_html['repeat-script-' +
                                  html_file] = walking_html_string
                else:
                    walking_html_string += line

    dictionary_to_json(output_path, json_html)


def php_to_json(output_path):
    """Save changes to the php add to playlist form template."""

    # create an empty (json) dictonary for the json file
    json_php = {}

    walking_php_string = ""

    for line in read_text_file_to_lines(os.path.join(PATH_PHP, PHP_FILE_FORM + ".php")):
        # strip whitespaces, tabs and paragraphs from line
        line = line.strip()
        # check if the line is neither empty nor a comment
        if line != "":
            if line.startswith("<!--"):
                # now the categories:
                if "before-html" in line:
                    json_php['before-html-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "custom-head-begin" in line:
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "custom-head-end" in line:
                    json_php['custom-head-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "floating-button-begin" in line:
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "floating-button-end" in line:
                    json_php['floating-button-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "before-title" in line:
                    json_php['before-title-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "after-title" in line:
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "before-artist" in line:
                    json_php['before-artist-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "after-artist" in line:
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "before-input" in line:
                    json_php['before-input-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "after-input" in line:
                    json_php['input-' + PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "before-submit" in line:
                    json_php['before-submit-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "after-submit" in line:
                    json_php['submit-' + PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                elif "body-end" in line:
                    json_php['after-submit-' +
                             PHP_FILE_FORM] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
            elif line.startswith('<?php'):
                if line.startswith('<?php '):
                    walking_php_string += line
                else:
                    walking_php_string += line + "\n"
            elif line.startswith('?>'):
                walking_php_string += "\n" + line
            elif not line.startswith('#'):
                walking_php_string += line

    walking_php_string = ""

    for line in read_text_file_to_lines(os.path.join(PATH_PHP, PHP_FILE_PROCESS + ".php")):
        # strip whitespaces, tabs and paragraphs from line
        line = line.strip()
        # check if the line is neither empty nor a comment
        if line != "":
            if line.startswith("#"):
                # now the categories:
                if "link-begin" in line:
                    json_php['before-link-' +
                             PHP_FILE_PROCESS] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
                if "link-end" in line:
                    json_php['link-' + PHP_FILE_PROCESS] = walking_php_string
                    # reset the string when the custom head begins
                    walking_php_string = ""
            elif line.startswith('<?php'):
                if line.startswith('<?php '):
                    walking_php_string += line
                else:
                    walking_php_string += line + "\n"
            elif line.startswith('?>'):
                walking_php_string += "\n" + line
            else:
                walking_php_string += line

    json_php['after-link-' + PHP_FILE_PROCESS] = walking_php_string

    for php_file in PHP_COPY_FILES:

        walking_php_string = ""

        for line in read_text_file_to_lines(os.path.join(PATH_PHP, php_file + ".php")):
            # strip whitespaces, tabs and paragraphs from line
            line = line.strip()
            # check if the line is neither empty nor a comment
            if line != "":
                if line.startswith('<?php'):
                    if line.startswith('<?php '):
                        walking_php_string += line
                    else:
                        walking_php_string += line + "\n"
                elif line.startswith('?>'):
                    walking_php_string += "\n" + line
                elif not line.startswith("#"):
                    walking_php_string += line

        json_php['php-data-' + php_file] = walking_php_string

    dictionary_to_json(output_path, json_php)


def js_to_json(output_path):
    """Copy javascript to java project."""

    json_javascript = {}

    for js_file in JS_FILES:

        # read the css file
        with open(os.path.join(PATH_JS, js_file + ".js")) as file:
            content_js = file.readlines()

        # create an empty "walking" string with the opening style tag
        walking_js_string = ""

        # walk through all lines of the html email
        for line in content_js:
            # strip whitespaces, tabs and paragraphs from line
            walking_js_string += line.strip()

        json_javascript[js_file] = walking_js_string

    # save the json dictionary in a json file
    with open(output_path, 'w') as outfile:
        json.dump(json_javascript, outfile)

    print("- Json file copied to: " + output_path)


if __name__ == '__main__':

    # main output path for website data
    MAIN_OUTPUT_DIRECTORY = os.path.join(
        os.pardir, "DesktopClient/res/websiteData")

    # create the directory if there is no such directory
    if not os.path.exists(MAIN_OUTPUT_DIRECTORY):
        os.makedirs(MAIN_OUTPUT_DIRECTORY)

    # css website data to json
    CSS_OUTPUT_PATH = os.path.join(MAIN_OUTPUT_DIRECTORY, "css.json")
    css_to_json(CSS_OUTPUT_PATH)

    # the html data to json
    HTML_OUTPUT_PATH = os.path.join(MAIN_OUTPUT_DIRECTORY, "html.json")
    html_to_json(HTML_OUTPUT_PATH)

    # part of the php data to json
    PHP_OUTPUT_PATH = os.path.join(MAIN_OUTPUT_DIRECTORY, "php.json")
    php_to_json(PHP_OUTPUT_PATH)

    # copy javascript to websites data libraries
    JAVASCRIPT_W3_OUTPUT_PATH = os.path.join(MAIN_OUTPUT_DIRECTORY, "js.json")
    js_to_json(JAVASCRIPT_W3_OUTPUT_PATH)

    print("Ready!")
