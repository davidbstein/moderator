# moderator
google moderator clone


# setup notes

  - set up a moderator server
  - turn on the log somewhere `heroku --tail`
  - set heroku master to deploy from not head
    - `git push -f heroku HEAD:master`
  - turn on sql
  - set up sql
    - `heroku pg:psql --app appboy-moderator < src/model/model.sql`
  - set up production config vars
