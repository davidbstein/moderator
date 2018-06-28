import os
import json

from model.helpers import (
  r2d,
  DB,
  PermissionError,
)

from model.user import User

_DOMAIN_MAPS = json.loads(os.environ.get("DOMAIN_MAPS", "{}"))

class Org:
  def __init__(self):
    raise Exception("This class is a db wrapper and should not be instantiated.")

  @classmethod
  def get(cls, domain, user_email, **__):
    user = User.get(user_email)
    user_domain = _DOMAIN_MAPS.get(user['domain'], user['domain'])
    if user_domain != domain:
      raise PermissionError("%s does not have a %s email" % (user_email, domain))
    org = DB.ex(
      DB.orgs.select(DB.orgs.columns.domain == domain)
    ).fetchone()
    assert org, "There is no org for the @" + user['domain'] + " domain yet! Are you signed in with your work account?"
    return r2d(org)

  @classmethod
  def create(cls, domain, user_email, **__):
    command = DB.orgs.insert({
      "domain": domain,
      "moderators": [user_email],
      "title": domain,
    })
    DB.ex(command)
    return Org.get(domain, user_email)

  @classmethod
  def update(cls, domain, user_email, moderators=None, title=None, **__):
    values = {}
    Org.get(domain, user_email)
    if moderators:
      values["moderators"] = moderators
    if title:
      values["title"] = title
    command = DB.orgs.update(
      ).where(
        DB.orgs.columns.domain == domain
      ).values(
        **values)
    DB.ex(command)
    return Org.get(domain, user_email)
