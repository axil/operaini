import re
KEY = '____________________________'
fin = open('standard_toolbar.ini')
fout = open('canonic.ini', 'wt')
fout.write('[Header&!!%@#$@#$]\n')
for line in fin:
    if ( re.match('\[[^]]+\]\s*$', line) or
         re.match('\s*$', line) or
         line[0] == ';' or
         '=' in line):
        fout.write(line)
    else:
        fout.write(line.strip() + '="'+ KEY +'"\n')
fout.close()

