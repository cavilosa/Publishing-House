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

def test_session(self):
        with self.client() as c:
            with c.session_transaction() as sess:
                sess['token'] = self.token
                return sess
                # print(sess)


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

        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyNDI2MjMzLCJleHAiOjE2MzI1OTYyMzMsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.VUGT8ZBDDUWknogC1sULVPBf5OOoLHy8FrJFl6aW5vtHkoJbL7etNg5ls6r3mmKLhX7h0LGiW1I0B4IQqxlyltecqU9yXM9P4gPfjLQCTacfwz1ayn9iXBBrDHLNsnCTdRvClI2g8crZjwbYXSc8NqleGi8tteI1Mas1aHpeSH45s_BZQOaMtHXSA0hbW97wevn7tbAVGu3-oDY2lvMwJWzqaMF7miIEt_6VwXmQXP-j2KHX_KYKofkW6M8XylPGImB4LrmdaBhBic2tiksxGEAYtJCsHD9vFDCS2_5brMW5tqG792c31XRd2QtEMx8jkubjZZ6_EcFhuD4pMm6Z5Q', 'id_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJuaWNrbmFtZSI6ImNhdmlsb3NhMzMiLCJuYW1lIjoiY2F2aWxvc2EzM0BnbWFpbC5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvZGMzN2ZlOWRiYjc5Yzc3NWQ4NmMzNzAwZGQwY2FlOTg_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZjYS5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyMS0wOS0yM1QxOTo0Mzo1Mi44ODdaIiwiZW1haWwiOiJjYXZpbG9zYTMzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOiJhMG16TFBYMFBaNktQV1ZHbzA1OEZGQ1VVTndTaHFJTiIsImlhdCI6MTYzMjQyNjIzMywiZXhwIjoxNjMyNTEyNjMzLCJub25jZSI6IndBT3FWNFkwWUF6UWF2U3BlZ2hGIn0.Jh5kSscT7K3x2Vyg5eF2lwnLxZOLxN_F1o1kKlHeD1Wm6bnU_HSNtyZtvo9uVns8N0tmcX3fN3C0TV1N5VtNQxQ2Tyc064ergcKgazXcaPahIHQMMSdSp66Og-8eoX9MawJut6mYQqlt4q2FPLfxpigDaE99_shZURlrhjfEsMH0JI-_GomZavQfnTyvZXisHcx2y42Tzy61xgD8ndrpbS4CKb_oVlPpKYGACLj8WYCToDIauwzSuT1slcDjYSnidxHDft8n_boGuifwCeCiV5PD8_ExvpMGjYE3EvyIHpe_aNDeLzhDwFkhja_cqJnBotYqFw2em9XuPHXtDmhtNw"

        # with self.client() as c:
        #     with c.session_transaction() as sess:
        #         sess['token'] = self.token
                # print(sess)

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


    def test_local_page(self):
        """test local page"""
        response = self.client().get('/test')

        data = response.get_data(as_text=True)
        # print("DATA", data)
        session = test_session(self)
        # print(session)
        books = Book.query.all()
        list = [book.format() for book in books]
        # print("LIST", str(list))

        self.assertFalse(str(list) in response.get_data(as_text=True))


    def test_books(self):
        """getting all the books"""
        response = self.client().get('/books', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = response.get_data(as_text=True)
        # session = test_session(self)
        # SESSION = requests.Session()
        # SESSION.headers.update({"Authorization": "Bearer {}".format(self.token)})
        # print(SESSION.headers["Authorization"])
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(session["token"], self.token)


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