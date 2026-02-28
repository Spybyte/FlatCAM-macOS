
# Install on Ubuntu(-like) systems

# Install system-level dependencies (C libs, etc.)
install_dependencies:
	sudo -H ./setup_ubuntu.sh

ICON_SRC := assets/resources/flatcam_icon256.png
ICON_DST := assets/resources/FlatCAM.icns

# Rebuild .icns only when the source PNG changes
$(ICON_DST): $(ICON_SRC)
	rm -rf build/FlatCAM.iconset
	mkdir -p build/FlatCAM.iconset
	@for pair in '16 16 icon_16x16' '32 32 icon_16x16@2x' '32 32 icon_32x32' \
	             '64 64 icon_32x32@2x' '128 128 icon_128x128' '256 256 icon_128x128@2x' \
	             '256 256 icon_256x256' '512 512 icon_256x256@2x' '512 512 icon_512x512' \
	             '1024 1024 icon_512x512@2x'; do \
		set -- $$pair; \
		sips -z $$1 $$2 $(ICON_SRC) --out build/FlatCAM.iconset/$$3.png >/dev/null; \
	done
	iconutil -c icns build/FlatCAM.iconset -o $(ICON_DST)

bundle-icon: $(ICON_DST)

bundle-alias: bundle-icon
	rm -rf build dist
	uv run python setup.py py2app -A

bundle: bundle-icon
	@# Move old build artifacts aside first (avoids "Directory not empty" when
	@# Finder or a lingering process still holds file handles in dist/).
	rm -rf build .dist_old
	-mv dist .dist_old 2>/dev/null; rm -rf .dist_old &
	uv run python setup.py py2app
	@# Verify dylib signatures; repair any that macholib corrupted.
	@bad=0; for lib in dist/FlatCAM.app/Contents/Frameworks/*.dylib; do \
		if ! codesign -v "$$lib" 2>/dev/null; then \
			bad=$$((bad+1)); \
			name=$$(basename "$$lib"); \
			src="/opt/homebrew/lib/$$name"; \
			if [ -f "$$src" ]; then \
				cp "$$src" "$$lib"; \
				install_name_tool -id "@executable_path/../Frameworks/$$name" "$$lib" 2>/dev/null; \
			fi; \
			codesign --force --sign - "$$lib" 2>/dev/null || echo "WARNING: could not sign $$name"; \
		fi; \
	done; \
	if [ $$bad -gt 0 ]; then echo "Repaired $$bad corrupted dylib(s)"; \
	else echo "All dylibs have valid signatures"; fi
	codesign --force --deep --sign - dist/FlatCAM.app 2>/dev/null || true
	@echo "Bundle created at dist/FlatCAM.app"

# uv-based development targets
sync:
	uv sync

sync-all:
	uv sync --extra optimization

run:
	uv run flatcam

lock:
	uv lock

test:
	QT_QPA_PLATFORM=offscreen uv run pytest tests/

# Install system dependencies for macOS
setup-macos:
	brew install geos spatialindex freetype libpng
	@echo ""
	@echo "System dependencies installed. Run 'make install' next."

USER_ID = $(shell id -u)

LOCAL_PATH = $(shell pwd)
LOCAL_APPS_PATH = ~/.local/share/applications
ASSEST_PATH = assets/linux

INSTALL_PATH = /usr/share/flatcam-beta
APPS_PATH = /usr/share/applications

MIN_PY3_MINOR_VERSION := 12
PY3_MINOR_VERSION := $(shell python3 --version | cut -d'.' -f2)

ifneq ($(MIN_PY3_MINOR_VERSION), $(firstword $(sort $(PY3_MINOR_VERSION) $(MIN_PY3_MINOR_VERSION))))
    $(info Current python version is 3.$(PY3_MINOR_VERSION))
    $(error You must have at least 3.$(MIN_PY3_MINOR_VERSION) installed)
endif

install:
ifeq ($(USER_ID), 0)
	@ echo "Installing it system-wide"
	cp -rf $(LOCAL_PATH) $(INSTALL_PATH)
	@ sed -i "s|python_script_path=.*|python_script_path=$(INSTALL_PATH)|g" $(INSTALL_PATH)/assets/linux/flatcam-beta
	ln -sf $(INSTALL_PATH)/assets/linux/flatcam-beta /usr/local/bin
	cp -f $(ASSEST_PATH)/flatcam-beta.desktop $(APPS_PATH)
	@ sed -i "s|Exec=.*|Exec=$(INSTALL_PATH)/$(ASSEST_PATH)/flatcam-beta|g" $(APPS_PATH)/flatcam-beta.desktop
	@ sed -i "s|Icon=.*|Icon=$(INSTALL_PATH)/$(ASSEST_PATH)/icon.png|g" $(APPS_PATH)/flatcam-beta.desktop
else
	@ echo "Installing locally for $(USER) only"
	cp -f $(ASSEST_PATH)/flatcam-beta.desktop $(LOCAL_APPS_PATH)
	@ sed -i "s|Exec=.*|Exec=$(LOCAL_PATH)/$(ASSEST_PATH)/flatcam-beta|g" $(LOCAL_APPS_PATH)/flatcam-beta.desktop
	@ sed -i "s|Icon=.*|Icon=$(LOCAL_PATH)/$(ASSEST_PATH)/icon.png|g" $(LOCAL_APPS_PATH)/flatcam-beta.desktop
endif

remove:
ifeq ($(USER_ID), 0)
	@ echo "Uninstalling it system-wide"
	rm -rf $(INSTALL_PATH)
	rm -f /usr/local/bin/flatcam-beta
	rm -r $(APPS_PATH)/flatcam-beta.desktop
else
	@ echo "Uninstalling only for $(USER) user"
	rm -f $(LOCAL_APPS_PATH)/flatcam-beta.desktop
endif
