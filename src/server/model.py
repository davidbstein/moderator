"""

Users
 + domain
 + u_id (email)
 - info

Org
 + domain
 - moderators
 - title

Events
 + domain
 + e_id
 + owner
 + lookup_id
 - moderators
 - title
 - description

Questions
 + e_id
 + q_id
 - flagged
 - flag_note
 - content
 - score
 - comments

Comments
 + o_id
 + q_id
 + c_id
 - u_id
 - content
 - score

Question_likes
 + q_id
 + u_id
 - score

Comment_likes
 + c_id
 + u_id
 - score

"""

class Org:
  def create(domain):
    pass

  def update(domain, moderators=None, name=None):
    pass

class Event:
  def create(name):
    pass

  def update(event_id, desc=None, moderators=None):
    pass

  def get(event_id, user_id):
    pass


class Question:
  def create(event_lookup_id, content):
    pass

  def get(question_id):
    pass

  def flag(question_id, user_id):
    pass

  def vote(question_id, user_id, vote):
    pass


class Comment
  def create(question_id, user_id, comment):
    pass

  def vote(question_id, comment_id, user_id, vote):
    pass
