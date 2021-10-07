import os
from dotenv.main import load_dotenv
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
import json

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

Base = declarative_base()

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def setup_db(app, DATABASE_URL=DATABASE_URL):
    if DATABASE_URL[0:10] != "postgresql":
        DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all() # Heroku deployment doesn't need this line

authors_books = db.Table("authors_books",
                         db.Column("book_id", db.Integer,
                                   db.ForeignKey("books.id"),
                                   primary_key=True),
                         db.Column("author_id", db.Integer,
                                   db.ForeignKey("authors.id"),
                                   primary_key=True)
                         )


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year):
        self.title = title,
        self.author = author,
        self.year = year

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    def __repr__(self):
        return f"<{self.title}, {self.authors}, {self.year}>"


class Author(db.Model):
    __tablename__ = "authors"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    yob = Column(db.Integer, nullable=False)
    books = relationship("Book", secondary=authors_books,
                         backref=db.backref("authors", lazy='dynamic',
                                            cascade="save-update, merge, \
                                                    delete"))

    def __init__(self, name, yob):
        self.name = name
        self.yob = yob

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "year_of_birth": self.yob
        }

    def __repr__(self):
        # return json.dumps(self.short())
        return f"<{self.id}, {self.name}>"
