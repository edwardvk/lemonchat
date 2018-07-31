import os
import cherrypy
import mako.lookup
import api.root

TEMPLATES = mako.lookup.TemplateLookup(['templates'])

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


class Root(object):
    @cherrypy.expose
    def index(self, user_id, agent=0, template='index'):
        assert template in ('index', 'chat')
        # @TODO If agent, then asset that user_id is actually an agent.
        template = TEMPLATES.get_template(template + ".mako.html")
        return template.render(user_id=user_id, agent=agent)

    api = api.root.Root()


root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')
