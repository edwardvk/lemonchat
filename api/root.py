import datetime
import json
import cherrypy

import sys
import os
sys.path.append(os.path.dirname(__file__))

import conversation
import message

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

    def iterencode(self, value):
        # Adapted from cherrypy/_cpcompat.py
        for chunk in super().iterencode(value):
            yield chunk.encode("utf-8")


json_encoder = _JSONEncoder()


def json_handler(*args, **kwargs):
    # Adapted from cherrypy/lib/jsontools.py
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return json_encoder.iterencode(value)


def CORS():
    """Allow web apps not on the same server to use our API
    """
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = (
        "content-type, Authorization, X-Requested-With"
    )

    cherrypy.response.headers["Access-Control-Allow-Methods"] = (
        'GET, POST, PUT, DELETE, OPTIONS'
    )


cherrypy.config['tools.json_out.handler'] = json_handler
cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
cherrypy.config['tools.CORS.on'] = True

class Root(object):
    @cherrypy.expose
    def index(self, *a, **kw):
        # @TODO return help regarding the api interface
        return repr([x for x in dir(self) if not x.startswith("_")])

    message = message.message()
    conversation = conversation.conversation()


root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')
