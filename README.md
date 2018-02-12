# moderator
google moderator clone

# local setup

Using brew or the tool of your choice install python2.7, postgreSQL, npm, sass

```
virtualenv env --python=/usr/bin/python2.7
source setup.sh
source init.sh
source dev-build.sh
```

# prod setup notes

  - set up a moderator server
  - turn on the log somewhere `heroku --tail`
  - set heroku master to deploy from not head
    - `git push -f heroku HEAD:master`
  - turn on sql
  - set up sql
    - `heroku pg:psql --app <INSTANCE_ID> < src/model/model.sql`
  - set up production config vars

# administration

__TODO: an admin page__


### New Event
```
heroku run bash --app <INSTANCE_ID>
cd src/
python -c "
from model import Event
EVENT =
ME =
event = Event.create(EVENT, ME)
"
```

### Hide old event
```
heroku pg:psql --app <INSTANCE_ID>
update events where id=<EVENT_ID> set visible=0
```

# get to the DB
```
import model
model.__DB.ex("command")
```
