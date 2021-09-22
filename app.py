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
from flask import session, abort

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
        session.pop('_flashes', None)
        return response


# Initial route to authorize with auth0
# -------------------------------------------------------------------------------------------
#
    @app.route("/", methods=["GET"])
    def index():

        if session.get("token"):
            # print("TOKE", session.get("token"))
            return redirect("/callback")
        else:
            login = True
            return render_template("layouts/main.html", login=True)


    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri="http://localhost:5000/callback", audience="app")


    @app.route('/callback')
    def callback_handling():
        # check if a user is logged in
        if session.get("token"):
            token = session["token"]
        else:
            token = auth0.authorize_access_token()
            session['token'] = token['access_token']
            token = token['access_token']
        
        payload = verify_decode_jwt(token)

        permissions = payload["permissions"]
        
        if "delete:author" and "delete:book" in permissions:
            flash('You were successfully logged in as an editor')
            return render_template('layouts/main.html', permissions=permissions, token=True)

        elif "patch:author" and "post:book" in permissions:
            flash('You were successfully logged in as a coordinator')
            return render_template('layouts/main.html',permissions=permissions, token=token)

        elif "get:book" and "get:authors" in permissions:
            flash('You were successfully logged in as a reader')
            return render_template('layouts/main.html', permissions=permissions,  token=True) 

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
        permissions = payload["permissions"]
        try:
            books = Book.query.order_by(Book.id).all()
        
        except:
            flash("No books were found in the database")
        
        return render_template("pages/books.html", books=books, permissions=permissions)


# See a book by it's id
    @app.route("/books/<id>", methods=["GET"])
    @cross_origin()
    @requires_auth("post:book")
    def book_by_id(payload, id):
        try:
            book = Book.query.get(id)

            permissions = payload["permissions"]
            item = {}
            for author in book.authors:
                item = {
                    "id": author.id
                }

        except:
            flash(f"The book with id {id} doesn't exist.")
            abort(422)

        return render_template("pages/book.html", book=book, permissions=permissions, author=item)


