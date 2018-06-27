# import sys
# import os
import arrow
import datetime
import json
import cherrypy
import mako.template
import rethinkdb as r
import wamp
import db

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


cherrypy.config.update({'server.socket_port': 8081})
cherrypy.config['tools.json_out.handler'] = json_handler


class Root(object):
    @cherrypy.expose
    def index(self, user_id):
        template = mako.template.Template(filename="index.mako.html")
        return template.render(user_id=user_id)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newconversation(self, user_id, subject):
        result = r.table('conversation').insert([{'user_id': user_id, 'subject': subject, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('%s.conversations' % (user_id,))
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationlist(self, user_id): 
        result = list(r.table('conversation').filter({'user_id': user_id}).order_by('stampdate').run(db.c()))
        for row in result:
            row['prettydate'] = arrow.get(row.get('stampdate')).humanize()
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationchange(self, conversation_id): 
        result = list(r.table('message').filter({'conversation_id': conversation_id}).order_by('stampdate').run(db.c()))
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newmessage(self, user_id, conversation_id, newmessage):
        result = r.table('message').insert([{'user_id': user_id, 'conversation_id': conversation_id, 'message': newmessage, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('%s.conversation.%s' % (user_id, conversation_id))
        return result


root = Root()
application = cherrypy.Application(root)

if __name__ == "__main__":
    cherrypy.quickstart(root, '/')
