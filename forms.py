from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms.validators import InputRequired, AnyOf, URL

class BookForm(FlaskForm):
    title = StringField("TITLE", validators=[DataRequired()])
    author = StringField("AUTHOR", validators=[DataRequired()])
    year = IntegerField("YEAR", validators=[DataRequired()])
    send = SubmitField('send')

class AuthorForm(FlaskForm):
    name = StringField("NAME", validators=[DataRequired()])
    send = SubmitField('send')