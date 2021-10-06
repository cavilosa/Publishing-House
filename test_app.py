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

        self.db.session.add(book)
        self.db.session.add(author)

        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.password = os.environ["PASSWORD"]
        self.database_name = "test_publishing_house"
        self.database_path = "postgresql://{}:{}@{}/{}".format('cavilosa',
                                                               self.password,
                                                               'localhost:5432',
                                                               self.database_name)
        setup_db(self.app, self.database_path)

        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()
            self.insert_data()

        self.editor_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM5MDQwLCJleHAiOjE2MzM3MDkwNDAsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.d_TIhbtzX4tbe6Tr3A4bOTejivYsuFBn5vXfNw0G9KFOgdscPBw9jkxuJzfOAjhR5NiGnIUxVSioRrmmiJ854AELA4YQ8lrUgc7MLpk-M3bUs9IH8p32ml-n3fox3EPLyjnCmsSDHl146ITjp7_s0EKFrGOvo9AkE7XUXCvv-rMTSuPujWBGZdvxMS0JlSkEBJX7hBD1HYNAWQu_szP1aWI5OzyEwqSUjtSvwWqzZ9GfJia3QXHT9hf0hyqvX757UCK9necMez7hpKpICfRpx4YIpElEIf53JI5ddRvVqHdj8oSCQBsukOpbBleh9h6s6eWMiekME9Jdi5tCryK4lA"

        self.reader_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjY3M2NiZDI3MDAwNjlmODg3NGIiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM4ODg2LCJleHAiOjE2MzM3MDg4ODYsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIl19.BZgHspyLL6M24hC7lhaOmTZXFoe3htgBBQL1sz2LZ4Hv0YxcHZsr9-MqOB9n-1-eCp__fuQ2n-1GHFQIyXp-udNQ4frLJrvmDv-mNwn7uhO51t8v7DfSqV70CR_RxbeZahImdNOnzr--NF5z133bE4fBEZ-9Ffn8jomkv-Q5WgtYOXnAa5P-Ma_O9S5Ti9rAJHDQCDKuLlYHDON7aRaLTuP3sR6egyAevFJf37YqZJjDzzS17lJbvg9dh1jg_SNWGN_s7bDDWBvuIkYlXv4xqwLMb7ilDnBDq7EzMXZ1VUL2wq2wmDgmNOYxkkxFdfiBRGES2U5QgWXjWcTvQuimdQ'

        self.coordinator_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjU0ZTYzNzYyYzAwNzBiZmU2MTgiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM4OTMyLCJleHAiOjE2MzM3MDg5MzIsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.GlmyKBZZ0jVH4Scq8IDh1eUD3nirJUbriqXT5L32_P6gMx9xaj4_V0NT7V0cjPaUuVcgVm-v4CZ1VX6M79wJMldcAEzJwIPZEQa4oyBTyAhAlQ-e9jT4x06JN35bMAn3d_yg5mZTccMCK0HyvDN1VbR4yCm2k7QBEr1lgsw4VZn2pvCTW6ep7_oj68eYV3yszUZtWc4eJqjM3_PMEv04BfEAP1cHD-BOvy5FfiosiIhpMGVs--HxAkhkHyuYcvZdhfE3Dw3T9j1ctcDkMcPQMv4jH78Hh8ALT4QmXhOfG6HLWr2u5A_DBfE_f8XNiGgefpeCrINp5EbwXrSRy_7Ciw"

        self.new_book = {
            "title": "TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": 3000
        }

        self.new_author = {
            "name": "TESTING NAME",
            "yob": 2000
        }

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

# ----------------------------------------------------------------------------
# Tests for the Books part
# ---------------------------------------------------------------------------

# /books
    def test_all_books_coordinator(self):
        """getting all the books for coordinator with links to details
           checking get and post methods"""
        response = self.client().get('/books', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["books"])

        res = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = res.get_data(as_text=True)
        html = """<li><a href="/books/1">TEST, Anna, 2000</a></li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])

    def test_all_books_reader(self):
        """getting all the books for reader with no links to details"""
        response = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)
        html = """<li> TEST, Anna, 2000</li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])

    def test_all_books_notauthorized(self):
        """getting all the books without authorization to fail"""

        response = self.client().get('/books', json={})

        data = json.loads(response.data)
        error = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data["code"])
        self.assertIsNone(response.headers.get('Authorization'))

