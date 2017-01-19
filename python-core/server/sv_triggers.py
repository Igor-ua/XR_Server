# ---------------------------------------------------------------------------
#           Name: sv_triggers.py
#         Author: Anthony Beaucamp (aka Mohican)
#    Description: Server Admin Triggers (more info on newerth.com)
#          State: modified
# ---------------------------------------------------------------------------

# Savage API
import core

# External modules
import os
import sys
import imp
import sv_custom_utils

# Global Variables
global fileList
global triggerList


# -------------------------------
def init():

    # Print Console Message
    core.ConsolePrint(' * Initializing Triggers...\n')

    # Custom libs path:
    sys.path.append('python/lib/custom')
    
    # Specify Path to Triggers
    sys.path.append('python/triggers')

    # List all .py modules with prefix 'trigger_'
    global fileList    
    global triggerList
    fileList = [f for f in os.listdir('python/triggers')] 
    fileList = [f for f in fileList if os.path.splitext(f)[1] == '.py']  
    triggerList = list(0 for n in range(0, len(fileList)))
    
    # Try to import each trigger module
    for index in range(0, len(fileList)):
        try:
            triggerList[index] = __import__(os.path.splitext(fileList[index])[0], globals(), locals(), ['check', 'execute'], -1)
            message = "   - Loading %s ...\n" % fileList[index]
            core.ConsolePrint(message)
        except:
            sv_custom_utils.simple_exception_info()

    # Custom module:
    import sv_custom
    sv_custom.init()


# -------------------------------
def re_load():

    # Reload all trigger modules
    for index in range(0, len(triggerList)):
        try:
            imp.reload(triggerList[index])
        except:
            sv_custom_utils.simple_exception_info()


# -------------------------------
def frame():

    # Check all trigger modules
    for index in range(0, len(triggerList)):
        try:
            if triggerList[index].check():
                triggerList[index].execute()
        except:
            sv_custom_utils.simple_exception_info()

