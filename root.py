# import sys
# import os
import cherrypy
import mako.template
import rethinkdb as r
import wamp

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})
cherrypy.config.update({'server.socket_port': 8081})


class Root(object):
    @cherrypy.expose
    def index(self, user_id):
        template = mako.template.Template(filename="index.mako.html")
        return template.render(user_id=user_id)

    @cherrypy.expose
    def newconversation(self, user_id, subject):
        conn = r.connect("localhost", 32769, db='lemonchat').repl()
        r.table('conversation').insert([{'user_id': user_id, 'subject': subject}]).run(conn)
        wamp.publish('%s.conversations' % (user_id,))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conversationlist(self, user_id): 
        conn = r.connect("localhost", 32769, db='lemonchat').repl()
        result = list(r.table('conversation').filter({'user_id': user_id}).run(conn))
        return result

root = Root()
application = cherrypy.Application(root)

if __name__ == "__main__":
    cherrypy.quickstart(root, '/')
