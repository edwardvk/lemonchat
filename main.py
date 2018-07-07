import cherrypy
import json
import datetime

from conversationcontroller import conversationcontroller
from messagecontroller import messagecontroller


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



if __name__ == '__main__':

    conversationcontroller = conversationcontroller()
    messagecontroller = messagecontroller();

    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)

    cherrypy.config['tools.json_out.handler'] = json_handler

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8081,
        'tools.CORS.on': True,
    })

    _api_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }

cherrypy.tree.mount(conversationcontroller, '/api/chat', _api_conf)
cherrypy.tree.mount(messagecontroller, '/api/message', _api_conf)

cherrypy.engine.start()
cherrypy.engine.block()
