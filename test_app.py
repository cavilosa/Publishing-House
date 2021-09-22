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

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyMjQ4MTgxLCJleHAiOjE2MzI0MTgxODEsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.fzO5a8C73ppQs9F3OCfZNTaERF28F_n8eStisMgL1U91t9Hv3GDj00CWawuomyGj81SZG0YtLtj-jpj_vzKTV3G6PJtXehS19NliCfTCfDNAEwjf8tBl07bULeCSVDctJNACPdeJxmguDce7gpW2fy36Y24BB169f9YfAZ1tBgvZEpErWYYvwvUvXhCz58BeZeNJYaxTmaTae_f0S8H29KuMnMIe1QXpGgpClADVPFZljremuLeqqSfR88NJeMobXvKLGrIJ2i3DA46HMFjUTjrXkv-p--glYyFVt4gdChItlfNW7hQ9iOW9rQt4RRtS-KLrmDurfDHqRA20WAxXgw"

class PublishingHouseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        password = os.environ["PASSWORD"]
        self.database_name = "test_publishing_house"
        self.database_path = "postgresql://{}:{}@{}/{}".format('cavilosa', password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

           # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
                # create all tables
            self.db.create_all()

        # with app.test_client() as c:
        #     with c.session_transaction() as sess:
        #         sess['token'] = token

        #     # once this is reached the session was stored
        #     result = app.test_client.get('/a_url')
        #     # NOT part of the 2nd context


        self.new_book = {
            "title":"TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": "TESTING YEAR"
        }
        
        self.new_author = {
            "name": "TESTONG NAME", 
            "yob": "TESTING YOB"
        }

        # self.new_book.authors.append(self.new_author)
        # self.new_author.books.append(self.new_book)

    def test_main_page(self):
        """MAIN PAGE"""
        
        
        # store the token in the session
        with self.client() as c:
            with c.session_transaction() as sess:
                sess['token'] = token
                # print("token", sess["token"])
        res = self.client().get('/', follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(request.path == url_for("callback_handling"))


    def tearDown(self):
       
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])
        pass


if __name__ == '__main__':
    unittest.main()