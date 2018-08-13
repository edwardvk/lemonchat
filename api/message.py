import cherrypy
import rethinkdb as r
import arrow
import db
import wamp
import doyatelegram
import telegram
import datetime
from typing import Dict, List


class message():

    # expose all the class methods at once
    exposed = True

    # def _cp_dispatch(self, vpath: List[str]):
    #     # since our routes will only contain the GUID, we'll only have 1
    #     # path. If we have more, just ignore it

    #    # if len(vpath) == 3:
    #       #  cherrypy.request.params['conversation_id'] = vpath.pop()
    #        # vpath.pop()  # /conversation
    #         #cherrypy.request.params['user_id'] = vpath.pop()

    #     return self


    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """Creates a new conversation"""
        input = cherrypy.request.json
        inputParams = {}

        for key, value in input.items():
            inputParams[key] = str(value)

        result = r.table('message').insert([{'user_id': inputParams.get('user_id'), 'conversation_id': inputParams.get('conversation_id'),
                                             'message': inputParams.get('message'), 'stampdate': arrow.utcnow().datetime}]).run(db.c())
       # wamp.publish('conversation.%s' % (conversation_id), {'conversation_id': conversation_id})
        return result['generated_keys'][0]  # message_id

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(message_id):
        """Creates a new conversation"""
        input = cherrypy.request.json
        inputParams = {}

        for key, value in input.items():
            inputParams[key] = str(value)

        result = r.table('message').delete([{'conversation_id': inputParams.get('conversation_id')}]).run(db.c())
        # wamp.publish('conversation.%s' % (conversation_id), {'conversation_id': conversation_id})
        return result['generated_keys'][0]  # message_id

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def new(self, user_id, conversation_id, newmessage):
        try:
            previousmessage = r.table('message').filter({'conversation_id': conversation_id}).max('stampdate').run(db.c())
        except r.errors.ReqlNonExistenceError:
            previousmessage = None

        conversation = r.table('conversation').filter({'conversation_id': conversation_id}).run(db.c())

        result = r.table('message').insert([{'user_id': user_id, 'conversation_id': conversation_id, 'message': newmessage, 'stampdate': arrow.utcnow().datetime}]).run(db.c())
        wamp.publish('conversation.%s' % (conversation_id), {'conversation_id': conversation_id})
        wamp.publish('conversationsummary.%s' % (conversation_id), {'conversation_id': conversation_id})
        
        if arrow.utcnow().datetime - arrow.get(previousmessage['stampdate']).datetime > datetime.timedelta(minutes=15):
            try:
                doyatelegram.send('lemongroup', "New Message to old Conversation: %s. Go to https://masterpenny.com/lemonchat" % (conversation['subject']))
            except telegram.error.TimedOut:
                pass

        return result['generated_keys'][0]  # message_id
