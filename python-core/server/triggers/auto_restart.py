# ---------------------------------------------------------------------------
#           Name: auto_restart.py
#        Authors: Groentjuh
#  Last Modified: 20/12/2011
#    Description: Server Trigger for automatic Server Restarts, every hour it idles.
# ---------------------------------------------------------------------------

# Savage API
import core
import server


# -------------------------------
def check():
    # Check that server is idle and the game time is over 1h.
    if server.GetGameInfo(GAME_STATE) == 0 and server.GetGameInfo(GAME_TIME) > 3600000:
        return 1
    return 0


# -------------------------------
def execute():
    # Restart the server
    core.CommandExec('quit')
    pass
