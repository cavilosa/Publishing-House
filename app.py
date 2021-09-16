import os
from flask import Flask, request, abort, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from flask_cors import CORS
import json
from dotenv import load_dotenv
from models import db, setup_db,  Book, Author # authors_books, #db_drop_and_create_all
from auth.auth import AuthError #, requires_auth
from flask_migrate import Migrate
# from .auth.auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask import session

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
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

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    #     return response


    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if constants.PROFILE_KEY not in session:
                return redirect('/login')
            return f(*args, **kwargs)
 
        return decorated

    @app.route("/", methods=["GET"])
    def hello():
        return render_template("layouts/main.html")
        # return render_template("pages/books.html")
        # return redirect ("https://korzhyk-app.us.auth0.com/authorize?audience=app&response_type=token&client_id=a0mzLPX0PZ6KPWVGo058FFCUUNwShqIN&redirect_uri=http://localhost:8080/login-results")


    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri="http://localhost:5000/callback", audience="app")


    @app.route('/callback')
    def callback_handling():
        token = auth0.authorize_access_token()['access_token']

        session['token'] = token
        print("TOKEN", token)
        
        return render_template('layouts/main.html', token=token)

    @app.route('/logout')
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {'returnTo': url_for('hello', _external=True), 'client_id': "a0mzLPX0PZ6KPWVGo058FFCUUNwShqIN"}
        return redirect('https://korzhyk-app.us.auth0.com' + '/v2/logout?' + urlencode(params))


    # @app.route('/dashboard')
    # @requires_auth
    # def dashboard():
    #     return render_template('layouts/main.html',
    #                         userinfo=session[constants.PROFILE_KEY],
    #                         userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))



    


    # @app.route("/books", methods=["GET"])
    #     return render_template("books.html", books=Books.query.all)

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