from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField('Обо мне')
    birthday = StringField('Дата рождения(ДД.ММ.ГГГГ)', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
