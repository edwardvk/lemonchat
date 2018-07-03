import cherrypy
import rethinkdb as r
import arrow
import db

from typing import Dict, List

class conversationcontroller():

    # expose all the class methods at once
    exposed = True


    def __init__(self):
        pass

    def _cp_dispatch(self, vpath: List[str]):
        # since our routes will only contain the GUID, we'll only have 1
        # path. If we have more, just ignore it
        if len(vpath) == 1:
            cherrypy.request.params['user_id'] = vpath.pop()
        elif len(vpath) == 3:
            cherrypy.request.params['conversation_id'] = vpath.pop()
            vpath.pop()  # /conversation
            cherrypy.request.params['user_id'] = vpath.pop()

        return self

    @cherrypy.tools.json_out()
    def GET(self, **kwargs: Dict[str, str]) -> str:


        if 'conversation_id' in kwargs:
            return self.conversationsummary(kwargs['user_id'],kwargs['conversation_id'])
        elif 'user_id' in kwargs:
            return self.conversationlist(kwargs['user_id'])
        else:
            results = {}

        return results


    def conversationlist(self,user_id):
        results = list(r.table('conversation').filter({'user_id':user_id}).order_by('stampdate').run(db.c()))
        for row in results:
            row['date'] = arrow.get(row.get('stampdate')).datetime
        return results;

    def conversationsummary(self,user_id,conversation_id):
        print(conversation_id)
        print(user_id)
#        updated = r.table('message').filter({'conversation_id': conversation_id}).max('stampdate').run(db.c()).get(
 #           'stampdate')

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
        return {'updated': 'updated', 'unread': unread}



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
