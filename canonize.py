import re

FIN = 'standard_mouse.ini'
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

