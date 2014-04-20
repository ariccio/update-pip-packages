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
import threading
import optparse

try:
    import queue
except ImportError:
    import Queue as queue

class installerThread(threading.Thread):
    def __init__(self, queueOfPackagesToUpdate, queueOfFailedPackages):
        threading.Thread.__init__(self)
        self.__queueOfPackagesToUpdate = queueOfPackagesToUpdate
        self.__queueOfFailedPackages   = queueOfFailedPackages
    def run(self):
        '''Thread begins executing this function on call to aThreadObject.start().'''
        try:
            self.__nextPackage = self.__queueOfPackagesToUpdate.get_nowait()
        except queue.Empty:
            return
        while self.__nextPackage:
            self.__result = installSinglePackage(self.__nextPackage)
            if self.__result != 0:
                self.__queueOfFailedPackages.put(self.__result)
            try:
                self.__nextPackage = self.__queueOfPackagesToUpdate.get_nowait()
            except queue.Empty:
                return
            
def getInstalledPackages():
    dists = []
#    failed = []
    for dist in pip.get_installed_distributions():
        dists.append(dist.project_name)

    dists = sorted(dists, key=lambda s: s.lower())
    dists.insert(0, 'pip')  # let 'pip' be the first
    return dists

def buildDictOfInstalledPackages():
    dists = {}
    for dist in pip.get_installed_distributions():
        dists[dist.project_name] = dist
    return dists

def buildQueueOfInstalledPackages():
    distQueue = queue.Queue()
    for dist in pip.get_installed_distributions():
        distQueue.put(dist)
    return distQueue

def installSinglePackage(aPackage):
    '''calls the right function (depending on the current OS) to install a single package. Massive function call overhead!'''
    if 'linux' in sys.platform:
        return safeLinuxPip(aPackage)
        
    elif ('win32' or 'win64') in sys.platform:    
        return safeWindowsPip(aPackage)





def safeLinuxPip(dist_name):
    failed = []
    cmd = "sudo pip install -U "
    cmd = "%s %s" % (cmd, dist_name)
    print(cmd)
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as aCalledProcessError:
        print('\tCalledProcessError! ', aCalledProcessError.cmd, aCalledProcessError.output, aCalledProcessError.returncode)
    return failed

def safeWindowsPip(dist_name):
    failed = []
    cmd = "C:\python%i%i\scripts\pip install -U " % (sys.version_info.major, sys.version_info.minor)    
    this_cmd = "%s %s" % (cmd, dist_name)
    print(this_cmd)
    try:
        exit_status = subprocess.check_output(this_cmd)
    except subprocess.CalledProcessError as aCalledProcessError:
        if aCalledProcessError.returncode == 1:
            #package is already up to date!
            print("\tPackage %s is already up to date!" % dist_name)
        else:    
            print('\tCalledProcessError! ')
            failed.append((dist_name, aCalledProcessError.cmd, aCalledProcessError.output, aCalledProcessError.returncode))
    return failed












    
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
    threads = []
    dists = getInstalledPackages()
    print('Got list of %i installed packages! Continue?' % len(dists))
    if sys.version_info.major > 2:
        input()
    else:
        raw_input()
##
##    if 'linux' in sys.platform:
##        failed = linuxPip(dists)
##        
##    elif ('win32' or 'win64') in sys.platform:    
##        failed = windowsPip(dists)
##    if len(failed) > 1:
##        print('---------------------------------------------------')
##        print('Failures occured while upgrading all packages:')
##        for dist_name, cmd, output, returncode in failed:
##            print('Failed upgrade of package: ', dist_name)
##            print('\tFailing command:         ', cmd)
##            print('\tOutput of command:       ', output)
##            print('\tReturn code of command:  ', returncode)
##        badPackageFileNameDir = os.getcwdu()
##        badPackageFileName = '%s%s%s' % (badPackageFileNameDir, os.sep, 'pip_update_known_troublemakers')
##        with open(badPackageFileName, 'a') as f:
##            for items in failed:
##                dist_name, _, _2, _3 = items
##                f.write('%s\n' %(dist_name))
    try:
        queueOfPackagesToUpdate = buildQueueOfInstalledPackages()
        queueOfFailedPackages   = queue.Queue()
        if sys.version_info.major == 3 and sys.version_info.minor > 3:
            numCPUs = os.cpu_count()
        else:
            numCPUs = 8
        [threads.append(installerThread(queueOfPackagesToUpdate, queueOfFailedPackages)) for _ in range(numCPUs)]    
        for thread in threads:
            thread.start()
    except KeyboardInterrupt:
        sys.exit()

def _profile(continuation):
    prof_file = 'duplicateFileFinder.prof'
    try:
        import cProfile
        import pstats
        print('Profiling using cProfile')
        cProfile.runctx('continuation()', globals(), locals(), prof_file)
        stats = pstats.Stats(prof_file)
    except ImportError:
        import hotshot
        import hotshot.stats
        prof = hotshot.Profile(prof_file, lineevents=1)
        print('Profiling using hotshot')
        prof.runcall(continuation)
        prof.close()
        stats = hotshot.stats.load(prof_file)
    stats.strip_dirs()
    #for a in ['calls', 'cumtime', 'cumulative', 'ncalls', 'time', 'tottime']:
    for a in ['cumtime', 'time', 'ncalls']:
        try:
            stats.sort_stats(a)
            stats.print_stats(150)
            stats.print_callees(150)
            stats.print_callers(150)
        except KeyError:
            pass
    os.remove(prof_file)

        
def main():
    parser = optparse.OptionParser("usage: %prog [options] target")
    parser.add_option('--profile', action='store_true', dest='profile', default=False, help="for the hackers")
    (values, args) = parser.parse_args()
    if values.profile:
        print("ready to profile...")
        _profile(updatePip)
    else:
        updatePip()    
            
if __name__ == '__main__':
    main()
