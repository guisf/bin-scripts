#!/usr/bin/python2

import BeautifulSoup as bs
import sys

try:
    fin = open(sys.argv[1])
    data = fin.read()
    fin.close()
    fout = open(sys.argv[1], 'w')
    soup = bs.BeautifulSoup(data)
    fout.write(soup.prettify())
    fout.close()
except:
    print "usage: %s file.html" % sys.argv[0]
    sys.exit(1)
    
