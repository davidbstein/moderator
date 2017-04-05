```
>>> model.__DB.ex("update events set domain='appboy.com-archive' where id=7")
<sqlalchemy.engine.result.ResultProxy object at 0x7f30039ec790>
>>> model.__DB.ex("select * from events where id=7").fetchall()
[(7L, u'appboy.com-archive', u'david.stein@appboy.com', u'7dc0313c6caa4ac43565102b3ce45577', [u'david.stein@appboy.com'], u'Appboy Mid-Q1 Company All-Hands', u'Appboy Mid-Q1 Company All-Hands')]
```
