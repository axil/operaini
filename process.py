import re, os
from iniparse import INIConfig
from copy import deepcopy

KEY = '____________________________'

def canonize(filename):
    FIN = filename
    FOUT = 'canonic.ini'

    with open(FOUT, 'wt') as fout:
        fout.write('[' + KEY + ']\n')
        for line in open(FIN):
            if ( re.match('\[[^]]+\]\s*$', line) or
                re.match('\s*$', line) or
                line[0] == ';' or
                '=' in line):
                fout.write(line)
            else:
                fout.write(line.strip() + ' = "'+ KEY +'"\n')

def decanonize(filename):
    os.rename(filename, filename+'.bak')
    with open('canonic-res.ini') as fin:
        with open(filename, 'wt') as fout:
            fin.readline()
            for line in fin:
                fout.write(re.sub(' = "%s"$' % KEY, '', line))

def process_mouse():
    filename = 'ui/standard_mouse.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'))
    cfg.Application.GestureDown = 'New browser window'
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)

def process_keyboard():
    filename = 'ui/standard_keyboard.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'))
    cfg.Application['t ctrl'] = 'Add to bookmarks'
    cfg.Application['PageUp ctrl'] = 'Switch to previous page'
    cfg.Application['PageDown ctrl'] = 'Switch to next page'
#    cfg['Browser Widget']['PageUp shift'] = 'Page left'
#    cfg['Browser Widget']['PageDown shift'] = 'Page right'
#    del cfg['Browser Widget']['PageUp ctrl']
#    del cfg['Browser Widget']['PageDown ctrl']
    cfg['Browser Widget']._lines[-1].find('PageUp ctrl').name='PageUp shift'
    cfg['Browser Widget']._lines[-1].find('PageDown ctrl').name='PageDown shift'
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)

def process_toolbar():
    filename = 'ui/standard_toolbar.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'), optionxformvalue=None)
    
    # ____ hotlist ____
    cfg['Hotlist.alignment'].Collapse = 1
    s1 = cfg['Bookmarks Panel Toolbar.content']
    s2 = deepcopy(s1)
    for v in s1:
        del s1[v]
    i=0
    for v in s2:
        s1[v] = s2[v]
        if i==0:
            s1['Button, -1759909084'] = 'New folder'
        i = i+1 
    
    # ____ address bar ____
    s1 = cfg['Document Toolbar.content']
    del s1['Button, S_WAND_TOOLBAR_BUTTON_TEXT']  # wand combined with fast forward
    s2 = deepcopy(s1)
    for v in s1:
        del s1[v]
    s1['Button, 1409512585'] = '"Rewind + Show popup menu, "Internal Rewind History""'
    for v in s2:
        if not 'HOME_BUTTON' in v and not 'WAND_TOOLBAR_BUTTON' in v:
            s1[v] = s2[v]
        if 'Combined Back Forward' in v:
            s1['Button, -108388079'] = '"Fast Forward + Show popup menu, "Internal Fast Forward History""'
            s1['Button, -1320335960'] = '"Enable display images > Disable display images, , , -383776252 > Display cached images only, , , 333270751 + Show popup menu, "Images And Style Menu""'
        if 'STOP_BUTTON' in v:
            s1['Button, -119414254'] = 'Wand'
        if v.startswith('Address'):
            s1['Button, 870715797'] = 'Go'
    
    # ____ panels ____
    s1 = cfg['Hotlist Panel Selector.content']
    for v in list(s1):
        del s1[v]
    for i, v in enumerate(['Bookmarks', 'Widgets', 'Notes', 'Transfers', 'History', 'Links']):
        s1['%s, %d' % (v, i)] = '"%s"' % KEY
    
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)
    
def process_prefs():
    filename = 'operaprefs_default.ini'
    cfg_from = INIConfig(open('myprefs.ini'), optionxformvalue=None)
    with open(filename) as fin: 
        header = fin.readline()
        cfg_to = INIConfig(fin, optionxformvalue=None)
        for sect in cfg_from:
            for key in cfg_from[sect]:
                cfg_to[sect][key]=cfg_from[sect][key]
    os.rename(filename, filename+'.bak')
    with open(filename,'wt') as fout:
        fout.write(header)
        print >>fout, cfg_to

if __name__ == '__main__':
#    process_mouse()
    process_keyboard()
#    process_toolbar()
#    process_prefs()
