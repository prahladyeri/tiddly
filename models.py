import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__author__ = "Prahlad Yeri"
__license__ = "MIT"

#TODO: Change as needed:
engine = create_engine("sqlite:///tiddly.db", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
dbsession = Session()

class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key=True)
	email = Column(String)
	password = Column(String)
	name = Column(String)
	
	def repr(self):
		return "<User(name=%s, email=%s, )>" % (name, email)
		
class Dual(Base):
	__tablename__ = "dual"
	id = Column(Integer, primary_key=True)
	text = Column(String)
	
	def repr(self):
		return "<Dual(id=%s, text=%s, )>" % (id, text)

Base.metadata.create_all(engine)

def get_class_by_tablename(tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename: #c.__table__.fullname == table_fullname
      return c