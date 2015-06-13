#!/usr/bin/env python

"""Delete some files created by mac systems, like .DS_Store, ._whatever"""

import os
import re
import shutil
import sys

del_match = re.compile(r'\..+')

def main():
    dir = os.curdir
    for dirpath, dirnames, filenames in os.walk(dir):
        for d in dirnames:
            if del_match.match(d):
                print 'Deleting -> %s/%s' % (dirpath, d)
                shutil.rmtree('%s/%s' % (dirpath, d))
        for f in filenames:
            if del_match.match(f):
                print 'Deleting -> %s/%s' % (dirpath, f)
                os.remove('%s/%s' % (dirpath, f))
        
if __name__ == '__main__':
    #Just call the program in the website root directory."
    main()
