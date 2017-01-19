#---------------------------------------------------------------------------
#           Name: sh_threads.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 28/09/2011
#    Description: Wrapper Class for Threaded Command Calls
#---------------------------------------------------------------------------

import __builtin__

# Python Modules
import threading

# Threads Array
global threads
threads = []

# Thread Class
class Thread(threading.Thread):

    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command
        
    def run(self):
        exec self.command
    
    
#-------------------------------
# Called directly by Silverback
#-------------------------------
def frame():
    pop = []
    
    # Update Threads
    for thread in threads:
        thread.join(0.001)
        if not thread.isAlive():
            pop.append(thread)
    
    # Pop dead Threads
    for thread in pop:
        threads.pop(threads.index(thread))


#-------------------------------
def createThread(command):
    # Create thread object
    t = Thread(command)
    threads.append(t)
    t.start()
    return t

    
# Export some Functions
__builtin__.createThread = createThread
