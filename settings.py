weburl = "http://lemonchat.localhost"

try:
    from settings_local.py import *  # Override your deployment settings in here.
except Exception as e:
    pass