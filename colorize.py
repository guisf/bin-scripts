#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Print colorized text in the terminal without using curses
or any other program.

See --help for full explanation.

guisf, 2008-12-24
"""

from optparse import OptionParser
import sys


class Palete:
    """This class only defines a name scope. The classes that wants
    to use color must derive this class and use self.palete dictionary
    to access the colors."""

    formats = {
        ''              : '',
        'Bold'          : '1', 
        'HalfBright'    : '2', 
        'Underscore'    : '4', 
        'Blink'         : '5', 
        'Reverse'       : '7',
        'Hidden'        : '8',
        'Normal'        : '22' 
        }
    foreground = {
        ''              : '',
        'Black'         : '30',
        'Red'           : '31', 
        'Green'         : '32',
        'Yellow'        : '33', 
        'Blue'          : '34', 
        'Magenta'       : '35',
        'Cyan'          : '36', 
        'White'         : '37' 
        }
    background = {
        ''              : '',
        'OnBlack'       : '40',
        'OnRed'         : '41',
        'OnGreen'       : '42',
        'OnYellow'      : '43',
        'OnBlue'        : '44',
        'OnMagenta'     : '45',
        'OnCyan'        : '46',
        'OnWhite'       : '47' 
        }
    palete = {}
    for a, x in formats.items():
        for b, y in foreground.items():
            for c, z in background.items():
                key = '%s%s%s' % (a,b,c)
                if key == '': continue
                palete[key] = [n for n in [x,y,z] if n]


class Color(Palete):
    """Class used to print colorized text."""
    
    base = '\033[%sm%s'
    reset = '\033[0m'

    def __init__(self):
        self.texts = []
        self.colors = []
        self.line_break = False # set to True to break lines
    
    def tint(self, text, list_numbers):
        """Don't use this function, use color()."""
        return self.base % ( ';'.join(list_numbers), text )

    def color(self, text, color_name='', reset=False):
        """Use this function to print colorised text.
        color_name must be in the format: FormatForegroundBackground,
        with the words capitalized."""
        if not color_name:
            color_name = 'Normal'
        elif color_name not in self.palete:
            print "Error: Invalid color name '%s'" % color_name
            sys.exit(1)
        out = self.tint(text, self.palete[color_name])
        if reset: out += self.reset
        return out
    
    def add_text(self, text='', color=''):
        self.texts.append(text)
        self.colors.append(color)

    def __str__(self):
        out = ''
        for text, color in zip(self.texts, self.colors):
            if text:
                out += self.color(text, color)
                if self.line_break:
                    out += '%s%s' % (self.reset, '\n')
        return out + self.reset

    def __repr__(self):
        return self.__str__().replace('\\', '\\\\').replace('[', '\[')


def main():
    usage = 'usage: %prog [option] [text1 color1 text2 color2 ...]'
    parser = OptionParser(usage)
    parser.add_option("-s", "--show", dest="show", action="store_true",
                      help="Show color names.")
    parser.add_option("-c", "--color", dest="color", action="store_true",
                      help="Return colorized text. The arguments "\
                           "must come in pairs, text and color.")
    parser.add_option( "-r", "--repr", dest="string", action="store_true",
                        help="Print the string to generate "\
                             "the colorized text.")
    option, args = parser.parse_args()

    if not option.show and len(args) == 0:
        print 'See --help.'
        sys.exit(0)

    color = Color()
    
    # just show the possible names for colors.
    if option.show:
        out = ''
        for name in reversed(sorted(color.palete.keys())):
            out += "%30s%3s%s\n" % (name, " ", 
                                        color.color(name, name, reset=True))
        print out
    # print colorized text or its literal string representation
    elif option.color or option.string:
        for i in range(0, len(args), 2):
            color.add_text(args[i], args[i+1])
        if option.color:
            print color
        else:
            print repr(color)
    # unknown option
    else:
        print "See --help."
        sys.exit(1)


if __name__ == '__main__':
    main()

