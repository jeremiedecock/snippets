#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os

# GET THE ROOT DIRECTORY ######################################################

parser = argparse.ArgumentParser(description='An os.walk() snippet.')

parser.add_argument("root_dir_args", nargs=1, metavar="DIRECTORY", help="The directory to explore")
args = parser.parse_args()
root_dir = args.root_dir_args[0]

if not os.path.isdir(root_dir):
    print("{0} is not a directory.".format(root_dir))

# WALK THE ROOT DIRECTORY #####################################################

#for cur_dir, dirs, files in os.walk(root_path, topdown=False):
#   # cur_dir = path du répertoire courant dans l'exploration
#   # dirs    = liste des répertoires dans "cur_dir"
#   # files   = liste des fichiers dans "cur_dir"

for cur_dir, dirs, files in os.walk(root_dir, topdown=False):
    for name in files:
        # Print files
        print(os.path.join(cur_dir, name))
    for name in dirs:
        # Print directories
        print(os.path.join(cur_dir, name))
