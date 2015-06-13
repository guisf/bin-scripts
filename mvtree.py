#!/usr/bin/env python

"""Move files parsing an archive generated from matchtree.py."""

import os
import re
import sys
import shutil

if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    items = text.split('\n\n')
    i = 1
    to_move = []
    for item in items:
        if item:
            try:
                old, new = item.split('\n')
            except:
                print item
                raise
        else:
            break
        directory = os.path.dirname(new)
        if not os.path.exists(directory):
            print "Error: directory '%s' does not exist. " % directory
            print "Line: %i'" % i
            sys.exit(1)
        to_move.append([old, new])
        i += 3
    i = 1
    for old, new in to_move:
        shutil.move(old, new)
        print "* Moving: %s" % new
        i += 1
    print "Total: %i files moved." % i

