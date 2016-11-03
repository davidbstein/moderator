"""
VIEWS
=====

/
- home, welcome, create org

/about

/privacy

/login

/logout

/o/<org>
- create new event, list existing events
    /<event_id>-<event_id>
    - list of questions, voting, zooom into question
        #<question_id>
        - question view
/q/<event_lookup_id>
- post a question anonymously

APIs
====

/api/<event_lookup_id>
- post a question anonymously

/api
  /<org>
    /<event_id>
      /question
        /new
        /<q_id>
          /vote
          /comment
            /new
            /<c_id>
              /vote
"""

### flask flask-login google-login
