"""
Type these into the REPL loop on the serial console if you need to put the system back into
filesystem-write mode on the computer.
"""
import os
os.rename("boot.py", "boot.off.py")
