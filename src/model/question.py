from model.helpers import (
  r2d,
  DB,
  PermissionError,
)

from user import User
from event import Event

class Question:
  @classmethod
  def _flag_filter(cls, question):
    question = r2d(question) or {}
    if question.get("flagged", False):
      question["content"] = "(this question has been flagged as inappropriate and is being reviewed)"
    return question

  @classmethod
  def get(cls, question_id, user_email, override_auth=False, **__):
    question = r2d(DB.ex(DB.questions.select(
      DB.questions.columns.id == question_id
    )).fetchone())
    event = Event.get(question['e_id'], user_email)
    assert event, "this should be unreachable since Event.get throws a PermissionError"
    return Question._flag_filter(question)

  @classmethod
  def get_all_for_event(cls, event, user):
    assert event['domain'] == user['domain'], "how did you call this?"
    return map(r2d,
      DB.ex(DB.questions.select(
        DB.questions.columns.e_id == event['id']
      ))
    )

  @classmethod
  def create(cls, event_lookup_id, content, **__):
    event = Event.lookup(event_lookup_id)
    command = DB.questions.insert(dict(
      e_id=event['id'],
      flagged=False,
      flag_note=[],
      content=content,
      score=0,
      comment_count=0,
    )).returning(*DB.questions.columns)
    return r2d(DB.ex(command).fetchone())

  @classmethod
  def flag(cls, question_id, user_email, comment, **__):
    question = Question.get(question_id, user_email)
    question['flagged'] = True
    question['flagged_note'].append(comment)
    DB.question.update(
      ).where(
        DB.questions.columns.id == question['id']
      ).values(
        **question
      )
    return Question.get(question_id, user_email)

  @classmethod
  def unflag(cls, question_id, user_email, comment, **__):
    question = Question.get(question_id, user_email)
    question['flagged'] = False
    question['flagged_note'].append(comment)
    DB.question.update(
      ).where(
        DB.questions.columns.q_id == question['id']
      ).values(
        **question)
    return Question.get(question_id, user_email)

  @classmethod
  def _update_vote(cls, question_id, user_email, score):
    vote_clause = (
      (DB.question_votes.columns.q_id == question_id) &
      (DB.question_votes.columns.user_email == user_email)
    )
    vote = r2d(DB.ex(DB.question_votes.select(vote_clause)).fetchone())
    if vote:
      prev_score = vote.get("score", 0)
      vote_command = DB.question_votes.update(
        ).where(
          vote_clause
        ).values(
          score=score
        )
    else:
      prev_score = 0
      vote_command = DB.question_votes.insert(dict(
        q_id=question_id,
        user_email=user_email,
        score=score,
      ))
    DB.ex(vote_command)
    return {
      "prev_vote_score": prev_score,
      "new_vote_score": score,
      "delta": score - prev_score,
    }

  @classmethod
  def vote(cls, question_id, user_email, score, **__):
    assert -1 <= score <= 1, "vote must be -1, 0 or 1"
    question = Question.get(question_id, user_email)
    assert question, "no question found that user has permission to access"
    vote = Question._update_vote(question_id, user_email, score)
    new_score = question['score'] + vote['delta']
    question_command = DB.questions.update(
      ).where(
        DB.questions.columns.id == question_id
      ).values(
        score=new_score
      ).returning(*DB.questions.columns)
    return r2d(
      DB.ex(
        question_command
      ).fetchone()
    )

  @classmethod
  def flag(cls, question_id, user_email, comment, **__):
    question = Comments.get(question_id, user_email)
    question_command = DB.questions.update(
      ).where(
        (DB.questions.columns.id == question_id)
      ).values(
        flagged=True,
        flag_note=[comment]
      ).returning(*DB.questions.columns)
    return r2d(
      DB.ex(
        question_command
      ).fetchone()
    )

  @classmethod
  def unflag(cls, question_id, user_email, comment, **__):
    raise PermissionError("you gotta do this manually in the DB")

