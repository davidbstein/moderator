import sqlalchemy as SA
import os

class PermissionError(Exception):
  pass

def r2d(row):
  if row is None:
    return None
  return {k: row[k] for k in row.iterkeys()}

class _DBWrapper:
  def __init__(self, **__):
    self.engine = SA.create_engine(os.environ.get("DATABASE_URL"))
    self.meta = SA.MetaData()
    self.meta.reflect(bind=self.engine)
  def __getattr__(self, a, **__):
    if (a in self.meta.tables):
        return self.meta.tables[a]
    raise AttributeError("%s has no table %s" % (self.engine, a))
  def ex(self, q, **__):
    connection = self.engine.connect()
    return connection.execute(q)
DB = _DBWrapper()
