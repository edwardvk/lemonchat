*****************
Install LemonChat
*****************

#. Install some system packages:
   apt install docker nginx
#. Install rethinkdb in a docker instance:
   docker run -d -P --name rethink1 rethinkdb
#. Setup your virtual environment:
   virtualenv -p python3 --no-site-packages venv-lemonchat 
#. Activate your virtual environment:
   . ./venv-lemonchat/bin/activate
#. Install the python packages inside your virtuelenv:
   pip install -r requirement.txt
#. Setup nginx
   ...
#. Run your uwsgi server.
   uwsgi uwsgi.ini