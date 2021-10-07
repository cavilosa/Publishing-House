# FULL STACK NANODEGREE CAPSTONE PROJECT

## <span style="color:blue">Publishing House Application</span>
-----------------
--------------------
Publishing House application can be used to store authors and books data for edition purposes.
This Final Project demonstrates my skills in:
- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## Project Dependencies:

Python 3.9.5 from <a href="https://www.python.org/downloads/">Official website</a>

pip 21.1.1 from <a href="https://pypi.org/project/pip/">Official website</a>

Create <a href="https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/">virtual environment</a> for the application:

    python3 -m venv env

Activate virtual environment with command:

    source env/bin/activate

To deactivate:

    deactivate

In the virtual environment install project dependencies from the requirements.txt file with pip command:

    pip install -r requirements.txt

Export environment variables with:

    source setup.sh

Start the postgresql server on ubuntu:

    sudo service postgresql start

Now we need to create main and test databases:

    sudo -u postgres createdb publishing_house

    sudo -u postgres createdb test

Psql users and passwords can be edited in the setup.sh file.

Locally, the application will run on <a href="localhost:5000/">localhost:5000/</a>

Production version URL is hosted on <a href="https://fsnd-capstone-publishing-house.herokuapp.com/">https://fsnd-capstone-publishing-house.herokuapp.com/</a>

## <span style="color:blue">Roles</span>
----------
There are 3 roles:

**Reader** can access a list of books and authors.
Permissions - *get:authors, get:books*.

**Coordinator** c an see the details of books and authors, including a permission to modify and
create new entries.
Permissions - *reader + patch:author, patch:book, post:author, post:book*.

**Editor** has the major access to all the data with the coordinator access plus permissions to delete books and authors.
Permissions - *coordinator + delete:author, delete:book*.

#### Start the development server

From the main folder with app.py file run the command:

    export FLASK_APP=app && export FLASK_ENV=development && flask run --reload

## Authentication
_____________________

For the login purposes this app is using 3d party authentication: Auth0 services.
First, a user needs to sign up. That email needs to be assigned to a role in the auth0 dashboard.
After the login auth0 returns a jwt token that is used for checking permissions.
Each route, except the landing page, requires specific auth0 permission. Depending on those permissions, links to various routes become available.

## Sign in and JWT information
________________

To sigh in as a *reader*:

email: reader@gmail.com
password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjY3M2NiZDI3MDAwNjlmODg3NGIiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM4ODg2LCJleHAiOjE2MzM3MDg4ODYsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIl19.BZgHspyLL6M24hC7lhaOmTZXFoe3htgBBQL1sz2LZ4Hv0YxcHZsr9-MqOB9n-1-eCp__fuQ2n-1GHFQIyXp-udNQ4frLJrvmDv-mNwn7uhO51t8v7DfSqV70CR_RxbeZahImdNOnzr--NF5z133bE4fBEZ-9Ffn8jomkv-Q5WgtYOXnAa5P-Ma_O9S5Ti9rAJHDQCDKuLlYHDON7aRaLTuP3sR6egyAevFJf37YqZJjDzzS17lJbvg9dh1jg_SNWGN_s7bDDWBvuIkYlXv4xqwLMb7ilDnBDq7EzMXZ1VUL2wq2wmDgmNOYxkkxFdfiBRGES2U5QgWXjWcTvQuimdQ"

as a *coordinator*:

email: coordinator@gmail.com
password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjU0ZTYzNzYyYzAwNzBiZmU2MTgiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM4OTMyLCJleHAiOjE2MzM3MDg5MzIsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.GlmyKBZZ0jVH4Scq8IDh1eUD3nirJUbriqXT5L32_P6gMx9xaj4_V0NT7V0cjPaUuVcgVm-v4CZ1VX6M79wJMldcAEzJwIPZEQa4oyBTyAhAlQ-e9jT4x06JN35bMAn3d_yg5mZTccMCK0HyvDN1VbR4yCm2k7QBEr1lgsw4VZn2pvCTW6ep7_oj68eYV3yszUZtWc4eJqjM3_PMEv04BfEAP1cHD-BOvy5FfiosiIhpMGVs--HxAkhkHyuYcvZdhfE3Dw3T9j1ctcDkMcPQMv4jH78Hh8ALT4QmXhOfG6HLWr2u5A_DBfE_f8XNiGgefpeCrINp5EbwXrSRy_7Ciw"

as an *editor*:

