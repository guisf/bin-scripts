#!/usr/bin/python2

"""Eliminate extra spaces, comments, line breaks to optimize css files."""

import re

lines = re.compile(r'(\r\n|\n)')
comments = re.compile(r'/\*.*?\*/')
rbrack = re.compile(r' *} *')
lbrack = re.compile(r' *{ *')
spaces = re.compile(r' +')

def css_optimizer(css_text):
    o = lines.sub('', css_text)
    o = comments.sub('', o)
    o = rbrack.sub(' } ', o)
    o = lbrack.sub(' { ', o)
    o = spaces.sub(' ', o)
    return o

if __name__ == '__main__':
    import sys
    if sys.argv[1] == '--help':
        print '%s file.css'
        sys.exit(0)
    try:
        f = open(sys.argv[1])
    except:
        print 'Invalid CSS file.'
        sys.exit(1)

    print css_optimizer(f.read())

