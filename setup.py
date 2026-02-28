import os
import sys

from setuptools import setup

# Import version from the package (single source of truth)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from flatcam import __version__


# py2app >=0.28.9 rejects install_requires, but setuptools auto-populates it
# from pyproject.toml [project.dependencies].  Clear it just before py2app
# sees it by patching finalize_options — only when actually running py2app.
if 'py2app' in sys.argv:
    import py2app.build_app as _build_app
    _orig_finalize = _build_app.py2app.finalize_options

    def _patched_finalize(self):
        self.distribution.install_requires = []
        _orig_finalize(self)

    _build_app.py2app.finalize_options = _patched_finalize


APP = ['FlatCAM.py']

OPTIONS = {
    'argv_emulation': False,
    'arch': 'arm64',
    'iconfile': 'assets/resources/FlatCAM.icns',
    'packages': [
        'flatcam',
        'ctypes',
        'vispy',
        'matplotlib',
        'shapely',
        'rtree',
        'rasterio',
        'ezdxf',
        'fontTools',
        'reportlab',
        'svglib',
        'qrcode',
        'simplejson',
        'freetype',
        'lxml',
        'serial',
        'dill',
        'ortools',
        'multiprocessing',
        'encodings',
        'json',
        'email',
        'html',
        'http',
        'xml',
        'logging',
        'unittest',
        'urllib',
    ],
    'includes': [
        'OpenGL',
        'OpenGL.GL',
        'OpenGL_accelerate',
        'svg.path',
        'flatcam.preprocessors',
        'flatcam.tcl',
        'cffi',
        'cairocffi',
    ],
    'resources': ['assets', 'config', 'locale'],
    'qt_plugins': ['platforms', 'imageformats', 'styles'],
    'plist': {
        'CFBundleName': 'FlatCAM',
        'CFBundleDisplayName': 'FlatCAM',
        'CFBundleIdentifier': 'io.flatcam.FlatCAM',
        'CFBundleVersion': __version__,
        'CFBundleShortVersionString': __version__,
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
}


setup(
    name='FlatCAM',
    app=APP,
    options={'py2app': OPTIONS},
)