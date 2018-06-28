weburl = "http://lemonchat.localhost"\

try:
    import settings_local.py  # Override your deployment settings in here.
except Exception as e:
    pass