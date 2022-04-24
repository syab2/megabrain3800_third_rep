from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class EditProfile(FlaskForm):
    icon = FileField('Profile picture', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    nickname = StringField('Nickname')
    about = TextAreaField('Обо мне:')
    birthday = StringField('День рождения:')
    submit = SubmitField("Изменить")
