.PHONY: build img web

SRC_DIR=DesktopClient

all: build dist

# Build the program
build:
	echo "Build 'portable' runnable jar:"
	cd $(SRC_DIR); \
	mvn clean install

# Clean up build and extract/rename executable
dist:
	echo "Dist (rename) runnable jar:"
	cd $(SRC_DIR); \
	python3 format_exported_jar.py

# Update images
update_images:
	echo "Update/Create all images and icons: (wait some seconds)"
	cd ImageResources; \
	python3 create_image_resources.py

# Update web data
update_web_interfaces:
	echo "Update/Create all web interfaces:"
	cd WebInterfaces; \
	python3 create_website_resources.py
