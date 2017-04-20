# This Python file uses the following encoding: utf-8

import os
import sys
import os.path
import json
from os import listdir
from os.path import isfile, join

# Set up stat file if it doesn't exist already
if os.path.isfile('stats.json') is not True:
    data = {}  
    data['index'] = '100'
    data['size_gb'] = '0'
    data['duration'] = '0:00' 

    with open('stats.json', 'w') as outfile:
        json.dump(data, outfile)

if os.path.isfile('config.json') is not True:
    data = {}
    data['file_path'] = '/'
    data['archive_path'] = '/archive/'
    data['files_kept_in_archive'] = 10

    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)

# Get arguments
args = str(sys.argv)

# Read config
with open('config.json', 'r') as configfile:
    config = json.load(configfile)

FILE_PATH = config['file_path']
FINISHED_PATH = config['archive_path']
FILES_KEPT_IN_ARCHIVE = int(config['files_kept_in_archive'])

if '--upload' in args:
    # Read all files
    files = sorted([f for f in listdir(FILE_PATH) if isfile(join(FILE_PATH, f))]) 

    # Upload all files
    for file in files:

        with open('stats.json', 'r') as statfile:
            stats = json.load(statfile)

        result = os.system('youtube-upload --title=\"%s\" --privacy private %s' % (file, FILE_PATH + file))

        if result == 0:
            stats['index'] = int(stats['index']) + 1
            stats['size_gb'] = float(stats['size_gb']) + float(os.path.getsize(FILE_PATH + file)) / float(1000000000)
            os.rename(FILE_PATH + file, FINISHED_PATH + str(stats['index']) + file)

        with open('stats.json', 'w') as statfile:
            json.dump(stats, statfile)

if '--delete-archived' in args:
    archived_files = sorted([f for f in listdir(FINISHED_PATH) if isfile(join(FINISHED_PATH, f))], reverse = True)

    if len(archived_files) < FILES_KEPT_IN_ARCHIVE:
        print 'No files to remove'
    else:
        for index, file in enumerate(archived_files):
            if index >= FILES_KEPT_IN_ARCHIVE:
                os.remove(FINISHED_PATH + file)
                print 'Removed file: ' + str(file)
