#!/usr/bin/python

import time
import episode
import os
import shutil
import re

VALID_FILE_EXTENSIONS = ("*.avi", "*.mkv", "*.mpg", "*.mp4", "*.ogm", "*.mov")
CONFIG_FILE = "renamer.cfg"

def parse_config(s):
    """Parse a config file into a dictionary"""
    config_dict = {}
    lines = s.split("\n")
    for line in lines:
        line = line.strip()
        if line and line[0] != "#":
            values = line.split(" ", 1)
            config_dict[values[0]] = values[1].strip()
    return config_dict

# Print load message
print "TV Renaming Script Started"

# Read in the config file
f = file(CONFIG_FILE)
try:
    config_data = f.read()
finally:
    f.close()

config = parse_config(config_data)

# Check files
for root, dirs, files in os.walk(config["path_to_watch"]):
    for extension in VALID_FILE_EXTENSIONS:
        for filename in fnmatch.filter(files, extension):
            old_file_path = os.path.join(root, filename)
            ep = episode.Episode()
            try:
                ep.parse_filename(filename)
                ep.get_episode_name()
    
                new_file_path = os.path.join(config["destination_path"], ep.create_file_path(config["output_format"]))
                new_file_dir = os.path.dirname(new_file_path)
        
                if not os.path.exists(new_file_dir):
                    os.makedirs(new_file_dir)
    
                shutil.move(old_file_path, new_file_path)
            
                print "Moved " + old_file_path + " => " + new_file_path
            except episode.ParserError:
                print "Ignoring unparseable filename (%s)" % filename
            except episode.LookupError:
                print "Error: Couldn't find episode in tv database"
