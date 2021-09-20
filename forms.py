from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms.validators import InputRequired, AnyOf, URL

class BookForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    author = StringField("author", validators=[DataRequired()])
    year = IntegerField("year", validators=[DataRequired()])
    send = SubmitField('send')

class AuthorForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    send = SubmitField('send')