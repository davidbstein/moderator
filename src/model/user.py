
from model.helpers import (
  r2d,
  DB,
)


class User:
  @classmethod
  def get(cls, user_email, **__):
    assert "@" in user_email, "%s is not a valid email" % (user_email, )
    get_query = DB.users.select(DB.users.columns.u_email == user_email)
    user = DB.ex(get_query).fetchone()
    if user:
      return r2d(user)
    insert_command = DB.users.insert({
      "u_email": user_email,
      "domain": user_email.split("@")[-1],
      "info": {},
    })
    DB.ex(insert_command)
    to_ret = r2d(DB.ex(get_query).fetchone())
    return to_ret
