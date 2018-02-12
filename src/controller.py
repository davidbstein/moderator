
from flask import (
  Flask,
  abort,
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
  get_org_info_by_user,
  list_events_for_user,
  Comment,
  Event,
  Org,
  Question,
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
app.config["VERSION"] = os.environ.get("HEROKU_RELEASE_CREATED_AT")
app.debug=os.environ.get("DEBUG") == "DEBUG"

_g_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
_g_client_id = os.environ.get("GOOGLE_CLIENT_ID")
_g_org_suffix = os.environ.get("GOOGLE_ORG_SUFFIX")

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
        if request.data:
          kwargs['body'] = json.loads(request.data)
        else:
          kwargs['body'] = dict(request.form)
      if request.method == "GET":
        kwargs['body'] = request.args
      try:
        to_return = fn(**kwargs)
      except AssertionError, e:
        print e.message
        abort(403, e.message)

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
_EVENT_PREFIX = "/e/<string:_event_name>-<string:lookup_id>"
_POST = ("GET", "POST")
_GET = ("GET", "POST")


#######
# errors
#######

@app.errorhandler(403)
def page_not_found(e):
  print e
  return render_template('403.html', message=e.description), 404

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('5xx.html'), 500


#######
# global routes
######

@app.route("/", methods=_GET)
@web_helper(require_auth=True)
def home(body, user, **__):
  org = get_org_info_by_user(user['email'])
  if (org):
    return render_template("index.html", user_info=session, info={
      'page': "org",
      'org_info': org,
      'events': list_events_for_user(user['email'])
    })

@app.route("/about", methods=_GET)
@web_helper(require_auth=True)
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

@app.route("/post_question/<string:lookup_id>", methods=_GET)
@web_helper(require_auth=False)
def question_form(lookup_id, **__):
  return render_template("post_question.html", lookup_id=lookup_id)

@app.route("/submit_question/<string:lookup_id>", methods=_POST)
@web_helper(require_auth=False)
def post_question_form(lookup_id, body=None, **__):
  content = body['content'][0]
  question = Question.create(lookup_id, content)
  return render_template("question_posted.html", lookup_id=lookup_id, question=question)

#######
# local routes
#######

@app.route(_ORG_PREFIX, methods=_GET)
@web_helper(require_auth=True)
def show_org(org=None, **__):
  assert org in (_g_org_suffix, 'gmail.com'), "unknown org"
  return org

@app.route(_EVENT_PREFIX, methods=_GET)
@web_helper(require_auth=True)
def show_event(lookup_id=None, user=None, **kwargs):
  org = get_org_info_by_user(user['email'])
  return render_template("index.html", user_info=session, info={
    'lookup_id': lookup_id,
    'page': 'event',
    'org_info': org,
  })

@app.route(_EVENT_PREFIX + "/<question_id>", methods=_GET)
@web_helper(require_auth=True)
def show_question(lookup_id, **kwargs):
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

@app.route("/api/new_comment", methods=_POST)
@web_helper(json_encode_resp=True)
def post_comment(body=None, user=None):
  comment = Comment.create(body['question_id'], user['email'], body['content'])
  return comment

@app.route("/api/new_question_vote", methods=_POST)
@web_helper(json_encode_resp=True)
def post_question_vote(user=None, body=None):
  question = Question.vote(
    question_id=body['question_id'],
    user_email=user['email'],
    score=body['vote']
  )
  return question

@app.route("/api/new_comment_vote", methods=_POST)
@web_helper(json_encode_resp=True)
def post_comment_vote(user=None, body=None):
  comment = Comment.vote(
    question_id=body['question_id'],
    comment_id=body['comment_id'],
    user_email=user['email'],
    score=body['vote']
  )
  return comment

@app.route("/api/get_event", methods=_POST)
@web_helper(json_encode_resp=True)
def get_event(user=None, body=None):
  return get_all_event_info(body['lookup_id'], user['email'])

@app.route("/api/get_question", methods=_POST)
@web_helper(json_encode_resp=True)
def get_question(user=None, body=None):
  return get_all_question_info(body['question_id'], user['email'])

if __name__ == "__main__":
  app.run()
