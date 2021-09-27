from flask_testing import TestCase
import os
from dotenv import load_dotenv
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from models import Author, Book, setup_db
from app import create_app
import pytest
from flask import session, url_for, request, Flask

load_dotenv()


def get_response_data(self, route):
    response = self.client().get(route)
    data = response.get_data(as_text=True)
    return data


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

        self.editor_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyNzU1MDg4LCJleHAiOjE2MzI5MjUwODgsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.LyG-t7c52XMtOyOQ6n7nL5EN04Hxs6Pv4kuYdrhklkoBXmLwkIYa2dNmlyjHeBukDww6Eq7duYhtJjkzICe6hJyXXhvj5h3MAKa1Ifbs0z1ABsXFp35DvPoU_Ha37z0Dt8P1djMMMZOFVJkexsY-Fdq_YB1xaQgB0gW8mwVQB-rRH0zJqP_TDIMmoZ8upbHqz-WsSmcamOYmROBuwVqcs8WGhKErNxw6AN7sibR1zxt3Kiqgmp2z0yl0X38Y2jgCaCnBXeY7N7zUofs3gk0e4xVqmncw2eZf6JJ11IUwug3UgkeN6rPAy3xxNMw9KrASs9H7Ac6Iv-W8ZVMREC88NA"

        self.new_book = {
            "title":"TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": 3000
        }
        
        self.new_author = {
            "name": "TESTONG NAME", 
            "yob": "TESTING YOB"
        }

        # @self.app.route("/")
        # def hello():
        #     return render_template("layouts/main.html")

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


    def test_landing_page(self):
        """test landing page"""
        response = self.client().get('/')
        books = Book.query.all()
        list = [book.format() for book in books]

        self.assertFalse(str(list) in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)


    def test_books(self):
        """getting all the books"""
        response = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.editor_token)})
        data = response.get_data(as_text=True)
        html = """<li><a href="/books/1">TEST, Anna, 2000</a></li>"""
       
        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])


    def test_books_notauthorized(self):
        """getting all the books without authorization to fail"""
        response = self.client().get('/books')
        data = response.get_data(as_text=True)
        html = """<li><a href="/books/1">TEST, Anna, 2000</a></li>"""
        books = Book.query.all()
        list = [book.format() for book in books]

        self.assertEqual(response.status_code, 401)
        self.assertNotIn(html, data)
        self.assertNotIn(str(list), data)
        self.assertIsNone(response.headers.get('Authorization'))


    def test_database(self):
        """ testing the db """
        books = Book.query.all()
        authors = Author.query.all()
        self.assertEqual(isinstance(books, list), True)
        self.assertEqual(isinstance(books[0], Book), True)
        self.assertEqual(isinstance(authors, list), True)
        self.assertEqual(isinstance(authors[0], Author), True)
        

    # def test_index(self):
    #     """Landing PAGE"""
    #     res = self.client().get('/test')
    #     self.assertEqual(res.status_code, 200)
    #     # self.assertEqual(request.path == url_for("callback_handling"))


    # def test_test(self):
    #     """testing the testing route"""
    #     # res = self.client(). get("/test")
    #     # # data = json.loads(res.data)
    #     # # print("DATA", data)
    #     books = Book.query.all()
    #     list = [book.format() for book in books]

    #     # self.assertEqual(res.status_code, 200)
    #     # self.assert_template_used('pages/books.html')
    #     # self.assert_context("permissions", list)
    #     rv = self.client().get('/test')
    #     data = rv.data
    #     # print("DATA", data)
    #     # self.assertIn("HTML", rv.data)
    #     self.assertEqual(rv.status_code, 200)
    #     # self.assertEqual(len(templates), 1)
    #     # template, context = templates[0]
    #     # self.assertEqual(template.name, "books.html")
    #     # self.assertEqual(len(context['items']), 10)
       
    
    # def test_books(self):
    #     """LIST BOOKS"""
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