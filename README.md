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

    pip3 install -r requirements.txt

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

**Coordinator** can see the details of books and authors, including a permission to modify and
create new entries.
Permissions - *reader + patch:author, patch:book, post:author, post:book*.

**Editor** has the major access to all the data with the coordinator access plus permissions to delete books and authors.
Permissions - *coordinator + delete:author, delete:book*.

#### Start the development server

From the main folder with app.py file run the command on Lunix:

    export FLASK_APP=app && export FLASK_ENV=development && flask run --reload

On Windows:

    set FLASK_APP=app
    set FLASK_ENV=development
    set flask run --reload

## Authentication
_____________________

For the login purposes this app is using 3d party authentication: Auth0 services.
First, a user needs to sign up. That email needs to be assigned to a role in the auth0 dashboard.
After the login auth0 returns a jwt token that is used for checking permissions.
Each route, except the landing page, requires specific auth0 permission. Depending on those permissions, links to various routes become available.

## Sign in and JWT information
________________

To sign in as a *reader*:

email: reader@gmail.com

password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTVlMjMwZWZlMzliYjAwNjkyMTJkMTQiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNzA2MDU2LCJleHAiOjE2MzM4NzYwNTYsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIl19.gSMRYg6-VoPHH1sb2L-koWeiGHPjBvCRdxw2rHGDX4YKiRbURAptgseTZeftTLmfYzNcikVzacjThf6RUPIcZB_Qmaouo_wjxNQnubCttV_YqaRSRvkBjB4Cms4yLx6n5m7SLlfBl4BQSmVva1VtnU9irdbduRRVGO6u5zU6XBsiGw4zX8yes-lI-CE_RmvvWKTSBkyrVPNUiYz6-BYncVYOZU7eXKSof7Ve4wMPBV1p5PKXvv6YcAH-8cTOyzl1n6d6UKMaI8kMRmSrnJhwhW8ahv3ehuPViOUoQyEjdgyom8yoaSUj6TN87ez41a2ekUZAsCHHXuz0OQrLKxy80A"

as a *coordinator*:

email: coordinator@gmail.com

password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTVlMjM4YWZmODZmNjAwNmEzNTc0OTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNzA2MTYwLCJleHAiOjE2MzM4NzYxNjAsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.Z8Os8aPvbNaiKF7EKaxfT4FxYFDtDf44t7hPUwx7pkHil_sFoljji8cd1igd5QkHXvkp3wiZ8HNb5Y9pvBGJRit4YxUSmqi8ft1a4sfnWjqV7jY9MkKwiR8x0kYSGwqo3systVz9whgucS5bfqpja8pfCuVqta_fv85o52X35iaSahGFbElLcwo40fQCJ4925KIqzOIFa4sKAe0RLUsYcQVhHnJ54hFUEZ2U987CXw98eMxV2Yy7hDHIdZ_MvYrWo59-sqYzY5cOynLFM6WJDNtbTf1CNTCmk0Dvhxi5kPo6suMQTXoIZmmbh-fi5UeK5BTYrqcWSznk_IbcG6ihBw"

as an *editor*:

email: editor@gmail.com

password: Capstone1#

Valid JWT token is:
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMzNjI2NTk1LCJleHAiOjE2MzM3OTY1OTUsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.ksM1EXcMQ7TGXGZ9lAWu8mvDS6mE5yvca8tHSXlSnz5TAGnDeulooOu_2tzS0PO8F9-UPO0AomHoEtd_QkCblM9rf9m-2E4Ti4Lw2tywavuz7KqAqe3bmSgnTIUZPJCnUuO1dZG5EVbmIfXTtTyDwewbajzaYKeBSE0li93ai_3a7BHl-H9ayzLpET7tQIIOxcigNiJ6T6dCLC2yAcNpFqXAtEKkCdD1vHHxrO2HjwdFoXGY-nVqzGuUBA1tC0wLBIdxOTko9M018mN99w2FUONDs3Ag601qp8xmgRXB2RzwXkIb2MytgZIMeLxReq_sA9ElSW6guHerSB9rtctHpQ"


## <span style="color:blue"> Routes </span>

All routes use render_template method to display the information. For testing purposes and possible further development, most of the routes are equipped with json object returned if the request is of json type.

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

If the book or author id is not in the database, 422 error will be raised.

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

On GET request a BookForm or AuthorFrom will be loaded, JSON response for GET request will include:

        {
          "success": True,
          "permissions": permissions
        }

On POST request the forms will store user's input in the database, redirecting to the /books and /authors routes respectively.

JSON response for POST request will include:

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

Testing is done with unittest library, to run the tests:

    python test_app.py

Tests check all endpoints for success and fail behaviours, as well as for RBAC with appropriate permissions and withut them.


## <span style="color:blue"> PYCODESTYLE </span>

To check for pep8 errors I used pycodestyle library, excluding autogenerated folders:

    pycodestyle . --exclude=/migrations,env

For cleating the errors I ran authopep8 program on each python file:

    autopep8 --in-place --aggressive --aggressive <file_name>.py

