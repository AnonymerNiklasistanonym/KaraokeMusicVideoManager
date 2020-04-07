#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Rename the eventually created runnable jar
'''

import os
from xml.dom import minidom

XML_FILE = "pom.xml"

XML_TREE = minidom.parse(XML_FILE)

# get version and name from the pom.xml file
ARTIFACT_ID = XML_TREE.getElementsByTagName("artifactId")[0].firstChild.data
VERSION = XML_TREE.getElementsByTagName("version")[0].firstChild.data

# the exported file path/name
EXPORTED_FILE_PATH = os.path.join(
    "..", f"{ARTIFACT_ID}-{VERSION}-jar-with-dependencies.jar"
)
# the exported file path/name we really want
WISHED_FILE_PATH = os.path.join(
    "..",  f"{ARTIFACT_ID}-portable-{VERSION}.jar"
)

# check if the exported file even exists
if os.path.isfile(EXPORTED_FILE_PATH):
    # check if the wished exported file exists
    if os.path.isfile(WISHED_FILE_PATH):
        print(WISHED_FILE_PATH + " will be overwritten!")
        os.remove(WISHED_FILE_PATH)
    os.rename(EXPORTED_FILE_PATH, WISHED_FILE_PATH)
    print(EXPORTED_FILE_PATH + " renamed to " + WISHED_FILE_PATH)
# check then if the wished exported file exists
elif os.path.isfile(WISHED_FILE_PATH):
    print(EXPORTED_FILE_PATH + " doesn't exist and wished the filename " +
          WISHED_FILE_PATH + " already exists!")
else:
    print("No .jar file to rename or already renamed was found!")
