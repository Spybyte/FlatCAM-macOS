import pkgutil
import sys

# allowed command modules (please append them alphabetically ordered)
import flatcam.tcl.TclCommandAddCircle
import flatcam.tcl.TclCommandAddPolygon
import flatcam.tcl.TclCommandAddPolyline
import flatcam.tcl.TclCommandAddRectangle
import flatcam.tcl.TclCommandAlignDrill
import flatcam.tcl.TclCommandAlignDrillGrid
import flatcam.tcl.TclCommandBbox
import flatcam.tcl.TclCommandBounds
import flatcam.tcl.TclCommandClearShell
import flatcam.tcl.TclCommandCncjob
import flatcam.tcl.TclCommandCopperClear
import flatcam.tcl.TclCommandCutout
import flatcam.tcl.TclCommandDelete
import flatcam.tcl.TclCommandDrillcncjob
import flatcam.tcl.TclCommandExportDXF
import flatcam.tcl.TclCommandExportExcellon
import flatcam.tcl.TclCommandExportGerber
import flatcam.tcl.TclCommandExportGcode
import flatcam.tcl.TclCommandExportSVG
import flatcam.tcl.TclCommandExteriors
import flatcam.tcl.TclCommandGeoCutout
import flatcam.tcl.TclCommandGeoUnion
import flatcam.tcl.TclCommandGetNames
import flatcam.tcl.TclCommandGetPath
import flatcam.tcl.TclCommandGetSys
import flatcam.tcl.TclCommandHelp
import flatcam.tcl.TclCommandInteriors
import flatcam.tcl.TclCommandIsolate
import flatcam.tcl.TclCommandFollow
import flatcam.tcl.TclCommandJoinExcellon
import flatcam.tcl.TclCommandJoinGeometry
import flatcam.tcl.TclCommandListSys
import flatcam.tcl.TclCommandMillDrills
import flatcam.tcl.TclCommandMillSlots
import flatcam.tcl.TclCommandMirror
import flatcam.tcl.TclCommandNew
import flatcam.tcl.TclCommandNregions
import flatcam.tcl.TclCommandNewExcellon
import flatcam.tcl.TclCommandNewGeometry
import flatcam.tcl.TclCommandNewGerber
import flatcam.tcl.TclCommandOffset
import flatcam.tcl.TclCommandOpenDXF
import flatcam.tcl.TclCommandOpenExcellon
import flatcam.tcl.TclCommandOpenFolder
import flatcam.tcl.TclCommandOpenGCode
import flatcam.tcl.TclCommandOpenGerber
import flatcam.tcl.TclCommandOpenProject
import flatcam.tcl.TclCommandOpenSVG
import flatcam.tcl.TclCommandOptions
import flatcam.tcl.TclCommandPaint
import flatcam.tcl.TclCommandPanelize
import flatcam.tcl.TclCommandPlotAll
import flatcam.tcl.TclCommandPlotObjects
import flatcam.tcl.TclCommandQuit
import flatcam.tcl.TclCommandSaveProject
import flatcam.tcl.TclCommandSaveSys
import flatcam.tcl.TclCommandScale
import flatcam.tcl.TclCommandSetActive
import flatcam.tcl.TclCommandSetOrigin
import flatcam.tcl.TclCommandSetPath
import flatcam.tcl.TclCommandSetSys
import flatcam.tcl.TclCommandSkew
import flatcam.tcl.TclCommandSplitGeometry
import flatcam.tcl.TclCommandSubtractPoly
import flatcam.tcl.TclCommandSubtractRectangle
import flatcam.tcl.TclCommandVersion
import flatcam.tcl.TclCommandWriteGCode


__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    import importlib
    module = importlib.import_module('flatcam.tcl.' + name)
    __all__.append(name)


def register_all_commands(app, commands):
    """
    Static method which registers all known commands.

    Command should be in directory flatcam/tcl and module should start with TclCommand.
    Class has to follow same name as module.

    :param app: FlatCAMApp
    :param commands: List of commands being updated
    :return: None
    """

    tcl_modules = {k: v for k, v in list(
        sys.modules.items()) if k.startswith('flatcam.tcl.TclCommand')}

    for key, mod in list(tcl_modules.items()):
        if key != 'flatcam.tcl.TclCommand':
            class_name = key.split('.')[-1]
            class_type = getattr(mod, class_name)
            command_instance = class_type(app)

            for alias in command_instance.aliases:
                try:
                    description = command_instance.description
                except AttributeError:
                    description = ''
                commands[alias] = {
                    'fcn': command_instance.execute_wrapper,
                    'help': command_instance.get_decorated_help(),
                    'description': description
                }
