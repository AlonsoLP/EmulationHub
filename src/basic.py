#! /usr/bin/env python

import os

#
# CONFIG CLASS
#
class Basic:
    ''' Contains Basic Config '''
    NAME = 'EmulationHub'
    VERSION = '0.1'
    URL = 'http://www.'+NAME.lower()+'.com'
    DEVELOPER = 'Alonso Lara'
    DIRECTORIES = [ \
                    os.path.expanduser('~/.')+NAME.lower(), \
                    '/etc/'+NAME.lower(), \
                    '/opt/'+NAME.lower() \
                  ]

    def get_config(self, file):
	''' Return most relevant file (DIRECTORIES[0->n] = high to low prio) '''
	for i in range(len(self.DIRECTORIES)):
	    dirfile = self.DIRECTORIES[i] + '/' + str(file)
	    if os.path.exists(dirfile):
		return(dirfile)

# RUN SOME TESTS
if __name__ == '__main__':
    basic = Basic()
    print '- BASIC INFORMATION:\n  Name:', basic.NAME, \
	  '\n  Version:', basic.VERSION, \
	  '\n  Developer:', basic.DEVELOPER, \
	  '\n  URL:', basic.URL, \
	  '\n  Directories:', basic.DIRECTORIES
    print '- BASIC CLASS DIR:\n  ', dir(basic)
    print '- SEARCHING:\n  .../config/systems.xml'
    tmp = basic.get_config('config/systems.xml')
    if tmp == None:
	print '  .../config/systems.xml does not exists!'
    else:
	print '  ', tmp, 'found!'
    print basic.get_config.__doc__
