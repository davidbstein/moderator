from .comment import Comment
from .event import Event
from .org import Org
from .question import Question
from .user import User
from .helpers import DB as __DB

def get_org_info_by_user(user_email):
  user = User.get(user_email)
  org = Org.get(user['domain'], user['u_email'])
  if org:
    return org
  else:
    return {}

def get_all_event_info(event_lookup, user_email):
  e = Event.lookup(event_lookup, user_email)
  user = User.get(user_email)
  return {
    "event": e,
    "questions": Question.get_all_for_event(e, user),
  }

def get_all_question_info(question_id, user_email):
  user = User.get(user_email)
  question = Question.get(question_id, user_email)
  comments = Comment.get_all_for_question(question, override_auth=True)
  return {
    "question": question,
    "comments": comments,
  }

def list_events_for_user(user_email):
  user = User.get(user_email)
  return Event.get_all_for_domain(user['domain'], override_auth=True)
