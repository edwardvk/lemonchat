import cherrypy
import arrow
import rethinkdb as r
import db
from typing import Dict, List

import wamp


class conversation():
    # def _cp_dispatch(self, vpath: List[str]):
    #     # since our routes will only contain the GUID, we'll only have 1
    #     # path. If we have more, just ignore it
    #     if len(vpath) == 1:
    #         cherrypy.request.params['user_id'] = vpath.pop()
    #     elif len(vpath) == 3:
    #         cherrypy.request.params['conversation_id'] = vpath.pop()
    #         vpath.pop()  # /conversation
    #         cherrypy.request.params['user_id'] = vpath.pop()

    #     return self
    @cherrypy.expose
    def moo(self):
        return "Moo"

    @cherrypy.tools.json_out()
    def GET(self, **kwargs: Dict[str, str]) -> str:
        if 'conversation_id' in kwargs:
            return self.conversationsummary(kwargs['user_id'],kwargs['conversation_id'])
        elif 'user_id' in kwargs:
            return self.conversationlist(kwargs['user_id'])
        else:
            results = {}

        return results


    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """Creates a new conversation"""
        input = cherrypy.request.json
        inputParams = {}

        for key, value in input.items():
            inputParams[key] = str(value)

        result = r.table('conversation').insert(
            [{'user_id': inputParams.get('user_id'),
              'subject': inputParams.get('subject'),
              'stampdate': arrow.utcnow().datetime}]).run(db.c())
        # wamp.publish('conversations')  # @TODO a user should only listen to conversation that involve them
        return result['generated_keys'][0]  # conversation_id

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def new(self, user_id: str, subject: str):
        result = r.table('conversation').insert([{'user_id': user_id, 'subject': subject, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('conversations')  # @TODO a user should only listen to conversation that involve them
        return {"conversation_id": result['generated_keys'][0]}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self, user_id: str, agent=0):
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
    def summary(self, user_id: str, conversation_id: str):
        """Returns only the last updated datetime and the number of messages unread"""
        updated = r.table('message').filter({'conversation_id': conversation_id}).max('stampdate').run(db.c()).get('stampdate')

        # Now determine how many unread messages there are.,
        lastseen_message_ids = list(r.table('lastseen').filter({'conversation_id': conversation_id, 'user_id': user_id}).run(db.c()))
        if lastseen_message_ids:
            lastseen_message_id = lastseen_message_ids[-1]['message_id']
            allmessages = r.table('message').filter({'conversation_id': conversation_id}).order_by('stampdate').run(db.c())
            message_ids = [x['message_id'] for x in allmessages]
            try: 
                pos = message_ids.index(lastseen_message_id)
            except ValueError:
                pos = -1
            unread = len(message_ids) - pos - 1
        else:
            unread = 0
        return {'updated': updated, 'unread': unread}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def change(self, conversation_id: str, user_id: str): 
        results = list(r.table('message').filter({'conversation_id': conversation_id}).order_by('stampdate').run(db.c()))
        if results:
            r.table('lastseen').filter({'user_id': user_id, "conversation_id": conversation_id}).delete().run(db.c())
            r.table('lastseen').insert({'user_id': user_id, 'conversation_id': conversation_id, 'message_id': results[-1]['message_id']}).run(db.c())
            wamp.publish('conversationsummary.%s' % (conversation_id), {'conversation_id': conversation_id})
        return results

