import os
import cherrypy
import mako.lookup
import api.root
import json
import random
import re
from cryptography.fernet import Fernet
import settings

TEMPLATES = mako.lookup.TemplateLookup(['templates'])

# sys.stdout = sys.stderr
# currentdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(currentdir)

# cherrypy.config.update({'environment': 'test_suite'})


def pickname():
    words = open("words.txt").read().split("\n")
    badwords = open("badwords.txt").read().split("\n")
    while True:
        word = random.choice(words)
        if word in badwords:
            continue
        if re.match("^[a-z]+$", word):
            break
    word += str(random.randint(10, 99))
    word = word[0].upper() + word[1:]
    return word


class Root(object):
    @cherrypy.expose
    def index(self, loginauth=None, template='chat'):
        assert template in ('index', 'chat')
        f = Fernet(settings.secret)  # lemongroup

        if not loginauth:
            # Look for cookies.
            if cherrypy.request.cookie.get('loginauth'):
                loginauth = str(cherrypy.request.cookie.get('loginauth').value)

        if not loginauth:
            # Assume an anonymous user, create a random user name for them.
            user_id = pickname()
            agent = 0
            
            loginauth = str(f.encrypt(json.dumps({'user_id': user_id, 'agent': agent}).encode()), "utf-8")
            cherrypy.response.cookie['loginauth'] = str(loginauth)
        else:
            input = json.loads(str(f.decrypt(loginauth.encode()), 'utf-8'))
            user_id = input['user_id']
            agent = input['agent']

        template = TEMPLATES.get_template(template + ".mako.html")
        return template.render(user_id=user_id, agent=agent)

    api = api.root.Root()


root = Root()
application = cherrypy.Application(root)

# if __name__ == "__main__":
#     cherrypy.quickstart(root, '/')