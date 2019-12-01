"""
**Introduction**

The Trivia app includes two sql Alchemy classes used manage the trivia
questions and categories.

- Questions: List of questions and anssers
- Categories: List of categories for the questions

"""

import os
from sqlalchemy import Column, String, Integer, create_engine
from flask import abort
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


# setup_db(app)
# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# ----------------------------------------------------------------------------#
# Helper Functions
#    populateClass: takes a Rest request object and populates the attributes
#    of a class (rather than list out all of the attributes)
#    names between the jsondata and class must be the same
# ----------------------------------------------------------------------------#
def populateClass(theInstance, requestData):
    for (attribute, required) in theInstance.__columnNames__:
        value = requestData.get(attribute, None)
        if required and value is None:
            abort(422)
        setattr(theInstance, attribute, value)


# ----------------------------------------------------------------------------#
# SQLAlcemy Class for question table
# ----------------------------------------------------------------------------#
class Question(db.Model):
    """The model definition for each question plus supporting CRUD operations
    """
    __tablename__ = 'questions'

    # Name of the columns and if they are required (True)
    __columnNames__ = [('question', True),
                       ('answer', True),
                       ('category', True),
                       ('difficulty', True)]

    # Metadata for the Question class
    id = Column(Integer, primary_key=True)
    """*id* is the auto assigned primary key.
        Type: Integer, Primary key. Required.
    """
    question = Column(String)
    """*question* is the question to be presented to the trivia players.
        Type: String, Required.
    """
    answer = Column(String)
    """*answer* the answer to the trivia question.
      Type: String, Required.
    """
    category = Column(String)
    """*category* is the question category.
      Type: String, respresented as an Integer.
      Is the Forigen Key of Category. Required.
    """
    difficulty = Column(Integer)
    """*difficulty* is the difficulty level of the question
      Type: Integer, Required.
    """

    # The question object is dynamically updated with data from the json
    # request object
    def __init__(self, request_json):
        # create the class with data from the request responses' json
        populateClass(self,  request_json)

    def insert(self):
        """Insert the Question object, as a row, into the trivia database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the Question object with any changes
        """
        db.session.commit()

    def delete(self):
        """Delete the Question object from the trivia database
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Return the Question record object as a Python Dictionary
        """
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }


# ----------------------------------------------------------------------------#
# SQLAlcemy Class for category table
# ----------------------------------------------------------------------------#
class Category(db.Model):
    """This class is the model for the list of tricia categories
    """
    __tablename__ = 'categories'

    # Metadata
    id = Column(Integer, primary_key=True)
    """*id* is the auto assigned primary key
      Type: Integer, Primary key. Required.
    """
    type = Column(String)
    """*type* is the question category name
      Type: String. Required.
    """

    def __init__(self, type):
        self.type = type

    def format(self):
        """Return the category record object formatted as a Python Dictionary
        """
        return {
          'id': self.id,
          'type': self.type
        }
