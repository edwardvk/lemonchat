import os
import cherrypy
import mako.template
import api.root

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


class Root(object):
    @cherrypy.expose
    def index(self, user_id, agent=0, template='index'):
        assert template in ('index', 'chat')
        # @TODO If agent, then asset that user_id is actually an agent.
<<<<<<< HEAD
        template = mako.template.Template(filename=template + ".mako.html")
=======
        template = mako.template.Template(filename=os.path.join("templates", "index.mako.html"))
>>>>>>> 64f55c37e42c38d9a68c5620c102a917841fdc26
        return template.render(user_id=user_id, agent=agent)

    api = api.root.Root()

root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')
