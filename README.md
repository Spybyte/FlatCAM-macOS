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

```bash
# Clone & enter the repo
git clone <repo-url> && cd FlatCAM-OSX

# Create a virtual environment (recommended)
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python -m flatcam          # preferred
# or
python FlatCAM.py          # backward-compatible shim
```

For development (editable install):

```bash
pip install -e .
```

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

- **Python** >= 3.9 (tested with 3.12)
- **PyQt5**
- All other dependencies are listed in `requirements.txt`

---

## Installation

### macOS

```bash
# Install Homebrew (if not already installed)
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and PyQt5
brew install python@3.12 pyqt@5

# Clone the repository
git clone <repo-url> && cd FlatCAM-OSX

# Set up a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FlatCAM
python -m flatcam
```

### Linux (Ubuntu / Debian)

```bash
# Make sure Python 3 and pip are installed
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Clone the repository
git clone <repo-url> && cd FlatCAM-OSX

# Option A – use the setup script
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh

# Option B – manual venv setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run FlatCAM
python3 -m flatcam
```

Alternatively, using `make`:

```bash
make install_dependencies   # optional, if system deps are missing
make install                # user-local install
sudo make install           # system-wide install
```

### Windows

```powershell
# Install Python 3.12+ from https://www.python.org/downloads/
# Make sure "Add Python to PATH" is checked during installation.

# Clone the repository
git clone <repo-url>
cd FlatCAM-OSX

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FlatCAM
python -m flatcam
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
