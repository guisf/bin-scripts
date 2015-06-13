#!/usr/bin/python2

"""
Set files and directories permissions.

Sometimes you want to set specific permisions to directories and files,
recursvely. Generaly you need different permissions for directories and files,
and this is the purpose of this program.

guisf, 2009-11-19
"""

import os, sys
import optparse

if __name__ == '__main__':
    usg = "%prog -f file_mode -d dir_mode [paths]"
    dsc = "Set permission for files and directories separatelly."
    parser = optparse.OptionParser(usage=usg, description=dsc)
    parser.add_option('-f', '--file', action='store', dest='fmode',
                        type='int', help='file mode')
    parser.add_option('-d', '--dir', action='store', dest='dmode',
                        type='int', help='dir mode')
    parser.add_option('-r', '--recursive', action='store_true', dest='rec',
                        default=False, help='enable recursion')
    options, args = parser.parse_args()
    
    if len(args) == 0:
        print 'See --help.'
        sys.exit(0)
    if not options.fmode:
        parser.error('-f option is obrigatory.')
    elif not options.dmode:
        parser.error('-d option is obrigatory.')
    
    for arg in args:
        if os.path.isdir(arg):
            os.chmod(arg, options.dmode)
            if options.rec:
                for root, dirs, files in os.walk(arg):
                    for file in files:
                        os.chmod(os.path.join(root, file), options.fmode)
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), options.dmode)
        else:
            os.chmod(arg, options.fmode)

