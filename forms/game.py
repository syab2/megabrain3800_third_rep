from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    icon = FileField('Icon of game', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'ico'], 'Images only!')])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField("Description")
    archive = FileField('Archive with game', validators=[FileRequired(), FileAllowed(['zip'], 'Archives only!')])
    slide1 = FileField('Screenshots from the game', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'ico'], 'Images only!')])
    slide2 = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'ico'], 'Images only!')])
    slide3 = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'ico'], 'Images only!')])
    submit = SubmitField('Submit')
