import re, os
from iniparse import INIConfig
from copy import deepcopy
from optparse import OptionParser

KEY = '____________________________'
DRY_RUN = True

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
    if not DRY_RUN:
        if os.path.exists(filename+'.bak'):
            os.unlink(filename+'.bak')
        os.rename(filename, filename+'.bak')
        with open('canonic-res.ini') as fin:
            with open(filename, 'wt') as fout:
                fin.readline()
                for line in fin:
                    fout.write(re.sub(' = "%s"$' % KEY, '', line))

def set_key(cfg, section, key, value):
    try:
        curval = cfg[section][key]
        if value == curval:
            print "= setting %s['%s'] = '%s'" % (section, key, value)
        else:
            if type(curval) != str:
                print "+ setting %s['%s'] = '%s'" % (section, key, value)
            else:
                print "> setting %s['%s']: '%s' -> '%s'" % (section, key, curval, value)
            cfg[section][key] = value
    except:
        print "! setting %s['%s']: %s" % (section, key, '____error____')

def rename_key(cfg, section, key, newkey):
    curval = cfg[section][key]
    if type(curval) != str:
        if type(cfg[section][newkey]) == str:
            status, result = '=', '____already renamed____'
        else:
            status, result = '!', '____not found____'
    else:
        cfg[section]._lines[-1].find('PageUp ctrl').name = 'PageUp shift'
        status, result = '>', 'ok'
    print "%s renaming %s['%s'] -> %s['%s']: %s" % (status, section, key, section, newkey, result)

def remove_key(cfg, section, key):
    curval = cfg[section][key]
    if type(curval) != str:
        status, result = '!', '____not found____'
    else:
        del curval
        status, result = '>', 'ok'
    print "%s removing %s['%s']: %s" % (status, section, key, result)

def process_mouse():
    filename = 'ui/standard_mouse.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'))
    set_key(cfg, 'Application', 'GestureDown', 'New browser window')
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)

def process_keyboard():
    filename = 'ui/standard_keyboard.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'))
#    cfg.Application['t ctrl'] = 'Add to bookmarks'
#    cfg.Application['PageUp ctrl'] = 'Switch to previous page'
#    cfg.Application['PageDown ctrl'] = 'Switch to next page'
    set_key(cfg, 'Application', 't ctrl', 'Add to bookmarks')
    set_key(cfg, 'Application', 'PageUp ctrl', 'Switch to previous page')
    set_key(cfg, 'Application', 'PageDown ctrl', 'Switch to next page')
#    cfg['Browser Widget']['PageUp shift'] = 'Page left'
#    cfg['Browser Widget']['PageDown shift'] = 'Page right'
#    del cfg['Browser Widget']['PageUp ctrl']
#    del cfg['Browser Widget']['PageDown ctrl']

#    cfg['Browser Widget']._lines[-1].find('PageUp ctrl').name='PageUp shift'
#    cfg['Browser Widget']._lines[-1].find('PageDown ctrl').name='PageDown shift'
    rename_key(cfg, 'Browser Widget', 'PageUp ctrl', 'PageUp shift')
    rename_key(cfg, 'Browser Widget', 'PageDown ctrl', 'PageDown shift')

    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)

def process_toolbar():
    def add_button(desc, key, value):   # s1, s2 passed implicitly
        if type(s2[key])!=str:
            s1[key]=value
            print '>',
        else:
            print '=',
        print desc

    filename = 'ui/standard_toolbar.ini'
    canonize(filename)
    cfg = INIConfig(open('canonic.ini'), optionxformvalue=None)
    
    # ____ hotlist ____
    set_key(cfg, 'Hotlist.alignment', 'Collapse', '1')
    s1 = cfg['Bookmarks Panel Toolbar.content']
    s2 = deepcopy(s1)
    for v in s1:
        del s1[v]
    i=0
    for v in s2:
        s1[v] = s2[v]
        if i==0:
            add_button('new folder', 'Button, -1759909084', 'New folder')
        i = i+1 
    
    # ____ address bar, progress bar ____
    for section in 'Document Toolbar.content', 'Progress Toolbar.content':
        s1 = cfg[section]
        remove_key(cfg, section, 'Button, S_WAND_TOOLBAR_BUTTON_TEXT')  # wand combined with fast forward
        s2 = deepcopy(s1)
        for v in s1:
            del s1[v]
        add_button('rewind', 'Button, 1409512585', '"Rewind + Show popup menu, "Internal Rewind History""')
        for v in s2:
            if not 'HOME_BUTTON' in v and not 'WAND_TOOLBAR_BUTTON' in v:
                s1[v] = s2[v]
            if 'Combined Back Forward' in v:
                add_button('fast forward', 'Button, -108388079', '"Fast Forward + Show popup menu, "Internal Fast Forward History""')
                add_button('images', 'Button, -1320335960', '"Enable display images > Disable display images, , , '
                        '-383776252 > Display cached images only, , , 333270751 + Show popup menu, "Images And Style Menu""')
            if 'STOP_BUTTON' in v:
                add_button('wand', 'Button, -119414254', 'Wand')
            if v.startswith('Address'):         # address bar only
                add_button('go', 'Button, 870715797', 'Go')
    
    # ____ panels ____
    s1 = cfg['Hotlist Panel Selector.content']
    for v in list(s1):
        del s1[v]
    for i, v in enumerate(['Bookmarks', 'Widgets', 'Notes', 'Transfers', 'History', 'Links']):
        s1['%s, %d' % (v, i)] = '"%s"' % KEY
    
    print >>open('canonic-res.ini', 'wt'), cfg
    decanonize(filename)
    
def process_prefs(use_header=0):
    filename = 'operaprefs_default.ini'
    cfg_from = INIConfig(open('myprefs.ini'), optionxformvalue=None)
    with open(filename) as fin: 
        if use_header:
            header = fin.readline()
        cfg_to = INIConfig(fin, optionxformvalue=None)
        for sect in cfg_from:
            for key in cfg_from[sect]:
                cfg_to[sect][key]=cfg_from[sect][key]
    if not DRY_RUN:
        if os.path.exists(filename+'.bak'):
            os.unlink(filename+'.bak')
        os.rename(filename, filename+'.bak')
        with open(filename,'wt') as fout:
            if use_header:
                fout.write(header)
            print >>fout, cfg_to

def parse_options():
    global DRY_RUN
    parser = OptionParser()
    parser.add_option('-a', '--apply', dest='apply', action='store_true', default=False, help='apply changes')
    options, args = parser.parse_args()
    DRY_RUN = not options.apply
    if DRY_RUN:
        print '____Dry run____'

if __name__ == '__main__':
    parse_options()

#    process_mouse()
#    process_keyboard()
    process_toolbar()
#    process_prefs()
