#!/usr/bin/env python

"""
Update all the packages (in alphabetical order)
that you have installed globally with pip
(i.e. with `sudo pip install`).

http://pythonadventures.wordpress.com/2013/05/22/update-all-pip-packages/

Jabba Laci, 2013--2014 (jabba.laci@gmail.com)
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import pip
import sys


def linuxPip(dists):
    cmd = "sudo pip install -U "
    for dist_name in dists:
        cmd = "%s %s" % (cmd, dist_name)
    print('#',cmd)
    os.system(cmd)

def windowsPip(dists):
    cmd = "C:\python%i%i\scripts\pip install -U " % (sys.version_info.major, sys.version_info.minor)
    for dist_name in dists:
        this_cmd = "%s %s" % (cmd, dist_name)
        print('#',this_cmd)
        exit_status = os.system(this_cmd)
        print('Exit status: ', os.system(this_cmd))
        if exit_status != 0:
            failed.append((dist_name, exit_status))

def updatePip():
    dists = []
    failed = []
    for dist in pip.get_installed_distributions():
        dists.append(dist.project_name)

    dists = sorted(dists, key=lambda s: s.lower())
    dists.insert(0, 'pip')  # let 'pip' be the first

    #cmd = "C:\python27\scripts\pip install -U "
    
    if 'linux' in sys.platform:
        linuxPip(dists)
        
    elif ('win32' or 'win64') in sys.platform:    
        windowsPip(dists)
    print(failed)
    
def main():
    updatePip()    
            
if __name__ == '__main__':
    main()
