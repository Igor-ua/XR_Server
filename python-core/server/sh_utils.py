# ---------------------------------------------------------------------------
#           Name: sh_utils.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 05/05/2011
#    Description: Shared utils functions
# ---------------------------------------------------------------------------

# Savage API
from core import *
from inspect import *


# Called directly by Silverback (don't mess with this!)
def checkSyntax(Module, Function, Command, nArgs):
    m = __import__(Module)
    f = getattr(m, Function)
    args = getargspec(f)
    total = len(args[0]) if args[0] is not None else 0
    defaults = len(args[3]) if args[3] is not None else 0
    if nArgs in range(total - defaults, total + 1):
        return 1
    else:
        if len(args[0]) == 0:
            syntax = 'Syntax Error, ' + Command + ' takes no arguments\n\n'
        else:
            syntax = 'Syntax Error, use: ' + Command + ''.join(
                ' <' + args[0][i] + '>' for i in range(total - defaults)) + \
                     ''.join(' [' + args[0][i] + ']' for i in range(total - defaults, total)) + '\n\n'
        ConsolePrint(syntax)
        return 0
