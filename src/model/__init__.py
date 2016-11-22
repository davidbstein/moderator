from comment import Comment
from event import Event
from org import Org
from question import Question
from user import User
from helpers import DB as __DB

def get_all_event_info(event_id, user_email):
  event = Event.get(event_id, user_email)
  user = User.get(user_email)
  return {
    "event": event,
    "questions": Question.get_all_for_event(event, user),
  }

def get_all_question_info(question_id, user_email):
  user = User.get(user_email)
  question = Question.get(question_id, user_email)
  comments = Comment.get_all_for_question(question, override_auth=True)
  return {
    "question": question,
    "comments": comments,
  }

def list_events(user_email):
  user = User.get(user_email)
  return Event.get_all_for_domain(user['domain'], override_auth=True)
