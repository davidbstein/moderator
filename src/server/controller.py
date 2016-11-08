"""
VIEWS
=====

/
- home, welcome, create org

/about

/privacy

/login

/logout

/o/<org>
- create new event, list existing events
    /<event_id>-<event_id>
    - list of questions, voting, zooom into question
        #<question_id>
        - question view
/q/<event_lookup_id>
- post a question anonymously

APIs
====

/api/<event_lookup_id>
- post a question anonymously

"""
from flask import (
  Flask,
  request,
  session,
)
from flask.sessions import (
  NullSession,
  SecureCookieSession,
)
import json
app = Flask(__name__)
app.debug=True

def require_login():
  def inner(fn):
    return fn
  return inner

def web_helper():
  """ adds user and request post body fields """
  def outer(fn):
    def inner(*args, **kwargs):
      if isinstance(session, NullSession):
        raise Exception("FOOBAR")
      raise Exception("BAZ")
      if kwargs.get('user'):
        pass
      if kwargs.get('body'):
        pass
      kwargs['user'] = {}
      print request
      if request.method == "POST":
        print request.body
        kwargs['body'] = json.loads(request.body)
      return fn(*args, **kwargs)
    inner.__name__ = fn.__name__
    return inner
  return outer

_ORG_PREFIX = "/o/<string:org>"
_EVENT_PREFIX = "{ORG_PREFIX}/<string:_event_name>-<string:event_id>".format(ORG_PREFIX=_ORG_PREFIX)
_POST = ("GET", "POST")
_GET = ("GET",)
### flask flask-login google-login


#######
# global routes
######

@app.route("/", methods=_GET)
@web_helper()
def home(*_, **__):
  raise Exception("")
  return "home"

@app.route("/about", methods=_GET)
def about(*_, **__):
  return "about"

@app.route("/login", methods=_GET)
def login(*_, **__):
  return "login"

@app.route("/logout", methods=_GET)
def logout(*_, **__):
  return "logout"

#######
# local routes
#######

@require_login()
@app.route(_ORG_PREFIX, methods=_GET)
@web_helper()
def show_org(org=None, **__):
  raise Exception("")
  return org

@require_login()
@app.route(_EVENT_PREFIX, methods=_GET)
def show_event(**kwargs):
  return json.dumps(kwargs)

@require_login()
@app.route("/get_question", methods=_GET)
def show_question(**kwargs):
  return json.dumps(kwargs)

##########
## API methods
##########
# HAX: I'm using POSTs and funky endpoints instead of standard HTTP
# methods. It's an easy way to use GETs to test while I'm hacking
# this service together. Not hard to fix if someone cares about
# being pedantic, but IMHO isn't very important and this is fine,
# so it will probably be a hack that linkers.
# - stein 2016-11-06

@require_login()
@app.route("/api/new_org", methods=_POST)
def post_org(**kwargs):
  return Org.create(user.domain)

@require_login()
@app.route("/api/new_event", methods=_POST)
def post_event(**kwargs):
  pass

@app.route("/api/new_question", methods=_POST)
def post_question(*_, **__):
  return "foo"

@app.route("/api/new_question", methods=_POST)
def post_comment():
  return "foo"

@app.route("/api/new_question", methods=_POST)
def post_vote():
  return "foo"

@app.route("/api/new_question", methods=_POST)
def get_event():
  return "foo"

@app.route("/api/new_question", methods=_POST)
def get_question():
  return "foo"

app.run()
