.PHONY: build dist install img web

SRC_DIR=DesktopClient
BIN_DIR=bin
PROJECT_NAME=KaraokeMusicVideoManager
VERSION=2.0.0

ifeq ($(PREFIX),)
    PREFIX := /usr/bin
endif

all: build dist

# Build the program
build:
	echo "Build 'portable' runnable jar:"
	cd $(SRC_DIR); \
	mvn install

# Clean up build and extract/rename executable
dist:
	echo "Dist (rename) runnable jar:"
	cd $(SRC_DIR); \
	python3 format_exported_jar.py

	mkdir -p $(BIN_DIR)
	cp $(PROJECT_NAME)-portable-$(VERSION).jar $(BIN_DIR)/

	echo -e "\
	#!/usr/bin/env bash\n\
	java -jar $(PROJECT_NAME)-portable-$(VERSION).jar\
	" > $(BIN_DIR)/$(PROJECT_NAME)
	chmod +x $(BIN_DIR)/$(PROJECT_NAME)

	cp ImageResources/logo.svg  $(BIN_DIR)/$(PROJECT_NAME).svg
	echo -e "\
	[Desktop Entry]\n\
	Version=1.0\n\
	Type=Application\n\
	Terminal=false\n\
	Exec=$(PROJECT_NAME)\n\
	Name=$(PROJECT_NAME)\n\
	Comment=Index local music videos to search and open them\n\
	Icon=$(PROJECT_NAME).svg\n\
	" > $(BIN_DIR)/$(PROJECT_NAME).desktop

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

# Install built program
install:
	install -d $(DESTDIR)$(PREFIX)/
	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME)-portable-$(VERSION).jar $(DESTDIR)$(PREFIX)/
	install -Dm 777 $(BIN_DIR)/$(PROJECT_NAME) $(DESTDIR)$(PREFIX)/

# Install a desktop file for the installed program
install_desktop:
	sed -i s#Exec=#Exec=$(DESTDIR)$(PREFIX)/# bin/$(PROJECT_NAME).desktop
	sed -i s#Icon=#Icon=/usr/share/applications/# bin/$(PROJECT_NAME).desktop
	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME).desktop /usr/share/applications/
	sed -i s#Exec=$(DESTDIR)$(PREFIX)/#Exec=# bin/$(PROJECT_NAME).desktop
	sed -i s#Icon=/usr/share/applications/#Icon=# bin/$(PROJECT_NAME).desktop

	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME).svg /usr/share/applications/

# Uninstall installed program
uninstall:
	echo $(DESTDIR)
	echo $(PREFIX)

	rm -f $(DESTDIR)$(PREFIX)/$(PROJECT_NAME)-portable-$(VERSION).jar
	rm -f $(DESTDIR)$(PREFIX)/$(PROJECT_NAME)

	rm -f /usr/share/applications/$(PROJECT_NAME).desktop
	rm -f /usr/share/applications/$(PROJECT_NAME).svg

create_package:
	makepkg .
	# Install with
	# pacman -U packagename.tar.gz
