import Crypto
import sqlalchemy as SA
import os

# util
class _DBWrapper:
  def __init__(self, **__):
    self.engine = SA.create_engine(os.environ.get("DATABASE_URL"))
    self.meta = SA.MetaData()
    self.meta.reflect(bind=self.engine)
  def __getattr__(self, a, **__):
    if (a in self.meta.tables):
        return self.meta.tables[a]
    raise AttributeError("DBWrapper has no attribute %s" % a)
  def ex(self, q, **__):
    connection = self.engine.connect()
    return connection.execute(q)
DB = _DBWrapper()
#/util

class User:
  def get(user_email, **__):
    assert "@" in user_email, "not a valid email"
    get_query = DB.users.select(DB.users.columns.u_email == user_email)
    user = DB.ex(get_query).fetchone()
    if user:
      return user
    insert_command = DB.users.insert({
      "u_email": user_email,
      "domain": user_email.split("@")[-1],
      "info": {},
    })
    DB.ex(insert_command)
    return DB.ex(get_query).fetchone()

class Org:
  def get(domain):
    org = DB.ex(
      DB.org.select(DB.org.domain == domain)
    ).fetchone()
    assert org, "no such org"
    return org

  def create(domain, user_email, **__):
    command = DB.orgs.insert({
      "domain": domain,
      "moderators": [user_email],
      "title": domain,
    })
    DB.ex(command)
    return Org.get(domain)

  def update(domain, moderators=None, title=None, **__):
    values = {}
    if moderators:
      values["moderators"] = moderators
    if title:
      values["title"] = title
    command = DB.orgs.update(
      ).where(DB.orgs.columns.domain == domain
      ).values(**values)
    DB.ex(command)
    return Org.get(domain)

class Event:
  def create(name, title, description, user_email, **__):
    user = User.get(user_email)
    org = Org.get(user.domain)
    unique_hash = "".join(map(
      lambda b: str(hex(ord(b)))[2:],
      Crypto.Random.new().read(16)
    ))
    new_event = dict(
      owner_email=user_email,
      domain=user.domain,
      lookup_id=unique_hash,
      moderators=list(set(org.moderators + [user_email])),
      title=title,
      description=description,
    )
    command = DB.events.insert(new_event)
    e_id = DB.ex(command).lastrowid
    return Event.get(e_id, user_email)

  def update(event_id, desc=None, moderators=None, **__):
    raise NotImplementedError()

  def lookup(event_lookup_id):
    query = DB.events.select(
      (DB.events.columns.e_id==event_id) &
      (DB.events.columns.domain==user.domain)
    )
    return DB.ex(query).fetchone()

  def get(event_id, user_email, **__):
    user = User.get(user_email)
    query = DB.events.select(
      (DB.events.columns.e_id==event_id) &
      (DB.events.columns.domain==user.domain)
    )

class Question:
  def create(event_lookup_id, content, **__):
    event = Event.lookup(event_lookup_id)
    DB.questions.insert(
      NotImplementedError
    )

  def get(question_id, **__):
    pass

  def flag(question_id, user_email, **__):
    pass

  def vote(question_id, user_email, vote, **__):
    pass


class Comment:
  def create(question_id, user_email, comment, **__):
    pass

  def vote(question_id, comment_id, user_email, vote, **__):
    pass
