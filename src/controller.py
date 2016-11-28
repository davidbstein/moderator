### TODO: look into
### flask flask-login google-login

from flask import (
  Flask,
  request,
  Response,
  send_from_directory,
  render_template,
  session,
)
from flask.sessions import (
  NullSession,
  SecureCookieSession,
)
import model
import json
app = Flask(__name__)
app.debug=True

def web_helper(json_encode_resp=False, require_login=True):
  """
  passes 'user' and 'body' args to decorated function - where 'user' is the user
  profile and 'body' is the post body (POSTs) or query params (GETs)
  """
  def outer(fn):
    def inner(*args, **kwargs):
      if isinstance(session, NullSession):
        assert not require_login
      if kwargs.get('user'):
        raise Exception("cannot name a url chunck 'user'")
      if kwargs.get('body'):
        raise Exception("cannot name a url chunck 'body'")
      kwargs['user'] = {}
      if request.method == "POST":
        kwargs['body'] = json.loads(request.data)
      if request.method == "GET":
        kwargs['body'] = request.args
      to_return = fn(*args, **kwargs)
      if json_encode_resp:
        return Response(
          response=json.dumps(to_return),
          status=200,
          mimetype="application/json",
        )
      else:
        return to_return
    inner.__name__ = fn.__name__
    return inner
  return outer

_ORG_PREFIX = "/o/<string:org>"
_EVENT_PREFIX = "{ORG_PREFIX}/<string:_event_name>-<string:event_id>".format(ORG_PREFIX=_ORG_PREFIX)
_POST = ("GET", "POST")
_GET = ("GET", "POST")


#######
# errors
#######

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 404


#######
# global routes
######

@app.route("/", methods=_GET)
@web_helper(require_login=False)
def home(body, user, **__):
  return send_from_directory("templates", "index.html")

@app.route("/about", methods=_GET)
@web_helper(require_login=False)
def about(body, user, **__):
  return "about"

@app.route("/login", methods=_GET)
@web_helper(require_login=False)
def login(body, **__):
  return "login"

@app.route("/logout", methods=_GET)
@web_helper(require_login=False)
def logout(body, **__):
  return "login"

@app.route("/post_question/<string:event_id>", methods=_GET)
@web_helper(require_login=False)
def question_form(**__):
  return "post a question"

#######
# local routes
#######

@app.route(_ORG_PREFIX, methods=_GET)
@web_helper()
def show_org(org=None, **__):
  raise Exception("")
  return org

@app.route(_EVENT_PREFIX, methods=_GET)
@web_helper()
def show_event(event_id, **kwargs):
  return json.dumps(kwargs)

@app.route(_EVENT_PREFIX + "/<question_id>", methods=_GET)
@web_helper()
def show_question(event_id, **kwargs):
  return json.dumps(kwargs)

##########
## API methods
##########
# HAX: I'm using POSTs and funky endpoints instead of standard HTTP
# methods. Not hard to fix if someone cares about being pedantic, but
# IMHO this isn't very important for functionality, so it will
# probably be a hack that lingers.
# - stein 2016-11-06

@app.route("/api/new_org", methods=_POST)
@web_helper(json_encode_resp=True)
def post_org(**kwargs):
  return Org.create(user.domain)

@app.route("/api/new_event", methods=_POST)
@web_helper(json_encode_resp=True)
def post_event(**kwargs):
  return {}

@app.route("/api/new_question", methods=_POST)
@web_helper(json_encode_resp=True)
def post_question(**kwargs):
  return {"foo": "bar"}

@app.route("/api/new_comment", methods=_POST)
@web_helper(json_encode_resp=True)
def post_comment(**kwargs):
  return {"foo": "bar"}

@app.route("/api/new_question_vote", methods=_POST)
@web_helper(json_encode_resp=True)
def post_question_vote():
  return {"foo": "bar"}

@app.route("/api/new_comment_vote", methods=_POST)
@web_helper(json_encode_resp=True)
def post_comment_vote():
  return {"foo": "bar"}

@app.route("/api/get_event", methods=_POST)
@web_helper(json_encode_resp=True)
def get_event():
  return {"foo": "bar"}

@app.route("/api/get_question", methods=_POST)
@web_helper(json_encode_resp=True)
def get_question():
  return {"foo": "bar"}

app.run()
