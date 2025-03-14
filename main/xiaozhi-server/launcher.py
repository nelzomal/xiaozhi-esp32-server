#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import shutil
import sys


def copy_directory(src, dst):
    """
    Recursively copy a directory from src to dst.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.isdir(src_item):
            copy_directory(src_item, dst_item)
        else:
            if not os.path.exists(dst_item):
                shutil.copy2(src_item, dst_item)


def main():
    """
    Launcher script for the PyInstaller-bundled application.
    This script ensures that all necessary files and directories are available in the current working directory.
    """
    # Check if running in a PyInstaller bundle
    if getattr(sys, "frozen", False):
        # Get the directory where the executable is located
        bundle_dir = sys._MEIPASS

        # List of files to copy from bundle to current directory
        files_to_copy = [
            "config.yaml",
        ]

        # List of directories to copy from bundle to current directory
        dirs_to_copy = [
            "models",
            "core",
            "config",
        ]

        # Copy individual files
        for file_name in files_to_copy:
            bundled_file = os.path.join(bundle_dir, file_name)
            local_file = os.path.join(os.getcwd(), file_name)

            if not os.path.exists(local_file) and os.path.exists(bundled_file):
                print(f"Copying {file_name} to {os.getcwd()}")
                shutil.copy2(bundled_file, local_file)

        # Copy directories
        for dir_name in dirs_to_copy:
            bundled_dir = os.path.join(bundle_dir, dir_name)
            local_dir = os.path.join(os.getcwd(), dir_name)

            if not os.path.exists(local_dir) and os.path.exists(bundled_dir):
                print(f"Copying {dir_name} directory to {os.getcwd()}")
                copy_directory(bundled_dir, local_dir)

        # Create tmp and data directories if they don't exist
        tmp_dir = os.path.join(os.getcwd(), "tmp")
        data_dir = os.path.join(os.getcwd(), "data")

        if not os.path.exists(tmp_dir):
            print(f"Creating tmp directory at {tmp_dir}")
            os.makedirs(tmp_dir, exist_ok=True)

        if not os.path.exists(data_dir):
            print(f"Creating data directory at {data_dir}")
            os.makedirs(data_dir, exist_ok=True)

    # Import app module
    import app

    # Run the main function from app.py
    try:
        asyncio.run(app.main())
    except KeyboardInterrupt:
        print("手动中断，程序终止。")


if __name__ == "__main__":
    main()
