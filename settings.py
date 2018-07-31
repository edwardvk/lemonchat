weburl = "http://lemonchat.localhost"
rethinkport = 0

try:
    from settings_local import *  # Override your deployment settings in here.
except Exception as e:
    pass
