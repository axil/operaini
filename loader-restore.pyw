import os
from subprocess import Popen
from iniparse import INIConfig

if __name__ == '__main__':
    filename = 'C:\Documents and Settings\Lev\AppData\Roaming\Opera\Opera 11.6\operaprefs.ini'
    
    with open(filename) as f:
        header = [f.readline() for i in xrange(3)]
        cfg = INIConfig(f)
    
    cfg['User Prefs']['Startup Type'] = '3'
    try:
        del cfg['User Prefs']['Show Startup Dialog']
    except KeyError:
        pass

    with open(filename, 'w') as f:
        f.write(''.join(header) + str(cfg))

    p = Popen('opera.exe', shell=True)


