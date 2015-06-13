#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""ls wrapper to print two side pages in normal printer.
You specify the start and end pages, and the program generate the apropriate
page range.

guisf, 2009-10-10"""

import optparse

usage='%prog -b start -e end [-o lpoptions] file'
parser = optparse.OptionParser(usage=usage)
parser.add_option("-b", "--begin", dest="begin", action="store", type="int",
                    help="start page")
parser.add_option("-e", "--end", dest="end", action="store", type="int",
                    help="final page")
parser.add_option("-o", "--options", dest="lpopt", action="store", default="",
                    help="string with lp options")
options, args = parser.parse_args()

if not (options.begin and options.end):
    parser.error("-b and -e options are required.")
if len(args) != 1:
    parser.error("One file to print is expected.")

pag = ",".join([str(i) for i in range(options.begin, options.end, 2)])
cmd = "lp -P %s %s %s" % (pag, options.lpopt, args[0])
print cmd

