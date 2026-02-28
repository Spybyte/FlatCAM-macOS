# These modules contain test helper functions (with 'self' parameter) designed
# to be called as methods from TclShellTest in test_tcl_shell.py, not as
# standalone pytest tests. Prevent pytest from collecting them directly.
collect_ignore_glob = ["test_TclCommand*.py"]
