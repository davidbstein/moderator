import secrets
from model.helpers import (
  r2d,
  DB,
  PermissionError,
)

from model.user import User
from model.org import Org

class Event:
  def __init__(self):
    raise Exception("This class is a db wrapper and should not be instantiated.")

  @classmethod
  def get(cls, event_id, user_email, **__):
    user = User.get(user_email)
    query = DB.events.select(
      (DB.events.columns.id==event_id) &
      (DB.events.columns.domain==user['domain'])
    )
    event = DB.ex(query).fetchone()
    if not event:
      raise PermissionError("No event found in the set of events user has access to")
    return r2d(event)

  @classmethod
  def get_all_for_domain(cls, domain, override_auth=False):
    assert override_auth
    query = DB.events.select(
      (DB.events.columns.domain==domain) &
      (DB.events.columns.visible==1)
    )
    return map(r2d, DB.ex(query))

  @classmethod
  def lookup(cls, event_lookup_id, user_email=None, override_auth=False):
    query = DB.events.select(
      DB.events.columns.lookup_id==event_lookup_id
    )
    event = DB.ex(query).fetchone()
    if not override_auth:
      if event.domain != User.get(user_email)['domain']:
        raise PermissionError("No event found in the set of events user has access to")
    return r2d(event)

  @classmethod
  def create(cls, title, user_email, description=None, **__):
    title = title
    user = User.get(user_email)
    org = Org.get(user['domain'], user_email)
    unique_hash = "".join("%02x"%b for b in secrets.token_bytes(16))
    new_event = dict(
      owner_email=user_email,
      domain=user['domain'],
      lookup_id=unique_hash,
      moderators=list(set(org['moderators'] + [user_email])),
      title=title,
      description=description or title,
    )
    command = DB.events.insert(new_event).returning(*DB.events.columns)
    return r2d(DB.ex(command).fetchone())

  @classmethod
  def update(cls, event_id, desc=None, moderators=None, **__):
    raise NotImplementedError()
