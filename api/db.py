import sys
sys.path.append('..')
import rethinkdb as r
import settings
print(dir(settings))

def c():
    return r.connect("localhost", settings.rethinkport, db='lemonchat').repl()


if __name__ == "__main__":
    try:
        r.db_drop('lemonchat').run(c())
    except Exception as e:
        print(e)
    try:
        r.db_create("lemonchat").run(c())
    except Exception as e:
        print(e)

    for table in ('conversation', 'message', 'user', 'lastseen'):
        try:
            r.db("lemonchat").table_create(table, primary_key=table + "_id").run(c())
        except Exception as e:
            print(e)

    try:
        r.table('conversation').index_create('scrapdate').run(c())
    except Exception as e:
        print(e)


