"""
FlatCAM entry point shim (legacy).
Adds src/ to sys.path and delegates to flatcam.__main__.main().

Preferred way to run:
    uv run flatcam
    uv run python -m flatcam
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

if __name__ == '__main__':
    from flatcam.__main__ import main
    main()

