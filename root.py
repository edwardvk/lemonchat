import os
import cherrypy
import mako.lookup
import api.root
import json
from cryptography.fernet import Fernet
import settings

TEMPLATES = mako.lookup.TemplateLookup(['templates'])

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


class Root(object):
    @cherrypy.expose
    def index(self, loginauth, template='index'):
        assert template in ('index', 'chat')
        f = Fernet(settings.secret)  # lemongroup
        input = json.loads(f.decrypt(loginauth.encode()))
        user_id = input['user_id']
        agent = input['agent']

        template = TEMPLATES.get_template(template + ".mako.html")
        return template.render(user_id=user_id, agent=agent)

    api = api.root.Root()


root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')