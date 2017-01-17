### TODO: look into
### flask flask-login google-login

from flask import (
  Flask,
  redirect,
  render_template,
  request,
  Response,
  send_from_directory,
  session,
)
from flask.sessions import (
  NullSession,
  SecureCookieSession,
)
from model import (
  get_all_event_info,
  get_all_question_info,
)
from oauth2client.client import OAuth2WebServerFlow
import json
import model
import os
import requests
import traceback
import urlparse

app = Flask(__name__)
app.config["SESSION_TYPE"] = os.environ.get("SESSION_TYPE")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.debug=True

_g_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
_g_client_id = os.environ.get("GOOGLE_CLIENT_ID")

_flow = OAuth2WebServerFlow(
  client_id=_g_client_id,
  client_secret=_g_client_secret,
  scope="email",
  redirect_uri=os.environ.get('URL')+"/auth",
  )

def oauth_login():
  return _flow.step1_get_authorize_url()

def get_user_from_code(code):
  credentials = _flow.step2_exchange(code)
  authorization_header = {"Authorization": "OAuth %s" % credentials.access_token}
  uri = "https://www.googleapis.com/oauth2/v2/userinfo"
  resp = requests.get(uri, headers=authorization_header)
  return resp.json()

def web_helper(require_auth=True, foo=1, json_encode_resp=False):
  """
  passes 'user' and 'body' args to decorated function - where 'user' is the user
  profile and 'body' is the post body (POSTs) or query params (GETs)
  """
  def outer(fn):
    def inner(*_, **kwargs):
      print session.get("user_info", {}).get("email"), "called: ", fn.__name__, kwargs, session.get("authed")
      parsed_url = urlparse.urlparse(request.url)
      if require_auth and not session.get('authed', False):
        session['path'] = request.path
        return redirect("/login")
      if kwargs.get('user'):
        raise Exception("cannot name a url chunck 'user'")
      if kwargs.get('body'):
        raise Exception("cannot name a url chunck 'body'")
      kwargs['user'] = session.get("user_info")
      if request.method == "POST":
        kwargs['body'] = json.loads(request.data)
      if request.method == "GET":
        kwargs['body'] = request.args
      to_return = fn(**kwargs)
      if json_encode_resp:
        return Response(
          response=json.dumps(to_return),
          status=200,
          mimetype="application/json",
        )
      else:
        traceback.print_exc()
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
@web_helper(require_auth=True)
def home(body, user, **__):
  return render_template("index.html", user_info=session)

@app.route("/about", methods=_GET)
@web_helper(require_auth=False)
def about(body, user, **__):
  return render_template("about.html", user_info=session)

@app.route("/login", methods=_GET)
@web_helper(require_auth=False)
def login(body, **__):
  login_url = oauth_login()
  return render_template("login.html", login_url=login_url)

@app.route("/auth", methods=_GET)
@web_helper(require_auth=False)
def auth(body, **__):
  code = body.get("code")
  user_info = get_user_from_code(code)
  if user_info:
    session['authed'] = True
    session['user_info'] = user_info
    path = (session.get("path") or "/")
    if "/log" in path:
      path = "/"
    session['path'] = None
    return redirect(path)
  else:
    return "login failed?"

@app.route("/logout", methods=_GET)
@web_helper(require_auth=False)
def logout(body, **__):
  session['authed'] = False
  session['user_info'] = {}
  return redirect("/login")

@app.route("/post_question/<string:event_id>", methods=_GET)
@web_helper(require_auth=False)
def question_form(event_id, **__):
  return render_template("post_question.html", event_id=event_id)

#######
# local routes
#######

@app.route(_ORG_PREFIX, methods=_GET)
@web_helper()
def show_org(org=None, **__):
  assert org in ('appboy.com', 'gmail.com'), "unknown org"
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
def post_question_vote(user=None, body=None):
  return {"foo": "bar"}

@app.route("/api/new_comment_vote", methods=_POST)
@web_helper(json_encode_resp=True)
def post_comment_vote(user=None, body=None):
  return {"foo": "bar"}

@app.route("/api/get_event", methods=_POST)
@web_helper(json_encode_resp=True)
def get_event(user=None, body=None):
  return get_all_event_info(body['event_id'], user['email'])

@app.route("/api/get_question", methods=_POST)
@web_helper(json_encode_resp=True)
def get_question(user=None, body=None):
  return get_all_question_info(body['question_id'], user['email'])

app.run()
