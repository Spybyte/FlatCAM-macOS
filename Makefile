
# Install on Ubuntu(-like) systems

# Install system-level dependencies (C libs, etc.)
install_dependencies:
	sudo -H ./setup_ubuntu.sh

bundle-icon:
	rm -rf build/FlatCAM.iconset
	mkdir -p build/FlatCAM.iconset
	sips -z 16 16 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_16x16.png
	sips -z 32 32 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_16x16@2x.png
	sips -z 32 32 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_32x32.png
	sips -z 64 64 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_32x32@2x.png
	sips -z 128 128 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_128x128.png
	sips -z 256 256 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_128x128@2x.png
	sips -z 256 256 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_256x256.png
	sips -z 512 512 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_256x256@2x.png
	sips -z 512 512 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_512x512.png
	sips -z 1024 1024 assets/resources/flatcam_icon256.png --out build/FlatCAM.iconset/icon_512x512@2x.png
	iconutil -c icns build/FlatCAM.iconset -o assets/resources/FlatCAM.icns

bundle-alias: bundle-icon
	rm -rf build dist
	uv run python setup.py py2app -A

bundle: bundle-icon
	@# Move old build artifacts aside first (avoids "Directory not empty" when
	@# Finder or a lingering process still holds file handles in dist/).
	rm -rf build .dist_old
	-mv dist .dist_old 2>/dev/null; rm -rf .dist_old &
	uv run python setup.py py2app
	@echo "Fixing bundled native libraries..."
	@# py2app's macholib can corrupt code signatures when rewriting load paths.
	@# Fix: replace corrupted dylibs with fresh copies, rewrite install names, re-sign.
	@for lib in dist/FlatCAM.app/Contents/Frameworks/*.dylib; do \
		if ! codesign -v "$$lib" 2>/dev/null; then \
			name=$$(basename "$$lib"); \
			src="/opt/homebrew/lib/$$name"; \
			if [ -f "$$src" ]; then \
				echo "  Replacing corrupted $$name with fresh copy from homebrew..."; \
				cp "$$src" "$$lib"; \
				install_name_tool -id "@executable_path/../Frameworks/$$name" "$$lib" 2>/dev/null; \
			fi; \
			codesign --force --sign - "$$lib" 2>/dev/null || echo "  WARNING: could not sign $$name"; \
		fi; \
	done
	@echo "Re-signing bundle..."
	@codesign --force --deep --sign - dist/FlatCAM.app 2>/dev/null || true
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
	uv run pytest tests/

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
