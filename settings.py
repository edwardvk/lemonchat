weburl = "http://lemonchat.localhost"
rethinkport = 32769
testmode = False

try:
    from settings_local import *  # Override your deployment settings in here.
except Exception as e:
    pass
