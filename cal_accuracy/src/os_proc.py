#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def create_directory(directory):

    """
    Create a new directory if no exist
    """

    if os.path.exists(directory):
        print("%s already exists" % (directory))
    else:
        os.makedirs(directory)
        print("create directory %s" % (directory))

def change_directory(directory):

    """
    Change directory
    """

    if os.path.exists(directory):
        os.chdir(directory)
    else:
        print("%s does not exist" % (directory))

def remove_directory(directory, tmp_dir="./tmp/"):

    """
    Remove directory recursively
    """

    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print("remove directory %s" % (directory))
        except:
            if not os.path.exists(tmp_dir):
                create_directory(tmp_dir)
            shutil.move(directory, tmp_dir)
    else:
        print("%s does not exist" % (directory))

def get_basename(full_path):

    """
    return base name of dir/filename
    """

    return os.path.basename(full_path)

if __name__ == "__main__":

    """
    This is for test
    """

    create_directory("./test_dir")
    remove_directory("./test_dir")
    remove_directory("./haha.txt")
