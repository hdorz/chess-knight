"""
Helper function for build_main.ps1 script

This script edits the .spec file so that the executable can access the assets
required for running the game
"""

import os
import sys


def build_data_line(data_directory):
    edited_line = "datas=["
    folders = os.listdir(data_directory)
    for count in range(0, len(folders)):
        edited_line += f"('{data_directory}/{folders[count]}/*','{data_directory}/{folders[count]}')"
        if count < len(folders) - 1:
            edited_line += ", "

    edited_line += "]\n"

    return edited_line


def edit_spec_file(original_file: str, data_directory):
    temp_file = original_file + "_temp"

    with open(original_file, "r") as old_spec_file:
        with open(temp_file, "w") as temp_spec_file:
            lines = old_spec_file.readlines()
            lines[3] = build_data_line(data_directory)
            for line in lines:
                temp_spec_file.write(line)

    os.remove(original_file)
    os.rename(temp_file, original_file)


edit_spec_file(sys.argv[1], sys.argv[2])
