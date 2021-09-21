import os
from flask import Flask, request, abort, jsonify, redirect, render_template, request, url_for, flash
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from flask_cors import CORS, cross_origin
import json
from dotenv import load_dotenv
from models import db, setup_db,  Book, Author, authors_books
from forms import BookForm, AuthorForm
from auth.auth import AuthError, verify_decode_jwt, requires_auth
from flask_migrate import Migrate
# from .auth.auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask import session

load_dotenv()

#---------------------------------------------------------------------------------------------
# Configuring APP
#----------------------------------------

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, expose_headers='Authorization')
    migrate = Migrate(app, db)
    setup_db(app)
    app.secret_key = os.environ["JWT_CODE_SIGNING_SECRET"]

 

#----------------------------------------------------------------------------
# OAUTH initiation
#---------------------------------------------------------------------------
    oauth = OAuth(app)

    auth0 = oauth.register(
    'auth0',
    client_id=os.environ["AUTH0_ID"],
    client_secret=os.environ["JWT_CODE_SIGNING_SECRET"],
    api_base_url='https://' + os.environ["AUTH0_DOMAIN"],
    access_token_url='https://' + os.environ["AUTH0_DOMAIN"] + '/oauth/token',
    authorize_url='https://' + os.environ["AUTH0_DOMAIN"] + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    )
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        # print ("HEADERS", request.headers)
        return response


# Initial route to authorize with auth0
# -------------------------------------------------------------------------------------------
#
    @app.route("/", methods=["GET"])
    def index():
        # print ("SESSION get token", session.get("token"))
        if session.get("token"):
            print ("SESSION TOKEN TRUE")
            return redirect("/callback")
        else:
            login = True
            return render_template("layouts/main.html", login=True)


    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri="http://localhost:5000/callback", audience="app")


    @app.route('/callback')
    def callback_handling():
        print("CALLBACK")
        if session.get("token"):
            # print("SESSION TOKEN", session["token"])
            token = session["token"]
        else:
            token = auth0.authorize_access_token()
            session['token'] = token['access_token']
            token = token['access_token']
        
        payload = verify_decode_jwt(token)

        permissions = payload["permissions"]
        role = ""
        login = True
        if "delete:author" and "delete:book" in permissions:
            # flash('You were successfully logged in as an editor')
            return render_template('layouts/main.html', role="editor", permissions=permissions, login=False, token=True)

        elif "patch:author" and "post:book" in permissions:
            # flash('You were successfully logged in as a coordinator')
            return render_template('layouts/main.html', role="coordinator", permissions=permissions, login=True, token=token)

        elif "get:book" and "get:authors" in permissions:
            # flash('You were successfully logged in as a reader')
            return render_template('layouts/main.html', role="reader", permissions=permissions, login=False, token=True) 

        else:
            return render_template('layouts/main.html')
       
# Logout 
#-----------------------------------------------------------------------------------------------
#
    @app.route('/logout')
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {'returnTo': url_for('index', _external=True), 'client_id': os.environ["AUTH0_ID"]}
        return redirect('https://korzhyk-app.us.auth0.com' + '/v2/logout?' + urlencode(params))


#----------------------------------------------------------------------------------------
# Books routes: list, create, patch
#-----------------------------------------------------------------------------------------

# List all the books in the db
    @app.route("/books", methods=["GET"])
    @cross_origin()
    @requires_auth("get:books")
    def books(payload):
        role =[]
        permissions = payload["permissions"]

        books = Book.query.order_by(Book.id).all()
        
        return render_template("pages/books.html", books=books, permissions=permissions)


# See a book by it's id
    @app.route("/books/<id>", methods=["GET"])
    @cross_origin()
    @requires_auth("post:book")
    def book_by_id(payload, id):

        book = Book.query.get(id)

        permissions = payload["permissions"]

        return render_template("pages/book.html", book=book, permissions=permissions)


