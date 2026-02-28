"""
FlatCAM entry point shim.
Adds src/ to sys.path and delegates to flatcam.__main__.main().
Use `python -m flatcam` (with PYTHONPATH=src or pip install -e .) as the preferred way to run.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

if __name__ == '__main__':
    from flatcam.__main__ import main
    main()

