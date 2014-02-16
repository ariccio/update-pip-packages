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
        cmd = "%s %s" % (cmd, dist_name)
    print('#',cmd)
    exit_status = os.system(cmd)
    print('Exit status: ', os.system(cmd))
    if exit_status != '0':
        while exit_status != '0':
            with open("C:\\Users\\Alexander Riccio\\pip\\pip.log", 'r') as f:
                print('parsing logfile...')
                line = ''
                for aLine in f.readlines():
                    if 'DistributionNotFound: No distributions at all found for ' in aLine:
                        line = aLine
                    #if 'error: Could not find \'' in aLine:
                        
            try:
                endName = line.rfind(' in ')
                theBadPackage = line[56:endName]
                
            except ValueError:
                print('ValueError!')
                return
            if  theBadPackage == '':
                return
            cmd = "C:\python%i%i\scripts\pip install -U " % (sys.version_info.major, sys.version_info.minor)
            for dist_name in dists:
                if dist_name != theBadPackage:
                    print(dist_name, ' is not ', theBadPackage)
                    cmd = "%s %s" % (cmd, dist_name)
                else:
                    print('removing bad dist_name "', dist_name, '"')
                    dists.remove(dist_name)

            print('#',cmd)
            exit_status = os.system(cmd)
            print('Exit status: ', os.system(cmd))


def updatePip():
    dists = []

    for dist in pip.get_installed_distributions():
        dists.append(dist.project_name)

    dists = sorted(dists, key=lambda s: s.lower())
    dists.insert(0, 'pip')  # let 'pip' be the first

    #cmd = "C:\python27\scripts\pip install -U "

    ##for dist_name in dists:
    ##
    ##    cmd = "%s %s" %(cmd, dist_name)
    ##    #print('#', cmd)
    ##    #os.system(cmd)
    ##
    ###os.system(cmd)

    if 'linux' in sys.platform:
        linuxPip(dists)
        
    elif ('win32' or 'win64') in sys.platform:    
        windowsPip(dists)

def main():
    updatePip()    
    ##for dist_name in dists:
    ##    if 'linux' in sys.platform:
    ##        cmd = "sudo pip install {0} -U".format(dist_name)
    ##        print('#', cmd)
    ##        os.system(cmd)
    ##    elif ('win32' or 'win64') in sys.platform:
    ##        cmd = "C:\python27\scripts\pip install {0} -U".format(dist_name)
    ##        print('#', cmd)
    ##        os.system(cmd)
            
if __name__ == '__main__':
    main()
