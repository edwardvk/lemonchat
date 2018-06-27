import rethinkdb as r
import cherrypy

def c():
    return r.connect("localhost", 32769, db='lemonchat').repl()

for table in ('conversation', 'message', 'user'):
    try:
        r.db("lemonchat").table_create(table).run(c())
    except Exception as e:
        print(e)

try:
    r.table('conversation').index_create('scrapdate').run(c())
except Exception as e:
    print(e)




