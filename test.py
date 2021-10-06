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
from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


class PublishingHouseTestCase(unittest.TestCase):

    def create_app(self):
        return create_app()

    def insert_data(self):
        """Seed test database with initial data"""
        book = Book(title="TEST", author="Anna", year=2000)
        author = Author(name="Anna", yob=2017)

        self.db.session.add(book)
        self.db.session.add(author)
        self.db.session.commit()
        self.db.session.close()

    def create_app(self):
        self.app = create_app()

        self.client = self.app.test_client

        self.database_path = f"postgresql://cavilosa:cavilosa1@localhost:5432/test"

        setup_db(self.app, self.database_path)
        self.db = SQLAlchemy()
        self.db.init_app(self.app)

        self.new_book = {
            "title": "TESTING TITLE",
            "author": "TESTING AUTHOR",
            "year": 3000
        }

        self.new_author = {
            "name": "TESTING NAME",
            "yob": "TESTING YOB"
        }

    def test_database(self):
        """ testing the db """
        books = Book.query.all()
        print("books len", len(books))
        authors = Author.query.all()
        self.assertEqual(isinstance(books, list), True)
        self.assertEqual(isinstance(books[0], Book), True)
        self.assertEqual(isinstance(authors, list), True)
        self.assertEqual(isinstance(authors[0], Author), True)

class sampleTestCase(PublishingHouseTestCase):
    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


if __name__ == '__main__':
    unittest.main()