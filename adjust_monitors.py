#!/usr/bin/python
# by guisf

"""Set monitors to use in X environment."""

import subprocess, shlex

#monitors = ['VGA1', 'LVDS1']
#monitors = ['CRT1', 'LVDS']
monitors = ['eDP1', 'DP2']

out = subprocess.check_output(['xrandr', '-q'])
out = out.decode('utf-8')

score = sum([i+1 for i,m in enumerate(monitors) if '%s connected'%m in out])

if score == 2: # just the laptop monitor
    subprocess.call(shlex.split('xrandr --output %s --off' % monitors[0])) 
    subprocess.call(shlex.split('xrandr --output %s --auto' % monitors[1]))
    #subprocess.call(shlex.split('sh /home/gui/.fehbg'))
elif score == 3: # internal + external monitor
    #subprocess.call(shlex.split('''
    #    xrandr --output %s --auto 
    #           --output %s --auto
    #           --right-of %s''' % (monitors[1], monitors[0], monitors[1])))
    subprocess.call(shlex.split('xrandr --output %s --off' % monitors[0]))
    subprocess.call(shlex.split('xrandr --output %s --auto' % monitors[1]))
    subprocess.call(shlex.split('sh /home/gui/.fehbg'))
else:
    subprocess.call(shlex.split('xrandr --output %s --off' % monitors[0])) 
    subprocess.call(shlex.split('xrandr --output %s --auto' % monitors[1]))

