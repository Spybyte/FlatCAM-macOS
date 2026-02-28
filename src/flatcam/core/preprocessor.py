# ##########################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# http://flatcam.org                                       #
# File Author: Matthieu Berthomé                           #
# Date: 5/26/2017                                          #
# MIT Licence                                              #
# ##########################################################

from importlib.machinery import SourceFileLoader
import os
from abc import ABCMeta, abstractmethod
import math

# module-root dictionary of preprocessors

import logging

log = logging.getLogger('base')
preprocessors = {}


class ABCPreProcRegister(ABCMeta):
    # handles preprocessors registration on instantiation
    def __new__(cls, clsname, bases, attrs):
        newclass = super(ABCPreProcRegister, cls).__new__(cls, clsname, bases, attrs)
        if object not in bases:
            if newclass.__name__ in preprocessors:
                log.warning('Preprocessor %s has been overriden' % newclass.__name__)
            preprocessors[newclass.__name__] = newclass()  # here is your register function
        return newclass


class PreProc(object, metaclass=ABCPreProcRegister):
    @abstractmethod
    def start_code(self, p):
        pass

    @abstractmethod
    def lift_code(self, p):
        pass

    @abstractmethod
    def down_code(self, p):
        pass

    @abstractmethod
    def toolchange_code(self, p):
        pass

    @abstractmethod
    def up_to_zero_code(self, p):
        pass

    @abstractmethod
    def rapid_code(self, p):
        pass

    @abstractmethod
    def linear_code(self, p):
        pass

    @abstractmethod
    def end_code(self, p):
        pass

    @abstractmethod
    def feedrate_code(self, p):
        pass

    @abstractmethod
    def spindle_code(self, p):
        pass

    @abstractmethod
    def spindle_stop_code(self, p):
        pass


class AppPreProcTools(object, metaclass=ABCPreProcRegister):
    @abstractmethod
    def start_code(self, p):
        pass

    @abstractmethod
    def lift_code(self, p):
        pass

    @abstractmethod
    def down_z_start_code(self, p):
        pass

    @abstractmethod
    def lift_z_dispense_code(self, p):
        pass

    @abstractmethod
    def down_z_stop_code(self, p):
        pass

    @abstractmethod
    def toolchange_code(self, p):
        pass

    @abstractmethod
    def rapid_code(self, p):
        pass

    @abstractmethod
    def linear_code(self, p):
        pass

    @abstractmethod
    def end_code(self, p):
        pass

    @abstractmethod
    def feedrate_xy_code(self, p):
        pass

    @abstractmethod
    def z_feedrate_code(self, p):
        pass

    @abstractmethod
    def feedrate_z_dispense_code(self, p):
        pass

    @abstractmethod
    def spindle_fwd_code(self, p):
        pass

    @abstractmethod
    def spindle_rev_code(self, p):
        pass

    @abstractmethod
    def spindle_off_code(self, p):
        pass

    @abstractmethod
    def dwell_fwd_code(self, p):
        pass

    @abstractmethod
    def dwell_rev_code(self, p):
        pass


def load_preprocessors(app):
    import glob
    import sys
    import importlib
    from pathlib import Path

    # -------------------------------------------------------------------------
    # When running inside a frozen py2app bundle the preprocessor .py files
    # live as compiled .pyc entries inside the application zip (python3XX.zip).
    # glob.glob() cannot see into zip archives, so `SourceFileLoader` won't
    # find anything. In that case we fall back to importlib which *can* import
    # from zip-stored bytecode.
    # -------------------------------------------------------------------------
    if getattr(sys, 'frozen', False):
        import pkgutil
        pkg_name = 'flatcam.preprocessors'
        try:
            pkg = importlib.import_module(pkg_name)
        except ImportError:
            app.log.error("Could not import preprocessors package: %s" % pkg_name)
            return preprocessors

        for importer, modname, ispkg in pkgutil.walk_packages(
                path=pkg.__path__, prefix=pkg.__name__ + '.'):
            try:
                importlib.import_module(modname)
            except Exception as e:
                app.log.error("Failed to load preprocessor %s: %s" % (modname, str(e)))
    else:
        # Normal (non-frozen) loading from .py source files on disk
        _pkg_preprocessors = str(Path(__file__).resolve().parent.parent / 'preprocessors')

        preprocessors_path_search = [
            os.path.join(app.data_path, 'preprocessors', '*.py'),  # user-installed
            os.path.join(_pkg_preprocessors, '*.py'),               # package-bundled
            os.path.join('preprocessors', '*.py')                   # legacy CWD-relative
        ]
        for path_search in preprocessors_path_search:
            for file in glob.glob(path_search):
                try:
                    SourceFileLoader('FlatCAMPostProcessor', file).load_module()
                except Exception as e:
                    app.log.error(str(e))

    return preprocessors
