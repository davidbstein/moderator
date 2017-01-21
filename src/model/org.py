from model.helpers import (
  r2d,
  DB,
  PermissionError,
)

from user import User

class Org:
  @classmethod
  def get(cls, domain, user_email, **__):
    user = User.get(user_email)
    if user['domain'] != domain:
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