# /books/<id>
    def test_book_by_id_reader(self):
        """ get book by id for a reader"""
        response = self.client().get('/books/1', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)

        error = '{"code":"unauthorized","description":"Permission not found."}'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)

    def test_book_by_id_unauthorized(self):
        """ get book by id for a reader"""
        response = self.client().get('/books/1')
        data = response.get_data(as_text=True)

        error = '{"code":"authorization_header_missing","description":"Authorization header is expected."}\n'

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

        res = self.client().get('/books/1', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        book = Book.query.get(1).format()

        data_json = json.loads(res.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data_json["success"], True)
        self.assertEqual(data_json["book"], book)

        self.assertIn(title, data)
        self.assertIn(author, data)
        self.assertIn(year, data)

# /books/create
    def test_create_book(self):
        """ create a book """
        response = self.client().post('/books/create', json=self.new_book, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        res = self.client().get('/books/create', json=self.new_book, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data2 = json.loads(res.data)
        permission = "post:book"

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data2["permissions"])
        self.assertEqual(data["success"], True)
        self.assertIn(permission, data2["permissions"])

    def test_create_book_fail(self):
        """ create a book fails no authorization headers"""
        response = self.client().post('/books/create')

        data = json.loads(response.data)
        error = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data["code"])

    def test_create_book_reader(self):
        """a reader tries to access create book route without permissions"""

        res = self.client().get('/books/create', json=self.new_book, headers={'Authorization': 'Bearer {}'.format(self.reader_token)})

        data = json.loads(res.data)
        description = 'Permission not found.'

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"], description)

# /books/<id>/edit
    def test_edit_book_coordinator_get(self):
        """ edit book by id for coordinator"""
        # check get method for the route
        response = self.client().get('/books/1/edit', json=self.new_book, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_edit_book_unauthorized(self):
        """edititin the books/id/edit without auth"""
        response = self.client().get('/books/1/edit', json=self.new_book)

        data = json.loads(response.data)
        code = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["code"], code)

    def test_edit_book_coordinator_post(self):
        """ testing editing book by id with json response post and get"""
        response = self.client().post('/books/1/edit', json={"id": 1}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        res = self.client().get('/books/1/edit', json={"id": 1}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})
        data2 = json.loads(res.data)
        permission = "patch:book"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["book"])
        self.assertIn(permission, data2["permissions"])

    def test_edit_book_nonexistent_coordinator(self):
        """ edit book by non existing id for coordinator"""
        response = self.client().get('/books/1000/edit', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

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

# /books/<id>/delete
    def test_delete_book(self):
        """ deleting a book with editor permissions"""
        book = Book(self.new_book["title"], self.new_author["name"], self.new_book["year"])
        book.insert()

        response = self.client().get(f'/books/{book.id}/delete', json={}, headers={'Authorization': 'Bearer {}'.format(self.editor_token)})

        data = json.loads(response.data)
        permission = "delete:book"

        check_book = Book.query.get(book.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn(permission, data["permissions"])
        self.assertIsNone(check_book)

    def test_delete_book_fail(self):
        """ deleting a book fails"""
        response = self.client().post('/books/1000/delete', json={}, headers={'Authorization': 'Bearer {}'.format(self.editor_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], False)

# ----------------------------------------------------------------------------
# Tests for the Authors part
# ---------------------------------------------------------------------------
# /authors
    def test_all_books_coordinator(self):
        """getting all the authors for coordinator with links to details
           checking get and post methods"""
        response = self.client().get('/authors', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["authors"])

        res = self.client().get('/authors', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = res.get_data(as_text=True)
        html = """<li><a href="/authors/1"> Anna, 2017</a></li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])

    def test_all_authors_reader(self):
        """getting all the authors for reader with no links to details"""
        response = self.client().get('/authors', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})
        data = response.get_data(as_text=True)
        html = """ <li>Anna, 2017</li>"""

        self.assertIn(html, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Authorization", response.headers['Access-Control-Allow-Headers'])

    def test_all_authors_notauthorized(self):
        """getting all the authors without authorization to fail"""

        response = self.client().get('/authors', json={})

        data = json.loads(response.data)
        error = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data["code"])
        self.assertIsNone(response.headers.get('Authorization'))

# /authors/<id>
    def test_author_by_id_reader(self):
        """ get author by id for a reader"""
        response = self.client().get('/authors/1', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})

        data = response.get_data(as_text=True)
        error = '{"code":"unauthorized","description":"Permission not found."}'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)

    def test_author_by_id_unauthorized(self):
        """ get author by id for a reader"""
        response = self.client().get('/authors/1')
        data = response.get_data(as_text=True)

        error = '{"code":"authorization_header_missing","description":"Authorization header is expected."}\n'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)

    def test_author_by_id_coordinator(self):
        """ get author by id for a coordinator"""

        res = self.client().get('/authors/1', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        author = Author.query.get(1)
        formated_author = author.format()

        data_json = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data_json["success"], True)
        self.assertEqual(data_json["author"], formated_author)
        self.assertEqual(data_json["books"], author.books)

# /authors/create
    def test_create_author(self):
        """ create an author """
        response = self.client().post('/authors/create', json=self.new_author, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        res = self.client().get('/authors/create', json=self.new_author, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data2 = json.loads(res.data)
        permission = "post:author"

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data2["permissions"])
        self.assertEqual(data["success"], True)
        self.assertIn(permission, data2["permissions"])

    def test_create_author_fail(self):
        """ create author fails with no authorization headers"""
        response = self.client().post('/authors/create')

        data = json.loads(response.data)
        error = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data["code"])

    def test_create_author_reader(self):
        """a reader tries to access create author route without permissions"""

        res = self.client().get('/books/author', json=self.new_author, headers={'Authorization': 'Bearer {}'.format(self.reader_token)})

        data = json.loads(res.data)
        description = 'Permission not found.'

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"], description)

# /authors/<id>/edit
    def test_edit_author_coordinator_get(self):
        """ edit author by id for coordinator"""
        # check get method for the route
        response = self.client().get('/authors/1/edit', json=self.new_author, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        # check post method
        res = self.client().post('/authors/1/edit', json=self.new_author, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data_json = json.loads(res.data)

        author = Author.query.get(1).format()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data_json["success"], True)
        self.assertIn("patch:author", data["permissions"])
        self.assertEqual(author, data_json["author"])

    def test_edit_author_unauthorized(self):
        """edititin the authors/id/edit without auth"""
        response = self.client().get('/authors/1/edit', json=self.new_author)

        data = json.loads(response.data)
        code = 'authorization_header_missing'

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["code"], code)

    def test_edit_author_coordinator(self):
        """ testing editing author by id with json response post"""
        response = self.client().post('/authors/1/edit', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)
        author = Author.query.get(1).format()

        # checking get method with
        res = self.client().get('/authors/1/edit', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data2 = json.loads(res.data)
        permission = "patch:book"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["author"])
        self.assertEqual(author, data["author"])
        self.assertIn(permission, data2["permissions"])

    def test_edit_author_nonexistent_coordinator(self):
        """ edit author by non existing id for coordinator"""
        response = self.client().get('/authors/1000/edit', headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = response.get_data(as_text=True)
        html = "There is no such author in the database"

        self.assertEqual(response.status_code, 200)
        self.assertIn(html, data)

    def test_edit_author_reader(self):
        """ edit author by id for a reader"""
        response = self.client().get('/authors/1/edit', headers={'Authorization': 'Bearer {}'.format(self.reader_token)})

        data = response.get_data(as_text=True)
        error = '{"code":"unauthorized","description":"Permission not found."}'

        self.assertEqual(response.status_code, 401)
        self.assertIn(error, data)

# /authors/<id>/delete
    def test_delete_author(self):
        """ deleting author with editor permissions"""
        author = Author(self.new_author["name"], self.new_author["yob"])
        author.insert()
        id = author.id

        response = self.client().get(f'/authors/{id}/delete', json={}, headers={'Authorization': 'Bearer {}'.format(self.editor_token)})

        data = json.loads(response.data)
        permission = "delete:author"

        author = Author.query.get(f"{id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn(permission, data["permissions"])
        self.assertIsNone(author)

    def test_delete_author_fail(self):
        """ deleting an author fails for a cooridnator without permissions"""
        response = self.client().post('/authors/1000/delete', json={}, headers={'Authorization': 'Bearer {}'.format(self.coordinator_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["code"], "unauthorized")

    def test_delete_author_fail(self):
        """ deleting nonexistent author"""
        response = self.client().post('/authors/10000/delete', json={}, headers={'Authorization': 'Bearer {}'.format(self.editor_token)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data["success"])

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
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()


if __name__ == '__main__':
    unittest.main()
