.PHONY: build clean dist install install_desktop img web create_windows_installer

SRC_DIR=DesktopClient
BIN_DIR=bin
PROJECT_NAME=KaraokeMusicVideoManager
VERSION=2.0.0

ifeq ($(PREFIX),)
    PREFIX := /usr/bin
endif
ifeq ($(PREFIX_DESKTOP),)
    PREFIX_DESKTOP := /usr/share/applications
endif

all: build dist

clean:
	rm -rf $(BIN_DIR) pkg karaokemusicvideomanager.git src
	rm -f *.pkg.tar.xz *.jar
	cd $(SRC_DIR); \
	mvn clean

# Build the program
build:
	cd $(SRC_DIR); \
	mvn install

# Clean up build and extract/rename executable
dist:
	cd $(SRC_DIR); \
	python3 format_exported_jar.py

	mkdir -p $(BIN_DIR)
	cp $(PROJECT_NAME)-portable-$(VERSION).jar $(BIN_DIR)/

	echo -e "\
	#!/usr/bin/env bash\n\
	java -jar $(PROJECT_NAME)-portable-$(VERSION).jar\n\
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
	cd ImageResources; \
	python3 create_image_resources.py

# Update web data
update_web_interfaces:
	cd WebInterfaces; \
	python3 create_website_resources.py

# Install built program
install:
	install -d $(DESTDIR)$(PREFIX)/

	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME)-portable-$(VERSION).jar $(DESTDIR)$(PREFIX)/
	sed -i s#$(PROJECT_NAME)-portable#$(PREFIX)/$(PROJECT_NAME)-portable# $(BIN_DIR)/$(PROJECT_NAME)
	install -Dm 777 $(BIN_DIR)/$(PROJECT_NAME) $(DESTDIR)$(PREFIX)/
	sed -i s#$(PREFIX)/$(PROJECT_NAME)-portable#$(PROJECT_NAME)-portable# $(BIN_DIR)/$(PROJECT_NAME)

# Install a desktop file for the installed program
install_desktop:
	install -d $(DESTDIR)$(PREFIX_DESKTOP)/

	sed -i s#Exec=#Exec=$(PREFIX)/# $(BIN_DIR)/$(PROJECT_NAME).desktop
	sed -i s#Icon=#Icon=$(PREFIX_DESKTOP)/# $(BIN_DIR)/$(PROJECT_NAME).desktop
	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME).desktop $(DESTDIR)$(PREFIX_DESKTOP)/
	sed -i s#Exec=$(PREFIX)/#Exec=# $(BIN_DIR)/$(PROJECT_NAME).desktop
	sed -i s#Icon=$(PREFIX_DESKTOP)/#Icon=# $(BIN_DIR)/$(PROJECT_NAME).desktop

	install -Dm 644 $(BIN_DIR)/$(PROJECT_NAME).svg $(DESTDIR)$(PREFIX_DESKTOP)/

# Uninstall installed program
uninstall:
	rm -f $(PREFIX)/$(PROJECT_NAME)-portable-$(VERSION).jar
	rm -f $(PREFIX)/$(PROJECT_NAME)

	rm -f $(PREFIX_DESKTOP)/$(PROJECT_NAME).desktop
	rm -f $(PREFIX_DESKTOP)/$(PROJECT_NAME).svg

create_package:
	makepkg .
	# Install with
	# pacman -U packagename.tar.gz

create_windows_installer:
	cd WindowsInstaller; \
	python3 build_windows_installer.py
