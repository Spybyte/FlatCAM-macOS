"""
Shared test fixtures for the FlatCAM test suite.

Provides a minimal mock ``app`` object so that parser and geometry classes
(Excellon, Gerber, Geometry …) can be instantiated without a full
PyQt5 App.
"""

import pytest


class _MockSignal:
    """Stub for PyQt5 signals (e.g. app.inform)."""

    def emit(self, *args, **kwargs):
        pass


class _MockProcContainer:
    """Stub for app.proc_container."""

    new_text = ''

    def update_view_text(self, *args, **kwargs):
        pass


class _MockShapeCollection:
    """Stub returned by plotcanvas.new_shape_collection / new_shape_group."""
    pass


class _MockPlotCanvas:
    """Minimal stub used by Geometry.__init__."""

    def new_shape_collection(self, **kwargs):
        return _MockShapeCollection()

    def new_shape_group(self, **kwargs):
        return _MockShapeCollection()

    class view:
        class scene:
            pass


class _FallbackDict(dict):
    """A dict that returns sensible defaults for missing keys."""

    def __missing__(self, key):
        # Return safe zero/false-like defaults for any un-specified key
        return None


class _MockApp:
    """
    Lightweight stand-in for the real ``App`` instance.

    Provides the attributes that ``Geometry.__init__``,
    ``Excellon.__init__``, and ``Gerber.__init__`` access on
    ``self.app``.
    """

    decimals = 4
    is_legacy = False
    plotcanvas = _MockPlotCanvas()
    abort_flag = False
    inform = _MockSignal()
    proc_container = _MockProcContainer()

    defaults = _FallbackDict({
        "units": "MM",
        "decimals_inch": 4,
        "decimals_metric": 4,
        "global_tolerance": 0.005,
        "gerber_circle_steps": 64,
        "gerber_def_zeros": "L",
        "gerber_def_units": "MM",
        "gerber_use_buffer_for_union": True,
        "gerber_simplification": False,
        "gerber_simp_tolerance": 0.0005,
        "gerber_buffering": "full",
    })


@pytest.fixture(autouse=True)
def _set_mock_app(monkeypatch):
    """Inject a mock ``app`` into all classes that need it.

    ``FlatCAMObj.app`` is a **class attribute** that the real application
    sets at startup.  Parser/geometry classes reach it through the MRO.
    For tests that do *not* spin up the full App we patch both
    ``FlatCAMObj`` and ``Geometry`` so that standalone instantiation works.
    """
    mock = _MockApp()

    # Patch FlatCAMObj.app (objects layer)
    try:
        from flatcam.objects.base import FlatCAMObj
        monkeypatch.setattr(FlatCAMObj, "app", mock)
    except Exception:
        pass

    # Patch Geometry.app for direct parser usage (Excellon(), Gerber())
    try:
        from flatcam.cam.camlib import Geometry
        monkeypatch.setattr(Geometry, "app", mock, raising=False)
    except Exception:
        pass

    # Gerber has its own app = None class attribute that shadows Geometry.app
    try:
        from flatcam.parsers.gerber import Gerber
        monkeypatch.setattr(Gerber, "app", mock)
    except Exception:
        pass
