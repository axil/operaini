import re
KEY = '____________________________'
with open('res.ini') as fin:
    with open('res-final.ini', 'wt') as fout:
        fin.readline()
        for line in fin:
            fout.write(re.sub('="%s"$' % KEY, '', line))

