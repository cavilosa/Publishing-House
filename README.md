# FULL STACK NANODEGREE CAPSTONE PROJECT

## <span style="color:blue">Publishing House Application</span>
-----------------
--------------------
This application is for the Publishing House usage. It has a database with books
and authors, as well as detailed information about them. At the landing page
a user is offered to log is in order to see/edit/delete books and authors.
*****************
## Roles
----------
---------------
There are 3 roles:
#### Reader
---------------
A reader can access a list of books and authors.

Permissions - get:authors, get:books

#### Coordinator
------------
Can see the details of books and authors, including a permission to modify and
create new entries.

Permissions - reader + patch:author, patch:book, post:author, post:book

#### Editor
----------------
Has the major access to all the data with the coordinator access plus permissions to delete books and authors.

Permissions - coordinator + delete:author, delete:book

## Authentification
_____________________
___________________

For the login purposes this app is using 3d party authentication: Auth0 servicese.
First, a user needs to sign up. That email needs to be asssigned to a role in the auth0 dashboard.
After the login auth0 returns a jwt token that is used for checking permissions.
Each route, except the landing page, requires specific auth0 permission. Depending on those permissions, links to various routes become available.

**Auth0 errors**: token_expired, invalid_claims, invalid_header.

## <span style="color:blue"> Routes </span>

All routes use render_template method to display the information. For testing purposes and possible further development, most of the routes are equipped with json object return if the request is of json type.

### Landign page
____________________________________
Offers to log in, if a sesssion token is available, redirects to the /callback route with the appropriate information displayed, according to the permisssions.
Also, logout button will crear session token and redirect to landign page.

### Main page
_____________________________________
Here the application will determine what permissions a user has: for a reader will display Books and Authors, as well as Logout and Main Page links.

For a coordinator and an editor there will be additional links to Add New Book and Annd New Author available as well as Edit Book and Edit Author in the detailed pages.

And only an editor will have Delete buttons for Books and Authors displayed when followed the links to a precise book or author.

### /books and /authors
_______________________________________________
For readers this route will display just a list of books and authors.

For editors and coordinators this route will add links to detailed information, as well as editing options.

Autho0 errors will be raised is the permission is not found.


### /books/id and /authors/id
________________________________________
A reader won't have access to this route.

Coordinator will see
- the details of the book, its author and a button to edit it
- author details, his books and a route to edit it

Editor will get additional buttons to delete the book or the author.

### /books/<id>/edit and /authors/<id>/edit
A reader won't have access to this route.

Book and Author form objects will populate the existing entry and pick up the changes, returning them to the database.


#### /books/create and /authors/create
A reader won't have access to this route.

Book and Author forms wil pick up user inputs and setore them in the databse, redirecting to the /books and /authors routes respectively.

Books can be created only with the authors from the database, so in order to add a new book, its author should be created already.






