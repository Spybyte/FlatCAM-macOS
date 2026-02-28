from setuptools import setup


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
        'CFBundleVersion': '8.994',
        'CFBundleShortVersionString': '8.994',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
}


setup(
    name='FlatCAM',
    app=APP,
    options={'py2app': OPTIONS},
)