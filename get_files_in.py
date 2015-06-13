#!/usr/bin/python

import os
import sys
import random

list_of_files = []

def append(extension, dirname, fnames):
    extension = extension.lower().strip('.')
    list_of_files.extend([os.path.join(dirname, x) 
                for x in fnames if x.lower().endswith(extension)])

def find_files(path, extension):
    os.path.walk(path, append, extension)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print '%s path .ext' % sys.argv[0]
        sys.exit(1)
    if not sys.argv[1].startswith('/'):
        sys.argv[1] = os.path.join(os.getcwd(), sys.argv[1])
    find_files(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3] == '-s':
        random.shuffle(list_of_files)
    else:
        list_of_files.sort()
    print '\n'.join(list_of_files)
