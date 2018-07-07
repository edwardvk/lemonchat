from fabric.api import local, settings, abort, run, cd, sudo, env, put, parallel
from fabric.context_managers import prefix
from fabric.contrib.files import exists

env.hosts = []
env.hosts.append('lemonchat.nitric.co.za:32843')

env.deploy = '.'
version = "master"


def pull():
    with cd("/var/www/lemonchat.nitric.co.za/"):
        run("git pull")
