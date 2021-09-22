import os
from dotenv.main import load_dotenv
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
# from flask_migrate import Migrate
import json

load_dotenv()

password = os.environ["PASSWORD"]
# password = os.environ.get("PASSWORD")
database_name="publishing_house"
database_path = "postgresql://{}:{}@{}/{}".format('cavilosa', password, 'localhost:5432', database_name)

Base = declarative_base()

# app = FLASK(__name__)
# db = SQLAlchemy(app)
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()
    # add one demo row which is helping in POSTMAN test
    # book = Book(title="NEW BOOK", author=1, year=2000)
    # book.insert()

    # author = Author(name="NEW AUTHOR")
    # author.insert()

authors_books = db.Table("authors_books", 
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True), 
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True)
)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    # authors = db.relationship("Author", secondary=authors_books,
    #     backref=db.backref("books", lazy="dynamic", cascade="save-update, merge, delete"))

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
            "title":self.title,
            "author": self.author, 
            "year":self.year
        }

    def __repr__(self):
        return f"<{self.title}, {self.authors}, {self.year}>"


class Author(db.Model):
    __tablename__ = "authors"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    yob = Column(db.Integer, nullable=False)
    books = relationship("Book", secondary=authors_books, 
        backref=db.backref("authors", lazy='dynamic', cascade="save-update, merge, delete"))

    def __init__(self, name):
        self.name = name

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
            "name":self.name,
            "year_of_birth": self.yob
        }

    def __repr__(self):
        # return json.dumps(self.short())
        return f"<{self.id}, {self.name}>"


