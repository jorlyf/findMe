from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Логин ', validators=[DataRequired()])
    password = PasswordField('Пароль ', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Email ', validators=[Email()])
    username = StringField('Логин ', validators=[DataRequired()])
    password = PasswordField('Пароль ', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Зарегистрироваться')


class AddPostForm(FlaskForm):
    head = StringField('Заголовок ', validators=[DataRequired(), Length(max=40)])
    description = TextAreaField('Описание ', validators=[DataRequired(), Length(max=300)])
    vk = StringField('vk ')
    instagram = StringField('instagram ')
    otherContacts = StringField('instagram ')
    image = FileField('Фото ')
    submit = SubmitField('Создать ')
