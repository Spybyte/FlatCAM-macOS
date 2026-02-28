# FlatCAM-OSX — Copilot Instructions

## Architecture Overview

FlatCAM is a PyQt5 desktop application for PCB manufacturing post-processing. All source lives under `src/flatcam/` as an installable Python package.

**Core data flow:** File parsers (`parsers/`) → Document objects (`objects/`) → CAM toolpath generation (`cam/camlib.py`) → G-Code via preprocessors (`preprocessors/`).

| Layer | Key files | Role |
|-------|-----------|------|
| Entry point | `__main__.py` → `app.py` (10k+ lines) | QApplication bootstrap, central controller (`App` class owns everything) |
| Document objects | `objects/{gerber,excellon,geometry,cnc_job,document,script}.py` | Wrap parsed data + UI; inherit from `objects/base.py` |
| CAM engine | `cam/camlib.py` | Geometry primitives, isolation, paint, G-Code generation (Shapely-heavy) |
| GUI | `gui/main_window.py`, `gui/elements.py`, `gui/object_ui.py` | PyQt5 widgets; canvas via VisPy (`gui/vispy_canvas.py`) or legacy Matplotlib |
| Tools | `tools/*.py` (33 tools) | Each inherits `core/tool_base.py::AppTool`; receives `self.app` reference |
| Tcl commands | `tcl/TclCommand*.py` (67 commands) | Each inherits `tcl/command.py::TclCommand`; defines `aliases`, `arg_names`, `option_types`, `required`, `help` |
| Preprocessors | `preprocessors/*.py` (21 files) | Auto-registered via `ABCPreProcRegister` metaclass in `core/preprocessor.py` |
| Preferences | `defaults.py::FlatCAMDefaults.factory_defaults` | Flat dict with `"section_key"` naming (e.g. `"gerber_circle_steps"`) |

## Developer Commands

```bash
uv sync                          # install core deps
uv sync --extra optimization     # include ortools
uv run flatcam                   # run the app
uv run pytest tests/             # run tests
make bundle                      # build macOS .app (py2app)
make bundle-alias                # fast dev build (symlinks)
```

## Key Conventions

- **i18n boilerplate** — Nearly every module starts with this pattern. Always include it in new files:
  ```python
  import gettext
  from flatcam.core import translation as fcTranslate
  import builtins
  fcTranslate.apply_language('strings')
  if '_' not in builtins.__dict__:
      _ = gettext.gettext
  ```
- **Logging** — Use `log = logging.getLogger('base')` (single logger name throughout the codebase).
- **Imports** — Always use fully-qualified package imports: `from flatcam.gui.elements import FCButton`, never relative imports.
- **`self.app` pattern** — Tools, objects, and editors always receive `app` in their constructor and store it as `self.app`. Access defaults via `self.app.defaults["key"]`, decimal precision via `self.app.decimals`.
- **Single version source** — Version lives in `src/flatcam/__init__.py::__version__`. Both `pyproject.toml` and `setup.py` (py2app plist) read it dynamically.
- **`PROJECT_ROOT`** — Canonical path anchor from `flatcam.__init__.PROJECT_ROOT`. Handles both source runs and frozen py2app bundles.
- **macOS multiprocessing** — `set_start_method('fork')` is forced in `app.py` (required for PyQt5 on macOS 3.8+).
- **Preprocessor registration** — Subclass `PreProc` (from `core/preprocessor.py`) → automatically registered in the global `preprocessors` dict via metaclass. When frozen (py2app), loading uses `pkgutil.walk_packages` instead of `glob`.

## Adding New Components

- **New Tool:** Create `tools/my_tool.py`, subclass `AppTool`, wire it into `app.py`'s tool initialization and menu setup.
- **New Tcl Command:** Create `tcl/TclCommandMyCmd.py`, subclass `TclCommand`, define `aliases`, `arg_names`, `option_types`, `required`, `help` dicts, implement `execute()`. Register via explicit import in `tcl/__init__.py`.
- **New Preprocessor:** Create `preprocessors/my_proc.py`, subclass `PreProc`, implement all abstract methods (`start_code`, `lift_code`, `down_code`, etc.). Registration is automatic.

## Geometry & Dependencies

- All 2D geometry uses **Shapely 2.x** (`Polygon`, `MultiPolygon`, `LineString`, `unary_union`).
- Spatial indexing via **Rtree**. Raster operations via **rasterio**.
- DXF via **ezdxf**, SVG via **svg.path** + **svglib**, G-Code via custom preprocessor templates.
- Optional: **ortools** for toolpath optimization (install via `uv sync --extra optimization`).

## py2app Bundle Notes

- `setup.py` is py2app-only (not used for normal installs). It monkey-patches `finalize_options` to clear `install_requires` (py2app >=0.28.9 rejects it, but setuptools auto-populates from pyproject.toml).
- The `FlatCAM.py` shim at project root is the py2app entry point (`APP = ['FlatCAM.py']`).
- Frozen-app detection: `getattr(sys, 'frozen', False)` — only use where behavior genuinely differs (resource paths, preprocessor loading). Don't add redundant identical-branch checks.
