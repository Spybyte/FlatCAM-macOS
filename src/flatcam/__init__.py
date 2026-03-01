"""
FlatCAM - 2D Computer-Aided PCB Manufacturing
"""
import os
import sys
from pathlib import Path

# Canonical project root.
# - Source run: two levels up from this file (src/flatcam/__init__.py -> project root)
# - Frozen app (py2app): Resources directory exposed via RESOURCEPATH
if getattr(sys, 'frozen', False):
	PROJECT_ROOT = Path(os.environ.get('RESOURCEPATH', Path(__file__).resolve().parents[2]))
else:
	PROJECT_ROOT = Path(__file__).resolve().parents[2]

__version__ = "8.994dev2"
