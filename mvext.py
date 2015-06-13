#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""This program find all files with some wanted extensions inside a given 
directory and move them to another specified directory.
The search is recursive.

The program take care to not overwrite an existing file.

by guisf on 2009-10-29 <guifranca@gmail.com>
"""

import os, sys, optparse

def choose_files(path, files, wanted):
    """Start in 'path' looking recursivelly for all files that have
    extensions contained in the list 'wanted'. Append files to
    the list 'files'.

    'files' - must be a list
    'wanted' - must be a list of file extensions"""
    path = path.rstrip(os.sep)
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lstrip('.').lower()
        if ext in wanted:
            files.append(path)
    elif os.path.isdir(path):
        for item in os.listdir(path):
            choose_files(os.path.join(path, item), files, wanted)

def extensions(path, results):
    """Search in path for extension types and save the number of
    ocurrences in the dict 'results'."""
    path = path.rstrip(os.sep)
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lstrip('.').lower()
        results.setdefault(ext, 0)
        results[ext] += 1
    elif os.path.isdir(path):
        for item in os.listdir(path):
            extensions(os.path.join(path, item), results)

def move(old, new):
    """Rename file checking if an equal path already exists. If it exists
    it rename the file appending an integer like: file_1.txt, file_2.txt.
    This stop the program to overwrite an existing file."""
    if os.path.exists(new):
        count = 1
        root, ext = os.path.splitext(new)
        while True:
            new = "%s_%i%s" % (root, count, ext)
            if os.path.exists(new):
                count += 1
            else:
                break
        os.rename(old, new)
    else:
        os.rename(old, new)


if __name__ == '__main__':
    usage = """\
usage: %prog -i incomming_dir -d destination_dir [extensions]
       %prog -i incomming_dir -l [extensions]
       %prog -i incomming_dir -t
"""
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--incomming', dest='incomming_dir', 
                help='directory containing the files and subdirectories')
    parser.add_option('-d', '--destination', dest='destination_dir',
                help='destination directory where the files will be moved to')
    parser.add_option('-l', '--list', dest='list', action='store_true',
                help='list the files with the given extensions')
    parser.add_option('-t', '--tell', dest='tell', action='store_true',
                help='tell wich file extensions exists')
    options, args = parser.parse_args()
    if not options.tell and len(args) == 0:
        print "See --help."
        sys.exit(1)
    if options.tell:
        results = {}
        if not options.incomming_dir:
            parser.error('-i option required')
        extensions(options.incomming_dir, results)
        for ext, freq in results.items():
            print "[%s] %i file(s)" % (ext, freq)
    else:
        if options.list:
            if not options.incomming_dir:
                parser.error('-i option required')
        else:
            if not options.incomming_dir or not options.destination_dir:
                parser.error("-i and -d options required")
        if len(args) < 1:
            parser.error("no extensions specified")
        files, wanted = [], [ext.strip('.').lower() for ext in args]
        choose_files(options.incomming_dir, files, wanted)
        if options.list:
            for a in files:
                print a
        else:
            dest = options.destination_dir.rstrip(os.sep)
            if not os.path.exists(dest):
                os.mkdir(dest, 0755)
            for a in files:
                move(a, os.path.join(dest, os.path.basename(a)))

