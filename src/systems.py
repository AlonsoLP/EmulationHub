#! /usr/bin/env python
''' SYSTEMS MODULE '''

import xml.etree.ElementTree

#
# EMULATOR CLASS
#
class Emulator(object):
    ''' EMULATOR CONFIG '''

    def __init__(self, name, command='', extensions=None, config='', active=1):
        self.name = str(name)
        self.command = str(command)
        if extensions is None:
            self.extensions = []
        else:
            self.extensions = extensions
        self.config = str(config)
        self.active = int(active)

    def set_name(self, name):
        ''' SET EMULATOR NAME '''
        self.name = str(name)
    def get_name(self):
        ''' GET EMULATOR NAME '''
        return self.name

    def set_command(self, command):
        ''' SET EMULATOR COMMAND LINE '''
        self.command = str(command)
    def get_command(self):
        ''' GET EMULATOR COMMAND LINE '''
        return self.command

    def set_extensions(self, extensions):
        ''' SET EMULATOR SUPPORTED EXTENSIONS '''
        self.extensions = extensions
    def get_extensions(self):
        ''' GET EMULATOR SUPPORTED EXTENSIONS '''
        return self.extensions

    def set_config(self, config):
        ''' SET EMULATOR CONFIG FILE (IF ANY) '''
        self.config = str(config)
    def get_config(self):
        ''' GET EMULATOR CONFIG FILE (IF ANY) '''
        return self.config

    def set_active(self, active):
        ''' SET EMULATOR ACTIVE (1) OR INACTIVE (0) '''
        if active == 0 or active == 1:
            self.active = int(active)
    def get_active(self):
        ''' SHOW EMULATOR STATUS '''
        return self.active

#
# SYSTEM CLASS
#
class System(object):
    ''' SYSTEM CONFIG '''
    games = 0

    def __init__(self, name, fullname='', active=1, emulators=None):
        self.name = str(name)
        self.fullname = str(fullname)
        if emulators is None:
            self.emulators = []
        else:
            self.emulators = emulators
        self.active = int(active)
        self.games = 0

    def set_name(self, name):
        ''' SET SYSTEM SHORT NAME '''
        self.name = str(name)
    def get_name(self):
        ''' GET SYSTEM SHORT NAME '''
        return self.name

    def set_fullname(self, fullname):
        ''' SET SYSTEM FULL NAME '''
        self.fullname = str(fullname)
    def get_fullname(self):
        ''' GET SYSTEM FULL NAME '''
        return self.fullname

    def set_active(self, active):
        ''' SHOW SYSTEM IF ACTIVE '''
        if (active == 0 or active == 1) and self.active != active:
            if self.active == 0:
                System.games -= self.games
            else:
                System.games += self.games
            self.active = int(active)
    def get_active(self):
        ''' SHOW SYSTEM STATUS '''
        return self.active

#
# SYSTEMS LIST
#
def Systems(xmlfile):
    ''' CREATE SYSTEMS LIST FROM XML FILE '''
    systemslist = []
    tree = xml.etree.ElementTree.parse(xmlfile)
    systemstree = tree.getroot()
    for system in systemstree:
        systemslist.append(System(system.attrib['name'], system.attrib['fullname'], system.attrib['active']))
        emulatorslist = system.find('emulators')
        for emulator in emulatorslist:
            extensionlist = []
            for value in emulator:
                if value.tag == 'extension':
                    extensionlist.append(value.text)
                elif value.tag == 'command':
                    command = value.text
            systemslist[-1].emulators.append(Emulator(emulator.attrib['name'], command, \
                                             extensionlist, '', emulator.attrib['active']))
    return systemslist

#
# ROTATE LIST
#
def rotate(list2rotate, direction):
    ''' SHIFT ARRAY 1-POS TO left OR right '''
    if direction == 'right':
        return list2rotate[1:] + list2rotate[:1]
    elif direction == 'left':
        return list2rotate[-1:] + list2rotate[:-1]
    else:
        return list2rotate

#
# RUN SOME TESTS
#
if __name__ == '__main__':
    systemslist = Systems('config/systems.xml')
    for system in systemslist:
        print system.get_name(), ',', system.get_fullname(), ',',
        if system.get_active() == 1:
            print 'Active',
        else:
            print 'Inactive',
        print '[',
        for emulator in system.emulators:
            print '\n\t(', emulator.get_name(), ', \'' + emulator.get_command() + '\' ,', \
                   emulator.get_extensions(), ',',
            if emulator.get_active() == 1:
                print 'Active',
            else:
                print 'Inactive',
            print ')',
        print '\n]'

