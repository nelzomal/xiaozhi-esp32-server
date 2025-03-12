# This hook runs before any imports
import os
import sys

if hasattr(sys, "_MEIPASS"):
    # Set environment variables to help find the library
    os.environ["OPUSLIB_NEXT_LIB"] = os.path.join(sys._MEIPASS, "libopus.dylib")
    os.environ["DYLD_LIBRARY_PATH"] = sys._MEIPASS
    os.environ["LD_LIBRARY_PATH"] = sys._MEIPASS
