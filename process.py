from iniparse import INIConfig
with open('canonic.ini') as fin:
    #fin.readline()
    cfg = INIConfig(fin)
    a = cfg['Hotlist.alignment']
    print a['Collapse']
    a['Collapse']=123
    with open('res.ini', 'wt') as fout:
        print >>fout, cfg

