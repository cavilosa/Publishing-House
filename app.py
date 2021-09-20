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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, expose_headers='Authorization')
    migrate = Migrate(app, db)
    setup_db(app)
    # db_drop_and_create_all()
    app.secret_key = os.environ["JWT_CODE_SIGNING_SECRET"]

    oauth = OAuth(app)

    auth0 = oauth.register(
    'auth0',
    client_id=os.environ["AUTH0_ID"],
    client_secret=os.environ["JWT_CODE_SIGNING_SECRET"],
    api_base_url='https://YOUR_DOMAIN',
    access_token_url='https://korzhyk-app.us.auth0.com/oauth/token',
    authorize_url='https://korzhyk-app.us.auth0.com/authorize',
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
       

    @app.route('/logout')
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {'returnTo': url_for('hello', _external=True), 'client_id': "a0mzLPX0PZ6KPWVGo058FFCUUNwShqIN"}
        return redirect('https://korzhyk-app.us.auth0.com' + '/v2/logout?' + urlencode(params))


    @app.route("/books", methods=["GET"])
    @cross_origin()
    @requires_auth("get:books")
    def books(payload):
        role =[]
        permissions = payload["permissions"]
        # if "patch:author" and "post:book" in permissions:
        #     role = ["coordinator"]
        # elif "delete:author" and "delete:book" in permissions:
        #     role = ["editor"]
        # else:
        #     role = ["reader"]

        books = Book.query.all()
        
        return render_template("pages/books.html", books=books, permissions=permissions)


    @app.route("/books/<id>", methods=["GET"])
    @cross_origin()
    @requires_auth("post:book")
    def book_by_id(payload, id):

        book = Book.query.get(id)

        permissions = payload["permissions"]

        return render_template("pages/book.html", book=book, permissions=permissions)


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


    @app.route("/books/create", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("post:book")
    def create_book(payload):

        permissions = payload["permissions"]
        book = Book(title="", author="", year=0)
        form = BookForm()

        if request.method == "POST":
            form = BookForm(request.form, meta={'csrf': False})
        
            if form.validate_on_submit():
                
                form.populate_obj(book)

                book.insert()

                books = Book.query.all()

            return render_template("pages/books.html", books=books, permissions=permissions)

        return render_template("forms/create_book.html", form=form)


        return render_template("forms/create_book.html", form=form)





    @app.route("/authors", methods=["GET"])
    @cross_origin()
    @requires_auth("get:authors")
    def authors(payload):

        role = ""
        permissions = payload["permissions"]

        if "patch:author" and "post:book" in permissions:
            role = "coordinator"
        elif "delete:author" and "delete:book" in permissions:
            role = "editor"
        else:
            role = "reader"

        authors = Author.query.all()
        
        return render_template("pages/authors.html", authors=authors, role=role)

    # @app.route("/books", methods=["GET"])
    # @requires_auth("get:books")
    # def list_books(payload):
        
    #     books = Book.query.all()
    #     books_list = [book.format() for book in books]
    #     return jsonify({
    #              "success": books_list
    #         })


    # @app.route("/authors", methods=["GET"])
    # @requires_auth("get:authors")
    # def list_authors(payload):
        
    #     authors = Author.query.all()
    #     authors_list = [author.format() for author in authors]
    #     return jsonify({
    #              "success": authors_list
    #         })

    # @app.route("/books/create", methods=["GET", "POST"])
    # @requires_auth("post:books") # use fetch(Ajax request) to avoid reloading the page and 
    # # adding new book to the list
    # def create_book(payload):
    #     # new_book = {}
    #     new_book = {
    #       "title": "NAME",
    #       "author": "author", 
    #       "year": 2000
    #     }
    #     # title = request.get_json()["title"]
    #     # author = request.get_json()["author"]
    #     # year = request.form.get["year"]
    #     # new_book = Book(title=book[title], author=book[author], year=book[year])
    #     # new_book.insert()
    #     # body["title"] = title
    #     # body["author"] = author
    #     # body["year"] = year
    #     # return redirect(url_for("books"))
    #     return jsonify(new_book)
        
  
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