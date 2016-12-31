from model.helpers import (
  r2d,
  DB,
)
from question import Question
from user import User

class Comment:
  @classmethod
  def get(cls, question_id, comment_id, user_email, **__):
    question = Question.get(question_id, user_email)
    comment_command = DB.comments.select(
      (DB.comments.columns.id==comment_id) &
      (DB.comments.columns.q_id == question_id)
    )
    return r2d(DB.ex(comment_command).fetchone())

  @classmethod
  def _flag_filter(cls, comment):
    comment = r2d(comment) or {}
    if comment.get("flagged", False):
      comment["content"] = "(this comment has been flagged as inappropriate and is being reviewed)"
    return comment

  @classmethod
  def get_all_for_question(cls, question, override_auth=False):
    assert override_auth
    query = DB.comments.select(
      DB.comments.columns.q_id==question['id']
      ).order_by(DB.comments.columns.id)
    return map(Comment._flag_filter, DB.ex(query))

  @classmethod
  def create(cls, question_id, user_email, comment, **__):
    question = Question.get(question_id, user_email)
    command = DB.comments.insert(dict(
      q_id=question_id,
      owner_email=user_email,
      content=comment,
      score=0,
    ))
    DB.ex(command)
    user = User.get(user_email)
    question = Question.get(question_id, user_email)
    comments = Comment.get_all_for_question(question, override_auth=True)
    return {
      "question": question,
      "comments": comments,
    }

  @classmethod
  def _update_vote(cls, question_id, comment_id, user_email, score):
    vote_clause = (
      (DB.comment_votes.columns.q_id == question_id) &
      (DB.comment_votes.columns.c_id == comment_id)
    )
    vote = r2d(DB.ex(DB.comment_votes.select(vote_clause)).fetchone()) or {}
    if vote:
      prev_score = vote.get("score", 0)
      vote_command = DB.comment_votes.update(
        ).where(
          vote_clause
        ).values(
          score=score
        )
    else:
      prev_score = 0
      vote_command = DB.comment_votes.insert(dict(
        c_id=comment_id,
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
  def vote(cls, question_id, comment_id, user_email, score, **__):
    assert -1 <= score <= 1, "vote must be -1, 0 or 1"
    comment = Comment.get(question_id, comment_id, user_email)
    vote = Comment._update_vote(question_id, comment_id, user_email, score)
    new_score = comment['score'] + vote['delta']
    comment_command = DB.comments.update(
      ).where(
        (DB.comments.columns.q_id == question_id) &
        (DB.comments.columns.id == comment_id)
      ).values(
        score=new_score
      ).returning(*DB.comments.columns)
    return r2d(
      DB.ex(
        comment_command
      ).fetchone()
    )

  @classmethod
  def flag(cls, question_id, comment_id, user_email, comment, **__):
    comment = Comments.get(question_id, comment_id, user_email)
    comment_command = DB.comments.update(
      ).where(
        (DB.comments.columns.q_id == question_id) &
        (DB.comments.columns.id == comment_id)
      ).values(
        flagged=True,
        flag_note=[comment]
      ).returning(*DB.comments.columns)
    return r2d(
      DB.ex(
        comment_command
      ).fetchone()
    )

  @classmethod
  def unflag(cls, question_id, user_email, comment, **__):
    raise PermissionError("you gotta do this manually in the DB")