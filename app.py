import os
from flask import Flask, request, abort, jsonify, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from flask_cors import CORS, cross_origin
import json
from dotenv import load_dotenv
from models import db, setup_db,  Book, Author # authors_books, #db_drop_and_create_all
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
    def hello():
        # print ("SESSION", session)
        # if session["token"]:
        #     return redirect("/callback")
        # else:
        return render_template("layouts/main.html")


    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri="http://localhost:5000/callback", audience="app")


    @app.route('/callback')
    def callback_handling():
        # if session["token"]:
        #     print("SESSION TOKEN", session["token"])
        #     token = session["token"]
        # else:
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        token = token['access_token']
        
        payload = verify_decode_jwt(token)

        permissions = payload["permissions"]
        permission = ""
        if "delete:author" and "delete:book" in permissions:
            # flash('You were successfully logged in as an editor')
            return render_template('layouts/main.html', permission="editor")

        elif "patch:author" and "post:book" in permissions:
            # flash('You were successfully logged in as a coordinator')
            return render_template('layouts/main.html', permission="coordinator")

        elif "get:book" and "get:authors" in permissions:
            # flash('You were successfully logged in as a reader')
            return render_template('layouts/main.html', permission="reader") 

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
        print ("SESSION TOKEN /BOOKS", session["token"])

        return render_template("pages/books.html")

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