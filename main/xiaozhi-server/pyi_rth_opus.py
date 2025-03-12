import ctypes
import os
import sys


def patch_opuslib():
    """Patch opuslib_next to use our bundled library"""
    if hasattr(sys, "_MEIPASS"):
        lib_paths = [
            os.path.join(sys._MEIPASS, "libopus.dylib"),
            os.path.join(sys._MEIPASS, "libopus.0.dylib"),
        ]

        # Find the first available library
        for lib_path in lib_paths:
            if os.path.exists(lib_path):
                try:
                    # Load the library first
                    opus_lib = ctypes.CDLL(lib_path)

                    # Now patch opuslib_next
                    import opuslib_next.api

                    opuslib_next.api._lib = opus_lib
                    return True
                except Exception as e:
                    print(f"Failed to load {lib_path}: {e}")
                    continue
    return False


# Try to patch after imports
success = patch_opuslib()
if not success:
    print("Warning: Failed to patch opuslib_next library loading")
