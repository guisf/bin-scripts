#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Search for files and directories matching the given patterns.

see --help option

guisf, 2009-11-02
"""

import os
import re
import optparse

from lib import filenames


class Search(object):
    """Search for files and directories whose names match the given
    patterns. If self.recursive = True, the search will be recursive.
    The search is case insensitive.
    """

    def __init__(self, paths, patterns, recursive):
        """
        paths: list of paths
        patterns: list of regex, 
        recursive: True/False
        """
        self.paths = paths
        self.regex = [re.compile(p, re.U | re.I) for p in patterns]
        self.recursive = recursive
        self.results = []

    def search(self):
        """Search for files and directories."""
        for path in self.paths:
            if os.path.isdir(path):
                if self.recursive:
                    for root, dirs, files in os.walk(path):
                        dirs.extend(files)
                        for x in dirs:
                            self.score(root, x, self.results)
                else:
                    self.score('', path, self.results)
            else:
                self.score('', path, self.results)

    def score(self, root, name, list):
        """Pontuate the paths that matches something."""
        score = 0
        for regex in self.regex:
            if regex.search(name):
                score += 1
        if score:
            self.results.append([os.path.join(root, name), score])

    def sort(self):
        """Sort the paths by pontuation score."""
        self.results.sort(lambda a, b: cmp(b[1], a[1]))

    def get_results(self):
        return [path for path, score in self.results]


if __name__ == '__main__':
    usage = """\
%prog [-p pattern] [-w word] <paths>

Only one of the options are obrigatory, -p or -w, but you can set both and
you can also set multiple options for each type."""
    desc = """\
Find all paths matching the giving 'patterns' or 'words'.
The words (-w) have all non ASCII characters replaced or stripped.
The patterns (-p) is used as a regular expression.
The search is made in the list of 'paths' passed, and the default is to look
recursively. Set -r option to diseable recursion.
Note that you can set multiple options for -p and -w."""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-p', '--pattern', dest='pattern', action='append',
                        default=[], help='define regex pattern (multiple)')
    parser.add_option('-w', '--word', dest='word', action='append',
                        default=[], help='define word (multiple)')
    parser.add_option('-r', '--recursive', dest='recursive', default=True,
                        action='store_false', help='Diseable recursion.')
    parser.add_option('-c', '--codec', dest='codec', default='utf-8',
                        action='store', help='define codec (default=utf-8)')
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        parser.exit()
    if len(options.pattern) + len(options.word) < 1:
        parser.error('Error: No patterns or words specified.')
    patterns = [filenames.beautify(w, options.codec.lower()) 
                    for w in options.word]
    patterns.extend(options.pattern)
    s = Search(args, patterns, options.recursive)
    s.search()
    s.sort()
    for i, path in enumerate(s.get_results()):
        print "\n%4i => %s" % (i+1, path)
    print