# Edit a book by it's id
    @app.route("/books/<id>/edit", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("patch:book")
    def edit_book(payload, id):
        book = Book.query.get(id)
        if book is None:
            flash("You are trying to access a book with nonexisting id")
            abort(422)
        permissions = payload["permissions"]
        form = BookForm(obj=book)

        if request.method == "POST":
            form = BookForm(request.form, meta={'csrf': False})
            book = Book.query.get(id)
            if book is None:
                flash("You are trying to access a book with nonexisting id")
                abort(422)
            
            if form.validate_on_submit():
                form.populate_obj(book)
                try:
                    book.update()
                    flash("Successfully updated the book")
                except:
                    flask("Something went wrong and the book was not updated.")
                    abort(400)

            return render_template("pages/book.html", book=book, permissions=permissions)

        return render_template("forms/edit_book.html", form=form, permissions=permissions)


# Create new book
    @app.route("/books/create", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("post:book")
    def create_book(payload):

        permissions = payload["permissions"]
        book = Book(title="", author="", year=0)
        authors = Author.query.all()
        if authors is None:
            flash("We couldn't retrieve the authors from the database.")
            abort(404)
        form = BookForm()

        if request.method == "POST":
            form = BookForm(request.form, meta={'csrf': False})

            name = request.form.get("author")

            author=Author.query.filter_by(name=name).first()
            if author is None:
                flash("The author wasn't found in the library. Need to create an author first.")
                abort(404)
        
            if form.validate_on_submit():
                
                form.populate_obj(book)

                book.authors.append(author)

                try:
                    book.insert()
                    flash("The book has beed added successfully.")
                except:
                    flash("We couldn't add new book to the database")
                    abort(400)

                try:
                    books = Book.query.order_by(Book.id).all()
                except:
                    flash("Couldn't get books from the database.")
                    abort(404)

                return render_template("pages/books.html", books=books, permissions=permissions, authors=authors)

        return render_template("forms/create_book.html", form=form, authors=authors, permissions=permissions)


    # Delete book by it's id
    @app.route("/books/<id>/delete", methods=["GET", "POST"])
    @cross_origin()
    @requires_auth("delete:book")
    def delete_book(payload, id):
        try: 
            book = Book.query.get(id)
            permissions = payload["permissions"]

            book.delete()
            flash("The book was seccusfully deleted.")
            try:
                books = Book.query.order_by(Book.id).all()
            except:
                flash("Couldn't get the books from the database.")
                abort(500)
            
            return render_template("pages/books.html", books=books, permissions=permissions)
        except:
            flash(f"The is no book with id {id}.")
            abort(404)

#------------------------------------------------------------------------------------------
# Authors
#------------------------------------------------------------------------------------------

    @app.route("/authors", methods=["GET"])
    @cross_origin()
    @requires_auth("get:authors")
    def authors(payload):

        permissions = payload["permissions"]
        try:
            authors = Author.query.order_by(Author.id).all()
        except:
            flash("The authors list couldn't been retreived.")
            abort(404)
        
        return render_template("pages/authors.html", authors=authors, permissions=permissions)


    @app.route("/authors/<id>", methods=["GET"])
    @cross_origin()
    @requires_auth("post:author")
    def author_by_id(payload, id):
        try:
            author = Author.query.get(id)
  
            books = []

            for book in author.books:
                item = {
                    "title": book.title,
                    "year": book.year
                }
                books.append(item)   

            permissions = payload["permissions"]

        except:
            flash("There is no such author in the database.")
            abort(404)

        return render_template("pages/author.html", author=author, permissions=permissions, books=books)


# Edit a book by it's id
    @app.route("/authors/<id>/edit", methods=["POST", "GET"])
    @cross_origin()
    @requires_auth("patch:author")
    def edit_author(payload, id):

        author = Author.query.get(id)
        if author is None:
            flash("There is no such author in the database")
            abort(422)
        permissions = payload["permissions"]
        form = AuthorForm(obj=author)

        if request.method == "POST":
            form = AuthorForm(request.form, meta={'csrf': False})
            author = Author.query.get(id)
                
            if form.validate_on_submit():

                form.populate_obj(author)
                author.update()
            return render_template("pages/author.html", author=author, permissions=permissions)
       
        return render_template("forms/edit_author.html", form=form, permissions=permissions)
        

# DELETE author by id

    @app.route("/authors/<id>/delete", methods=["GET", "POST"])
    @cross_origin()
    @requires_auth("delete:author")
    def delete_author(payload, id):

        author = Author.query.get(id)
        if author is None:
            flash("There is no such author in the database")
            abort(422)
        permissions = payload["permissions"]
        try:
            author.delete()
            flash("The authro was deleted successfully.")
        except:
            flash("Couldn't delete the author")
            abort(422)

        try:
            authors = Author.query.order_by(Author.id).all()
        except:
            flash("Something went wrong.")
            abort(404)
        
        return render_template("pages/authors.html", authors=authors, permissions=permissions)


# Create new author
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
                try:
                    author.insert()
                    flash("The author was added successfully.")
                except:
                    flash("Couldn't add a new author to the database.")
                    abort(500)
            try:
                authors = Author.query.order_by(Author.id).all()
            except:
                flash("Couldn't process your request")
                abort(404)

            return render_template("pages/authors.html", authors=authors, permissions=permissions)

        return render_template("forms/create_author.html", form=form, permissions=permissions)


#----------------------------------------------------------
# Errorhandlers
#----------------------------------------------------
        
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

      # Handlers for all expected errors

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html")

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("errors/400.html")

    @app.errorhandler(422)
    def unprocessable(error):
        return render_template("errors/422.html")

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html")

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
    App.config['TEMPLATES_AUTO_RELOAD'] = True