# ---------------------------------------------------------------------------
#           Name: sv_custom.py
#           Description: Entry point to run custom scripts on the xr server
# ---------------------------------------------------------------------------


# External modules
import cmd_converter
import sv_custom_utils


def init():
    print("[!]   Initializing Custom Module...")
    try:
        cmd_converter.init()
    except:
        sv_custom_utils.simple_exception_info()
