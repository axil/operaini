import re
from iniparse import INIConfig

def canonize(filename):
    FIN = filename
    FOUT = 'canonic.ini'

    KEY = '____________________________'
    with open(FOUT, 'wt') as fout:
        fout.write('[____________]\n')
        for line in open(FIN):
            if ( re.match('\[[^]]+\]\s*$', line) or
                re.match('\s*$', line) or
                line[0] == ';' or
                '=' in line):
                fout.write(line)
            else:
                fout.write(line.strip() + '="'+ KEY +'"\n')

def decanonize(filename):
    KEY = '____________________________'
    with open('canonic-res.ini') as fin:
        with open(filename, 'wt') as fout:
            fin.readline()
            for line in fin:
                fout.write(re.sub('="%s"$' % KEY, '', line))

def process_mouse():
    canonize('standard_mouse.ini')
    cfg = INIConfig(open('canonic.ini'))
    cfg.Application.GestureDown = 'New browser window'
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize('standard_mouse-res.ini')

def process_keyboard():
    canonize('standard_keyboard.ini')
    cfg = INIConfig(open('canonic.ini'))
    cfg.Application['t ctrl'] = 'Add to bookmarks'
    cfg.Application['PageUp ctrl'] = 'Switch to previous page'
    cfg.Application['PageDown ctrl'] = 'Switch to next page'
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize('standard_keyboard-res.ini')

if __name__ == '__main__':
#    process_mouse()
    process_keyboard()
