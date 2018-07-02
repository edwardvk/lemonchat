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
    def index(self, user_id, agent=0):
        # @TODO If agent, then asset that user_id is actually an agent.
        template = mako.template.Template(filename="index.mako.html")
        return template.render(user_id=user_id, agent=agent)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newconversation(self, user_id, subject):
        result = r.table('conversation').insert([{'user_id': user_id, 'subject': subject, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('conversations')  # @TODO a user should only listen to conversation that involve them
        return result['generated_keys'][0]  # conversation_id

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationlist(self, user_id, agent=0):
        agent = int(agent)
        if agent:
            result = list(r.table('conversation').order_by('stampdate').run(db.c()))
        else:
            result = list(r.table('conversation').filter({'user_id': user_id}).order_by('stampdate').run(db.c()))
        for row in result:
            row['date'] = arrow.get(row.get('stampdate')).datetime
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationsummary(self, user_id, conversation_id):
        """Returns only the last updated datetime and the number of messages unread"""
        updated = r.table('message').filter({'conversation_id': conversation_id}).max('stampdate').run(db.c()).get('stampdate')
        
        # Now determine how many unread messages there are.,
        lastseen_message_ids = list(r.table('lastseen').filter({'conversation_id', 'user_id'}).run(db.c()))
        if lastseen_message_ids:
            lastseen_message_id = lastseen_message_ids[-1]['message_id']
            allmessages = r.table('message').filter({'conversation_id'}).order_by('stampdate').run(db.c())
            message_ids = [x['message_id'] for x in allmessages]
            pos = message_ids.index(lastseen_message_id)
            unread = len(message_ids) - pos
        else:
            unread = 0
        return {'updated': updated, 'unread': unread}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationchange(self, conversation_id, user_id): 
        result = list(r.table('message').filter({'conversation_id': conversation_id}).order_by('stampdate').run(db.c()))
        if result:
            r.table('lastseen').delete({'user_id': user_id, "conversation_id": conversation_id}, return_changes=False)
            r.table('lastseen').insert({'user_id': user_id, 'conversation_id': conversation_id, 'message_id': result[-1]['message_id']}).run(db.c())
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newmessage(self, user_id, conversation_id, newmessage):
        result = r.table('message').insert([{'user_id': user_id, 'conversation_id': conversation_id, 'message': newmessage, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('conversation.%s' % (conversation_id), {'conversation_id': conversation_id})
        return result['generated_keys'][0]  # message_id


root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')
