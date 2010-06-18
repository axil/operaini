from iniparse import INIConfig
cfg = INIConfig('canonic.ini')
a = cfg.Application.GestureDown = 'New browser window'
print >>open('res.ini', 'wt'), cfg

