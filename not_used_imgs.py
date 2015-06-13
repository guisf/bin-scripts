#!/usr/bin/env python

"""Find what images are not being used in CSS and HTML files.

by guisf on 2010-09-27

"""

import os
import re
import optparse
import sys

img_ext = re.compile(r'.+\.(jpg|png|gif)$', re.I)
html_ext = re.compile(r'.+\.(html|htm)$', re.I)

def main(img_dir, css_files, html_dir, move=False):
    """Print list of not used images inside css_files and html templates
    inside html_dir.
    
    """
    
    used = []

    # get all images
    imgs = []
    for root, dir, files in os.walk(img_dir):
        for file in files:
            if img_ext.match(file):
                imgs.append(os.path.join(root, file))

    # find images in css files
    for f in css_files:
        data = open(f).read()
        for img in imgs:
            patt = r'url(.*%s.*)' % img
            if re.search(patt, data, re.I):
                used.append(img)

    # find images in html files
    for root, dir, files in os.walk(html_dir):
        for file in files:
            if html_ext.match(file):
                data = open(os.path.join(root, file)).read()
                for img in imgs:
                    if img not in used:
                        patt = r'<img.*src=.*%s.*' % img
                        if re.search(patt, data, re.I):
                            used.append(img)

    not_used = [img for img in imgs if img not in used]
    not_used.sort()
    print "\n".join(not_used)
    if move:
        move_dir = 'not_used_imgs'
        if not os.path.exists(move_dir):
            os.mkdir(move_dir)
        for img in not_used:
            os.rename(img, os.path.join(move_dir, os.path.basename(img)))
        print '> Unused images moved to direcotry %s' % move_dir


if __name__ == '__main__':
    p = optparse.OptionParser()
    p.add_option('-i', '--img', dest='img_dir', help='Images directory')
    p.add_option('-c', '--css', dest='css_files', action='append', default=[],
                 help='Append CSS file')
    p.add_option('-f', '--html', dest='html_dir', help='HTML directory')
    p.add_option('-m', '--move', dest='move', action='store_true', 
                default=False, help='Move files to a directory')
    opt, args = p.parse_args()
    if opt.img_dir and opt.css_files and opt.html_dir:
        main(opt.img_dir, opt.css_files, opt.html_dir, opt.move)
    else:
        print 'Invalid parameters. See --help.'
        sys.exit(1)