# Edit a book by it's id
    @app.route("/books/<id>/edit", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("patch:book")
    def edit_book(payload, id):
        # session.pop('_flashes', None)
        book = Book.query.get(id)
        permissions = payload["permissions"]
        form = BookForm(obj=book)

        if request.method == "POST":
            form = BookForm(request.form, meta={'csrf': False})
            book = Book.query.get(id)
            

            if form.validate_on_submit():
                # flash("Successfully created a new book")
                form.populate_obj(book)

                book.update()

            return render_template("pages/book.html", book=book, permissions=permissions)

        return render_template("forms/edit_book.html", form=form)


# Create new book
    @app.route("/books/create", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("post:book")
    def create_book(payload):

        permissions = payload["permissions"]
        book = Book(title="", author="", year=0)
        authors = Author.query.all()
        # print("AUTHORS", authors)
        form = BookForm()

        if request.method == "POST":
            form = BookForm(request.form, meta={'csrf': False})

            name = request.form.get("author")

            author=Author.query.filter_by(name=name).first()
            # print("AUTHOR", author.id)
        
            if form.validate_on_submit():
                
                form.populate_obj(book)

                book.authors.append(author)
                
                book.insert()

            books = Book.query.order_by(Book.id).all()

            return render_template("pages/books.html", books=books, permissions=permissions,   authors=authors)

        return render_template("forms/create_book.html", form=form, authors=authors)


#------------------------------------------------------------------------------------------
# Authors
#------------------------------------------------------------------------------------------

    @app.route("/authors", methods=["GET"])
    @cross_origin()
    @requires_auth("get:authors")
    def authors(payload):

        permissions = payload["permissions"]

        authors = Author.query.order_by(Author.id).all()
        
        return render_template("pages/authors.html", authors=authors, permissions=permissions)


    @app.route("/authors/<id>", methods=["GET"])
    @cross_origin()
    @requires_auth("post:author")
    def author_by_id(payload, id):

        author = Author.query.get(id)

        books = []

        for book in author.books:
            item = {
                "title": book.title,
                "year": book.year
            }
            books.append(item)
        

        permissions = payload["permissions"]

        return render_template("pages/author.html", author=author, permissions=permissions, books=books)


# Edit a book by it's id
    @app.route("/authors/<id>/edit", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("patch:author")
    def edit_author(payload, id):
        # session.pop('_flashes', None)
        author = Author.query.get(id)
        permissions = payload["permissions"]
        form = AuthorForm(obj=author)

        if request.method == "POST":
            form = AuthorForm(request.form, meta={'csrf': False})
            author = Author.query.get(id)
            

            if form.validate_on_submit():
                # flash("Successfully created a new book")
                form.populate_obj(author)

                author.update()

            return render_template("pages/author.html", author=author, permissions=permissions)

        return render_template("forms/edit_author.html", form=form)


# Delete book by it's id
    @app.route("/books/<id>/delete", methods=["GET", "POST"])
    @cross_origin()
    @requires_auth("delete:book")
    def delete_book(payload, id):
        book = Book.query.get(id)
        permissions = payload["permissions"]

        book.delete()

        books = Book.query.order_by(Book.id).all()
        
        return render_template("pages/books.html", books=books, permissions=permissions)


# DELETE author by id

    @app.route("/authors/<id>/delete", methods=["GET", "POST"])
    @cross_origin()
    @requires_auth("delete:author")
    def delete_author(payload, id):
        author = Author.query.get(id)
        permissions = payload["permissions"]
        # print("METHOD", request.method)

        # if request.method == "DELETE":

        author.delete()

        authors = Author.query.order_by(Author.id).all()
        
        return render_template("pages/authors.html", authors=authors, permissions=permissions)


# Create new book
    @app.route("/authors/create", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("post:author")
    def create_author(payload):

        permissions = payload["permissions"]
        author = Author(name="")
        form = AuthorForm()

        if request.method == "POST":
            form = AuthorForm(request.form, meta={'csrf': False})
        
            if form.validate_on_submit():
                
                form.populate_obj(author)

                author.insert()

            authors = Author.query.order_by(Author.id).all()

            return render_template("pages/authors.html", authors=authors, permissions=permissions)

        return render_template("forms/create_author.html", form=form)

        
  
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
    App.config['TEMPLATES_AUTO_RELOAD'] = True