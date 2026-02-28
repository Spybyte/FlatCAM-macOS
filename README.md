# FlatCAM-OSX

**2D Computer-Aided PCB Manufacturing**

> macOS-focused fork by Björn Bubbat (2016), based on
> [FlatCAM BETA](https://bitbucket.org/jpcgt/flatcam) by Marius Stanciu (2019)
> and the original [FlatCAM](http://flatcam.org/) by Juan Pablo Caram (2014–2016).

FlatCAM prepares CNC jobs for manufacturing PCBs on a CNC router.
It reads Gerber, Excellon, DXF, SVG, and HPGL2 files and generates
G-Code for isolation routing, drilling, copper thieving, and more.

---

## Quick Start

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone & enter the repo
git clone <repo-url> && cd FlatCAM-OSX

# Install dependencies & create virtualenv (uv handles both)
uv sync

# Include optional OR-Tools optimization support
uv sync --extra optimization

# Run
uv run flatcam             # preferred
# or
make run                   # via Makefile
```

For development (editable install is the default with `uv sync`).

> **Legacy alternative:** `pip install -r requirements.txt` and `python -m flatcam`
> still work but are no longer the recommended workflow.

---

## Project Structure

All Python source code lives under `src/flatcam/` as a proper installable package:

```
src/flatcam/
├── __init__.py          # Package root, PROJECT_ROOT, __version__
├── __main__.py          # Entry point (python -m flatcam)
├── app.py               # Main application class
├── defaults.py          # Default settings
├── bookmark.py          # Bookmark management
├── cam/                 # CAM library (geometry & toolpath engine)
├── core/                # Utilities, workers, pool, database,
│                        #   preprocessor base, translation
├── editors/             # Interactive editors (Geometry, Excellon, Gerber, …)
├── gui/                 # Main window, UI widgets, VisPy canvas
│   └── preferences/     # Preference panels (cncjob, excellon, general,
│                        #   geometry, gerber, tools, utilities)
├── objects/             # FlatCAM document objects (Gerber, Excellon, …)
├── parsers/             # File-format parsers (Gerber, Excellon, DXF, SVG, …)
├── preprocessors/       # G-Code post-processor definitions
├── tcl/                 # Tcl/Tk command framework & shell commands
├── tools/               # Application tools (Isolation, Drilling, NCC, …)
└── vendor/
    └── descartes/       # Vendored (patched) descartes library
```

| Directory   | Purpose                                             |
|-------------|-----------------------------------------------------|
| `assets/`   | Icons, example files, platform-specific resources   |
| `config/`   | Portability configuration                           |
| `locale/`   | Translations (de, en, es, fr, it, pt_BR, ro, ru, tr) |
| `tests/`    | Test scripts                                        |
| `doc/`      | Sphinx documentation source                         |

---

## Requirements

- **Python** >= 3.12 (tested with 3.14)
- **[uv](https://docs.astral.sh/uv/)** >= 0.10 (package manager)
- **PyQt5**
- All dependencies are declared in `pyproject.toml` and locked in `uv.lock`

---

## Installation

### macOS

```bash
# Install Homebrew (if not already installed)
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install uv
brew install uv

# Clone the repository
git clone <repo-url> && cd FlatCAM-OSX

# Install dependencies (creates .venv automatically)
uv sync --extra optimization

# Run FlatCAM
uv run flatcam
```

### Linux (Ubuntu / Debian)

```bash
# Option A – use the setup script (installs uv + system deps automatically)
git clone <repo-url> && cd FlatCAM-OSX
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh

# Option B – manual setup
sudo apt-get update
sudo apt-get install python3 python3-venv libgdal-dev
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone <repo-url> && cd FlatCAM-OSX
uv sync --extra optimization
uv run flatcam
```

Useful Makefile targets:

```bash
make sync                   # uv sync (core deps only)
make sync-all               # uv sync --extra optimization
make run                    # uv run flatcam
make bundle-alias           # build alias app bundle for fast debug
make bundle                 # build self-contained py2app bundle
make test                   # uv run pytest tests/
make lock                   # uv lock (regenerate lockfile)
```

### Build macOS `.app` bundle (py2app)

For a self-contained macOS app bundle, use py2app (0.28.10) from the uv-managed environment:

```bash
# Ensure all dependencies are installed, including optimization extras (OR-Tools)
uv sync --extra optimization --group dev

# Fast validation build (uses sources in place, symlinks to source)
make bundle-alias

# Final self-contained app bundle (standalone, distributable)
make bundle

# Verify code signature
codesign -v --deep dist/FlatCAM.app
```

The generated application is at `dist/FlatCAM.app`.

The build automatically:
- Generates a multi-resolution `.icns` icon (only when the source PNG changes)
- Bundles all Python dependencies, Qt plugins, assets, config, and locale files
- Verifies and repairs any dylib code signatures corrupted by macholib
- Ad-hoc signs the final `.app` bundle

The bundle version (`CFBundleVersion`) is read automatically from `src/flatcam/__init__.py`.

### Windows

```powershell
# Install uv (https://docs.astral.sh/uv/getting-started/installation/)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone the repository
git clone <repo-url>
cd FlatCAM-OSX

# Install dependencies
uv sync --extra optimization

# Run FlatCAM
uv run flatcam
```

---

## Credits

| Role               | Name                          |
|--------------------|-------------------------------|
| macOS fork         | Björn Bubbat (2016–present)   |
| FlatCAM BETA       | Marius Stanciu (2019)         |
| Original FlatCAM   | Juan Pablo Caram (2014–2016)  |

## License

See [LICENSE](LICENSE) for details.

## Links

- [FlatCAM homepage](http://flatcam.org/)
- [Upstream Bitbucket repository](https://bitbucket.org/jpcgt/flatcam)
- [YouTube tutorials](https://www.youtube.com/playlist?list=PLVvP2SYRpx-AQgNlfoxw93tXUXon7G94_)
