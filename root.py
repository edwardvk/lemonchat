import os
import cherrypy
import mako.template
import api.root
import json
from cryptography.fernet import Fernet
import settings

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


class Root(object):
    @cherrypy.expose
    def index(self, loginauth):
        f = Fernet(settings.secret)  # lemongroup
        input = json.loads(f.decrypt(loginauth))
        user_id = input['salesagent_name']
        agent = input['agent']
        
        # @TODO If agent, then asset that user_id is actually an agent.
        template = mako.template.Template(filename=os.path.join("templates", "index.mako.html"))
        return template.render(user_id=user_id, agent=agent)

    api = api.root.Root()

root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')