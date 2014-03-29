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
import subprocess

def getInstalledPackages():
    dists = []
#    failed = []
    for dist in pip.get_installed_distributions():
        dists.append(dist.project_name)

    dists = sorted(dists, key=lambda s: s.lower())
    dists.insert(0, 'pip')  # let 'pip' be the first
    return dists

##    try:
##        outputDict[aPackage.project_name] = [subprocess.check_output("C:\\Python27\\Scripts\\pip.exe install -U %s" % (aPackage.project_name) )]
##        print outputDict[aPackage.project_name]
##    except subprocess.CalledProcessError as aCalledProcessError:
##        outputDict[aPackage.project_name] = [aCalledProcessError.cmd, aCalledProcessError.output, aCalledProcessError.returncode]
##        print outputDict[aPackage.project_name]



def linuxPip(dists):
    failed = []
    cmd = "sudo pip install -U "
    for dist_name in dists:
        cmd = "%s %s" % (cmd, dist_name)
        print('#', dists.index(dist_name),cmd)
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as aCalledProcessError:
            print('\tCalledProcessError! ', aCalledProcessError.cmd, aCalledProcessError.output, aCalledProcessError.returncode)
    return failed

def windowsPip(dists):
    failed = []
    cmd = "C:\python%i%i\scripts\pip install -U " % (sys.version_info.major, sys.version_info.minor)
    for dist_name in dists:
        this_cmd = "%s %s" % (cmd, dist_name)
        print('#', dists.index(dist_name), this_cmd)
        try:
            exit_status = subprocess.check_output(this_cmd)
        except subprocess.CalledProcessError as aCalledProcessError:
            if aCalledProcessError.returncode == 1:
                #package is already up to date!
                print("\tPackage %s is already up to date!" % dist_name)
            else:    
                print('\tCalledProcessError! ')
                failed.append((dist_name, aCalledProcessError.cmd, aCalledProcessError.output, aCalledProcessError.returncode))
##        print('Exit status: ', os.system(this_cmd))
##        if exit_status != 0:
##            failed.append((dist_name, exit_status))
    return failed

def getTroubleMakingPackages():
    badPackageFileNameDir = os.getcwdu()
    badPackageFileName = '%s%s%s' % (badPackageFileNameDir, os.sep, 'pip_update_known_troublemakers')
    dictNames = {}
    with open(badPackageFileName, 'r') as f:
        for line in f:
            theName = line[:-1]
            dictNames[theName] = True
    listNames = []
    for aName in dictNames.keys():
        listNames.append(dictNames[aName])
    return listNames

def updatePip():
    failed = []
    badPackages = []
    dists = getInstalledPackages()
    print('Got list of %i installed packages! Continue?' % len(dists))
    if sys.version_info.major > 2:
        input()
    else:
        raw_input()

    if 'linux' in sys.platform:
        failed = linuxPip(dists)
        
    elif ('win32' or 'win64') in sys.platform:    
        failed = windowsPip(dists)
    if len(failed) > 1:
        print('---------------------------------------------------')
        print('Failures occured while upgrading all packages:')
        for dist_name, cmd, output, returncode in failed:
            print('Failed upgrade of package: ', dist_name)
            print('\tFailing command:         ', cmd)
            print('\tOutput of command:       ', output)
            print('\tReturn code of command:  ', returncode)
        badPackageFileNameDir = os.getcwdu()
        badPackageFileName = '%s%s%s' % (badPackageFileNameDir, os.sep, 'pip_update_known_troublemakers')
        with open(badPackageFileName, 'a') as f:
            for items in failed:
                dist_name, _, _2, _3 = items
                f.write('%s\n' %(dist_name))
def main():
    updatePip()    
            
if __name__ == '__main__':
    main()
