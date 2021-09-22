from flask_testing import TestCase
import os
from dotenv import load_dotenv
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import Author, Book, setup_db
from app import create_app
import pytest
from flask import session, url_for, request

load_dotenv()


class PublishingHouseTestCase(unittest.TestCase):
    def insert_data(self):
        """Seed test database with initial data"""
        book = Book(title="TEST", author="Anna", year=2000)
        author = Author(name="Anna", yob=2017)
        book.authors.append(author)
        author.books.append(book)

        self.db.session.add(book)
        self.db.session.add(author)

        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.password = os.environ["PASSWORD"]
        self.database_name = "test_publishing_house"
        self.database_path = "postgresql://{}:{}@{}/{}".format('cavilosa', self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyMzM5MzA3LCJleHAiOjE2MzI1MDkzMDcsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.UcVle3fuBTg8_E2vlT_NiwnQ-UHLJ0Z_yH_MkoQIKJW0nnNHG9IlOQ3NwHSirKNixkrLkYOlp9gPHJd9hodDPf5PncDe7NApPobS-R8O-bVMqO9KG27KPJ6GlWLLOnkPxG8b7Vgy4mn06-HWB6s8G7jugGlln29Ea8svEyNZOoKjvSyt3lS-a39UFR22wxOdj6UqboSzmB2i79P1SnCuoFK7nt-v8-vLGBPI2VVvrGuFr9GS2LFeOUkZBHGN24KCZaxWogcDK85HnsPCD4Sm5Yy3BYmPrdlPbZsMjzf9gFWjRWH57wAwuQzBKOo-5H9diLLoVMSlpvD6Ki3T5d999Q"

        self.new_book = {
            "title":"TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": 3000
        }
        
        self.new_author = {
            "name": "TESTONG NAME", 
            "yob": "TESTING YOB"
        }

           # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.session.commit()
            self.db.session.close()
            self.db.session.remove()
            self.db.drop_all()
            self.db.create_all()
            # self.insert_data()


    def test_database(self):
        """ testing the db """
        books = Book.query.all()
        authors = Author.query.all()
        print(len(books), len(authors), books[0].format())
        self.assertEqual(isinstance(books, list), True)
        self.assertEqual(isinstance(books[0], Book), True)
        self.assertEqual(isinstance(authors, list), True)
        self.assertEqual(isinstance(authors[0], Author), True)
        


    def test_index(self):
        """MAIN PAGE"""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(request.path == url_for("callback_handling"))

    
    def test_books(self):
        res = self.client().get("/books", headers={'Authorization': 'Bearer ' + self.token})
        # data = json.loads(res)
        # print(data)
        self.assertEqual(res.status_code, 200)


    # def test_books(self):
    #     res = self.client().get("/books", headers={'Authorization': 'Bearer ' + self.token})

    #     self.assertEqual(res.status_code, 200)



#     # POST /manager
# def test_post_manager(self):
#     data = {
#         "name": "manager-2",
#         "phone": "1231231230",
#         "website": "www.facebook.com"
#     }
#     res = self.client().post(
#         '/manager', json=data, headers=ADMIN_AUTH)
#     data = json.loads(res.data)
#     self.assertEqual(res.status_code, 200)
#     self.assertEqual(data['success'], True)
#     self.assertEqual(data['manager']['name'], "manager-2")

    def tearDown(self):
        pass
       


if __name__ == '__main__':
    unittest.main()