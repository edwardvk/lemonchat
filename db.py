import rethinkdb as r
import cherrypy



for table in ('conversation', 'message', 'user'):
    try:
        r.db("lemonchat").table_create(table).run()
    except Exception as e:
        print(e)


