# -*- coding: utf-8 -*-
from sqlalchemy import Column,Integer,String,Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import app
"""
This script is used with sqlAlchemy, however I decided not use 
sqlAlchemy package, because it wasn't flexible enough to implement
the logic I wanted (dynamic table names)

For sqlAlchemy package, it is hard to dynamically change table names
rather model file should be structured for each table in a db 
"""

Base = declarative_base()
class DsmeText(Base):

  __tablename__ = app.table_name
  id = Column(Integer, primary_key = True)
  par_text = Column(Text)
  is_title = Column(Boolean)
  page = Column(Integer)

  # Add a property decorator to serialize information from this database
  @property
  def serialize(self):
      return {
          'par_text': self.par_text,
          'is_title': self.is_title,
          'page': self.page,
          'id': self.id

      }
#
#
# engine = create_engine('sqlite:///restaurants.db')

# To create a table with the name 'myTableName' in our database if one doesn’t already exist.
# Base.metadata.create_all(engine)