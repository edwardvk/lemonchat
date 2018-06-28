weburl = "http://lemonchat.localhost"

try:
    from settings_local import *  # Override your deployment settings in here.
except Exception as e:
    pass
