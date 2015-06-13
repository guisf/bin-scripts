#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The program renames (recursively) all the files and directories.
The files are renamed removing spaces, non ascii characters and ponctuation
marks. Special rules can be applied to specific file types.

See --help.

guisf, 2009-10-29, <guifranca@gmail.com>
"""

import os
import sys
import optparse
import re
import functools
import string
import unicodedata

ALLOWED_CHARS = u"%s%s_" % (string.lowercase, string.digits)
EXTRA_UNDERSCORES = re.compile(r'_+', re.UNICODE)
EXTRA_SPACES = re.compile(r'\s+', re.UNICODE)
NOT_ALLOWED_CHARS = re.compile(r'[^%s]' % ALLOWED_CHARS, re.UNICODE)

def remove_accents(name, code='utf-8'):
    """>>> remove_accents('pé de pano na calçada')
    u'pe de pano na calcada'
    """
    if not isinstance(name, unicode):
        name = unicode(name, code, 'ignore')
    nkfd_form = unicodedata.normalize('NFKD', name)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])

def beautify(name, code='utf-8'):
    """This function is used to change the file name, removing unwanted
    characters.
    >>> beautify('ola grande (coisa) & nada ** de mais.TXT')
    u'ola_grande_coisa_nada_de_mais.txt'
    """
    new, ext = os.path.splitext(name)
    ext = ext.lower()
    new = remove_accents(new, code).lower() # replace accented chars
    new = EXTRA_SPACES.sub('_', new) # replace extra spaces
    new = NOT_ALLOWED_CHARS.sub('_', new) # replace unwanted
    new = EXTRA_UNDERSCORES.sub('_', new) # remove possible extra _
    new = new.strip('_') # strip _ from both ends
    return "%s%s" % (new, ext)

def move(old, new):
    """Rename file taking care of overwriting: file_1.txt, file_2.pdf, ...
    return a tuple (old_name, new_name).
    """
    if old == new:
        return old, new
    root, ext = os.path.splitext(new)
    i = 1
    while os.path.exists(new):
        new = "%s_%i%s" % (root, i, ext)
        i += 1
    os.rename(old, new)
    return old, new

def fix_names_inside(dir, beauty):
    """Return a list of tuples (old_name, new_name) to be renamed.
    beauty is a callable function to be applied in each file and directory.
    """
    paths = []
    for root, dirs, files in os.walk(dir):
        base_dir = os.sep.join([beauty(d) for d in root.split(os.sep)])
        for item in dirs + files:
            paths.append((os.path.join(base_dir, item), 
                          os.path.join(base_dir, beauty(item))))
    return paths

if __name__ == '__main__':
    u = "%prog [options] <paths>"
    d = "Rename all paths passed as argument, removing non ASCII characters, "\
        "ponctuation characters and spaces. Convert everything to lowercase."
    parser = optparse.OptionParser(usage=u, description=d)
    parser.add_option('-r', '--recursive', action='store_true', default=False,
            dest='recursive', help='Rename files and dirs recursively.')
    parser.add_option('-c', '--codec', action='store', default='utf-8',
            dest='codec', help='Set encoding (default utf-8).')
    options, args = parser.parse_args()
    if len(args) == 0:
        print 'See --help.'
        sys.exit(1)
    codec = options.codec.lower()
    beauty = functools.partial(beautify, code=codec)
    for path in args:
        name = path.rstrip(os.sep).decode(codec)
        newname = beauty(name)
        old, new = move(name, newname)
        print "%s\n%s\n" % (old, new)
        if options.recursive and os.path.isdir(new):
            for oldname, newname in fix_names_inside(new, beauty):
                old, new = move(oldname, newname)
                print "%s\n%s\n" % (old, new)
