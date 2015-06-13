#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The main purpose of this program is to classify a set of file names 
against a  directory tree. The files will be moved to appropriate directories 
after that.

The words that compose the file name are compared against the names of the 
directory tree. The results are printed to a file.

See --help.

by guisf on 07 Oct 2011

"""

import os
import re
import sys
import optparse

from lib import filenames

# possible words separators
SEP = re.compile(r'[_ .\-/]+')

# use ~/.remove to remove regular expressions from file names
REMOVE_RE = []
remove_file = os.path.join(os.path.expanduser('~'), '.remove')
if os.path.exists(remove_file):
    data = open(remove_file).read().replace('\n', ' ')
    REMOVE_RE = [re.compile(patt, re.I) for patt in data.split() if patt]

# use /~.keywords to match better name in the directory tree
#
# format of the file:
#
# [path1] word1 word2 word3
# [path2] word4 word5
# ....
#
KEYS = {}
keyword_file = os.path.join(os.path.expanduser('~'), '.keywords')
if os.path.exists(keyword_file):
    data = open(keyword_file).read().replace('\n', '')
    sections = [section.strip() for section in data.split('[') if section]
    dir_keys = []
    for s in sections:
        dirname, keywords = s.split(']')
        dirname = dirname.strip().strip('/')
        keywords = [re.compile(word.strip(), re.I) 
                    for word in keywords.split() if word]
        dir_keys.append((dirname, keywords))
    KEYS = dict(dir_keys)
            
def get_dirs(base_path):
    """Get all directories in base_path. Return a dict with the keys
    being the complete directory path and values being a list with the
    elements the relative directory names.
    
    """
    paths = {}
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            a = os.path.join(root, dir)
            b = a.replace(base_path, '')
            paths[a] = SEP.split(b)
    return paths

def find_matches(file_name, paths, base_dir, keywords):
    """
    file_name -> string
    paths -> dict returned by function get_dirs
    base_dir -> base directory passed by -p option
    keywords -> bool

    Return a list containing (score, path) where score is the
    number of times the pattern gets matched.
    
    """
    matched = []
    file_words = SEP.split(file_name)
    for path, words in paths.items():
        score = 0
        # match words against file_name
        for word in words:
            if re.search(word, file_name, re.I):
                score += 1
        # match file_name against words
        for word in file_words:
            if re.search(word, "".join(words), re.I):
                score += 1
        # keyword matches
        if keywords:
            k = path.replace(base_dir, '').strip('/')
            regex = KEYS.get(k)
            if regex:
                for r in regex:
                    if r.search(file_name):
                        score += 1.5
        if score > 0:
            matched.append([score, path])
    # sort by score
    matched.sort(lambda a,b: cmp(b[0], a[0]))
    # return only first 5 results (most relevant)
    return matched[:6]

def filter_string(name):
    """Remove some substring from filename."""
    for r in REMOVE_RE:
        name = r.sub('_', name, re.I)
    return name

if __name__ == '__main__':
    desc = "Try to classify the files matching "\
           "its name against a directory tree."
    usag = "%prog -p path -o output [files]"
    parser = optparse.OptionParser(usage=usag, description=desc)
    parser.add_option('-p', '--path', dest='root', action='store',
                      help='base path containing the directory tree')
    parser.add_option('-o', '--out', dest='output', action='store',
                      help='output file name')
    parser.add_option('-c', '--codec', dest='codec', action='store', 
                      default='utf-8', help='set encoding (default UTF-8)')
    parser.add_option('-k', '--keywords', dest='keyword', action='store_true', 
                      default=False, help='use keyword matching')
    options, args = parser.parse_args()
    
    if len(args) == 0:
        print 'See --help.'
        sys.exit(0)
    
    if not options.root:
        parser.error("-p option is mandatory.")
    else:
        if not os.path.isdir(options.root):
            parser.error("Invalid path: %s." % options.root)
    if not options.output:
        parse.error("-o option is mandatory.")
    
    paths = get_dirs(options.root)
    out = open(options.output, 'w')
    code = options.codec.lower()
    for f in args:
        name = f
        for i in range(2):
            name = os.path.basename(name)
            name1 = filter_string(name)
            name1 = filenames.beautify(name1, code)
        match = find_matches(os.path.splitext(name1)[0], paths, options.root,
            options.keyword)
        dirsopt = [path for score, path in match if score > 0]
        if dirsopt:
            out.write("%s\n" % f)
            out.write("%s/%s" % (dirsopt[0], name))
            out.write("\n\n")
    out.close()

