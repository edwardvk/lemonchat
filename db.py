import rethinkdb as r


def c():
    return r.connect("localhost", 32769, db='lemonchat').repl()


try:
    r.db_create("lemonchat").run(c())
except Exception as e:
    print(e)

for table in ('conversation', 'message', 'user'):
    try:
        r.db("lemonchat").table_create(table).run(c())
    except Exception as e:
        print(e)

try:
    r.table('conversation').index_create('scrapdate').run(c())
except Exception as e:
    print(e)




