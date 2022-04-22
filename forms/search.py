from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    text = StringField('')
    submit = SubmitField('Search')