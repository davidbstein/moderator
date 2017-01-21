# moderator
google moderator clone


# setup notes

  - set up a moderator server
  - turn on the log somewhere `heroku --tail`
  - turn on sql
  - set up sql
    - `heroku pg:psql --app appboy-moderator < src/model/model.sql`
  - set up production config vars