email: editor@gmail.com
password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNTM5MDQwLCJleHAiOjE2MzM3MDkwNDAsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.d_TIhbtzX4tbe6Tr3A4bOTejivYsuFBn5vXfNw0G9KFOgdscPBw9jkxuJzfOAjhR5NiGnIUxVSioRrmmiJ854AELA4YQ8lrUgc7MLpk-M3bUs9IH8p32ml-n3fox3EPLyjnCmsSDHl146ITjp7_s0EKFrGOvo9AkE7XUXCvv-rMTSuPujWBGZdvxMS0JlSkEBJX7hBD1HYNAWQu_szP1aWI5OzyEwqSUjtSvwWqzZ9GfJia3QXHT9hf0hyqvX757UCK9necMez7hpKpICfRpx4YIpElEIf53JI5ddRvVqHdj8oSCQBsukOpbBleh9h6s6eWMiekME9Jdi5tCryK4lA"


## <span style="color:blue"> Routes </span>

All routes use render_template method to display the information. For testing purposes and possible further development, most of the routes are equipped with json object return if the request is of json type.

### Landing page
____________________________________
Offers to log in, if a session token is available, redirects to the /callback route with the appropriate information displayed, according to the permissions.
Also, logout button will clear session token and redirect to landing page.

### Main page after login
_____________________________________
Here the application will determine what permissions a user has: for a reader will display Books and Authors, as well as Logout and Main Page links.

For a coordinator and an editor there will be additional links to Add New Book and Add New Author available as well as Edit Book and Edit Author in the detailed pages.

And only an editor will have Delete buttons for Books and Authors displayed when followed the links to a precise book or author.

### /books and /authors, methods = GET
_______________________________________________
For readers this route will display just a list of books and authors.

For editors and coordinators this route will add links to detailed information, as well as editing options.

Autho0 error will be raised if the permission is not found.

JSON response will include:

        {
            "success": True,
            "books": list // "authors": list
        }


### - /books/id and /authors/id, methods = GET
________________________________________
A reader won't have access to this route.

Coordinator will see
- the details of the book, its author and a button to edit it
- author details, his books and a route to edit it

Editor will get additional buttons to delete the book or the author.

If the book or author id is not in the database, 422 error will raised.

JSON response will include:

        {
           "success": True,
           "book": book.format() // "author": author.format()
        }


### - /books/id/edit and /authors/id/edit, methods = GET, POST
_______________________________________
A reader won't have access to this route. Auth0 will raise error if authorization header is missing.

Book and Author form objects will be populated with  the existing entry on GET request.
POST method will pick up the new data and return it to the database, updating the entry with the corresponding id.

If the book or author id is not in the database, 422 error will raised.

JSON response for POST request will include:

        {
          "success": True,
          "book": book.format() // "author": author.format()
        }

JSON response for GET request will include:

        {
          "success": True,
          "permissions": permissions
        }


### - /books/create and /authors/create, methods = GET, POST
_________________________________________
A reader won't have access to this route.

On GET request a BookForm or AuthorFrom will loaded with JSON response for GET request will include:

        {
          "success": True,
          "permissions": permissions
        }

On POST request the forms wil store user's input in the database, redirecting to the /books and /authors routes respectively.

JSON response for GET request will include:

        {
          "success": True,
          "author": author.format() // "book": book.format
        }

Books can be created only with the authors from the database, so in order to add a new book, its author should be created already. If the author is not in the database, 404 error will raised.

### - /books/id/delete and /authors/id/delete, methods = GET, POST
This route authorized only for the editor role.

If the book or author id is not in the database, 404 error will raised. And return JSON object

    {
            "success": False
    }

On successful deletion JSON object will be returned:

    {
        "success": True,
        "book": book.format(),  // "author": author.format()
        "permissions": permissions
    }


## <span style="color:blue"> ERRORS </span>

**Auth0 errors**: token_expired, invalid_claims, invalid_header.

**Application** errors:
- 400:Bad Request. The server couldn't process your request,
- 404:You are trying to access an item that is not in the database.
The server can not find the requested resource.,
- 422:The request was well-formed but was unable to be followed due to semantic errors. The server couldn't process your request.
- 500:Internal server error. The server has encountered a situation it doesn't know how to handle.


## <span style="color:blue"> Tests </span>

Testing is done with uniitest library, to run the tests:

    python test_app.py

Tests check all endpoints for success and fail behaviours, as well as for RBAC with appropriate permissions and withut them.
