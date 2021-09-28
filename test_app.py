from flask_testing import TestCase
from flask_wtf import FlaskForm
import os
from dotenv import load_dotenv
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from models import Author, Book, setup_db
from app import create_app
import pytest
from flask import session, url_for, request, Flask, render_template
from forms import BookForm, AuthorForm

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

        self.reader_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjY3M2NiZDI3MDAwNjlmODg3NGIiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyNzU5MDg4LCJleHAiOjE2MzI5MjkwODgsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIl19.PfXHm4b203QziRByA4g2_Bbqycow8MGr9TXAEMXsMd2YN49tfR5tYkJD9F1gPUivAqy3a-2jLgcK5J2XGPtrRXsDsa22pI0BNbKs0_0czeIoALkU9m279z4rHB95kF2c4ASgQ2gQeIktQ4DIWE6GiUZKDRP5baJq85ONlVrxwC46vx7XiDFVC-qJhPcOSvIb4rRObH2zrd6kpRSZkg4sJbtV2LKYz7yITJWdknWNlodEGZCI7T9Ww_uTXt9H4U2Jf0cGFhcF1Akbuq6yCH2-gtBwaTfnIiJEjUbOWMsqlHFMJN4Ct0BdX8tZ5sOhGtnnCE6sS9bdVc2xw77BMPAVnQ"

        self.coordinator_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjU0ZTYzNzYyYzAwNzBiZmU2MTgiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyNzU5MTUxLCJleHAiOjE2MzI5MjkxNTEsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.jnC9h7wB8H4bU3w5oMaGweLeQVhoaV9MhNHiKTaaPPnCIfv4ln1lOIaeJuqnOTN6G2uQreJjxsOncmsZQ69D8sBHYS8u15emx3MKBkjVS6EA5lI1QiS312zaq_UNaWvy7f0XpgX9asTQ-WZQdOiU9ehyf19PHZ80hMwZgWOawaubJuqSizWrqSKmIGTdHYJ-pNlCfA8B9kWCzgnguq5NRoMkUeSpJ8_WwPsbVAvJCWRTgqIgkxqybD-PbaTuOz2_zP9XS6OCu9OU1w6Ez32pBNnp1THdpdqnj19LjU-t_80jThEExYXyW-48qz3EXn-r-RuFVT6Q2lbsG1yj51rbQw"


        self.new_book = {
            "title": "TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": 3000
        }
        
        self.new_author = {
            "name": "TESTING NAME", 
            "yob": "TESTING YOB"
        }

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
        self.assertEqual(isinstance(books, list), True)
        self.assertEqual(isinstance(books[0], Book), True)
        self.assertEqual(isinstance(authors, list), True)
        self.assertEqual(isinstance(authors[0], Author), True)


    def test_landing_page(self):
        """test landing page"""
        response = self.client().get('/')
        books = Book.query.all()
        list = [book.format() for book in books]

        self.assertFalse(str(list) in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

#------------------------------------------------------------------------------------------------
# Tests for the Books part
# -----------------------------------------------------------------------------------------------


    def test_books_coordinator(self):
        """getting all the books for coordinator with links to details"""
        response = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})
        data = response.get_data(as_text=True)
        html = """<li><a href="/books/1">TEST, Anna, 2000</a></li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])


    def test_books_reader(self):
        """getting all the books for reader with no links to details"""
        response = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)
        html = """<li> TEST, Anna, 2000</li>"""

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


    def test_book_by_id_reader(self):
        """ get book by id for a reader"""
        response = self.client().get('/books/1', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)

        error = '{"code":"unauthorized","description":"Permission not found."}'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)


    def test_book_by_id_coordinator(self):
        """ get book by id for a coordinator"""
        response = self.client().get('/books/1', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        book = Book.query.get(1)
        book = book.format()

        title = f'<p>Title: {book["title"]}</p>'
        author = f'<p>Author: {book["author"]}</p>'
        year = f'<p>Year: {book["year"]}</p>'

        data = response.get_data(as_text=True)
     
        self.assertEqual(response.status_code, 200)
        self.assertIn(title, data)
        self.assertIn(author, data)
        self.assertIn(year, data)


    def test_create_book(self):
        """ create a book """
        response = self.client().post('/books/create', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        book = Book(title=self.new_book["title"], author=self.new_book["author"], year=self.new_book["year"])
        book.insert()
        id = book.format()["id"]

        check_book = Book.query.get(f'{id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(book)
        self.assertIsNotNone(check_book)


    def test_create_book_fail(self):
        """ create a book fails no authorization headders"""
        response = self.client().post('/books/create')

        # book = Book(title=self.new_book["title"], author=self.new_book["author"], year=self.new_book["year"])
        # book.insert()
        # id = book.format()["id"]

        # check_book = Book.query.get(f'{id}')
        
        self.assertEqual(response.status_code, 401)
        # self.assertFalse(book)
        # self.assertIsNone(check_book)

    
    def test_edit_book_coordinator_get(self):
        """ edit book by id for coordinator"""
        # check get method for the route
        response = self.client().get('/books/1/edit', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = response.get_data(as_text=True)
        book = Book.query.get(1).format()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(book)
        self.assertTrue(data)


    def test_web_edit_book(self):
        book = {
            "id": 1,
            "title": "TEST", 
            "author": "Anna",
            "year": 2000
        }
        response = self.client().post('/books/1/edit', json=book, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)
        print("test edit json post", data)

        # res = self.client().get('/books/1/edit', json=book, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})
        # data2 = json.loads(res.data)
        # print("edit book test get json", data2)

        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(res.status_code, 200)

        # self.assertEqual(data["success"], True)
        # self.assertIsNotNone(data["book"])


    def test_edit_book_coordinator_post(self):
        """ edit book by id for coordinator"""
        # check post method for the route
        res = self.client().post('/books/1/edit', follow_redirects=True, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})
        data = res.get_data(as_text=True)
        # print("data post", data)
        book = Book.query.get(1).format()
        title = f'<p>Title: {book["title"]}</p>'
        author = f'<p>Author: {book["author"]}</p>'
        year = f'<p>Year: {book["year"]}</p>'
    
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(book)
        self.assertTrue(data)
        self.assertIn(title, data)
        self.assertIn(author, data)
        self.assertIn(year, data)
    

    def test_edit_book_nonexistent_coordinator(self):
        """ edit book by non existing id for coordinator"""
        response = self.client().get('/books/100/edit', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})
        data = response.get_data(as_text=True)
        html = "You are trying to access a book with non existent id"

        self.assertEqual(response.status_code, 200)
        self.assertIn(html, data)


    def test_edit_book_reader(self):
        """ edit book by id for a reader"""
        response = self.client().get('/books/1/edit', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})

        data = response.get_data(as_text=True)
        error = '{"code":"unauthorized","description":"Permission not found."}'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)


#------------------------------------------------------------------------------------------------
# Tests for the Authors part
# -----------------------------------------------------------------------------------------------


    def test_authors_editor(self):
        """getting all the authors"""
        response = self.client().get('/authors', headers={'Authorization': 'Bearer {}'.format(self.editor_token)})
        data = response.get_data(as_text=True)
        html = """<li><a href="/authors/1"> Anna, 2017</a></li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])


    def test_authors_reader(self):
        """getting all the authors"""
        response = self.client().get('/authors', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)
        html = """<li>Anna, 2017</li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])



    def test_authors_notauthorized(self):
        """getting all the authors without authorization to fail"""
        response = self.client().get('/authors')
        data = response.get_data(as_text=True)
        html = """<li><a href="/authors/1"> Anna, 2017</a></li>"""
        authors = Author.query.all()
        list = [author.format() for author in authors]

        self.assertEqual(response.status_code, 401)
        self.assertNotIn(html, data)
        self.assertNotIn(str(list), data)
        self.assertIsNone(response.headers.get('Authorization'))



    def tearDown(self):
        pass
       


if __name__ == '__main__':
    unittest.main()