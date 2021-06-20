from flask import Flask
from flask import request, redirect, url_for, render_template, flash, jsonify
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from functions import checkRole
import defs
from postControl import CheckBeforePost, addPostToDB, delPostFromDB
from showControl import toJson_and_delExtras, toJsonRole
from forms import LoginForm, RegisterForm, AddPostForm
from sqlalchemy import desc

import pymysql
import json
from dataBase import db

with open("config.json") as configFile:
    config = json.load(configFile)

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{us}:{psw}@localhost/{dbName}".format(
    psw=config['sqlLogin']['pass'], us=config['sqlLogin']['login'], dbName=config['sqlLogin']['dbName'])


app.config['SECRET_KEY'] = '$wf@@6QyxLo0PHpLq#4pEvTc7brcE%D#3E~RL|SOI$|Z1qn'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)
manager = LoginManager(app)
manager.login_view = "login_page"
manager.login_message = "Пожалуйста, войдите в аккаунт для продолжения"


def addUser(email, login, psw):
    try:
        user = defs.Users(email=email, username=login, password=psw)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('login_page'))
    except:
        print('ошибка добавления юзера')


@app.errorhandler(404)
def notFound(error):
    return render_template("error404.html")


@app.route('/admin')
@login_required
def admin():
    if not current_user.role == 'admin':
        return redirect(url_for('index'))

    return render_template("admin.html")


@app.route('/index')
@app.route('/')
def index():
    role = checkRole(current_user)
    return render_template("index.html", role=role)


@app.route('/add', methods=["POST", "GET"])
@login_required
def addPost():
    form = AddPostForm()
    condition, remaining_time = CheckBeforePost(current_user, form).get()

    if not condition:
        flash("Подождите {} секунд до следующей возможности добавить пост".format(remaining_time))

    if form.validate_on_submit():
        if not addPostToDB(form, current_user, app.root_path):
            flash('Оставьте хоть один контакт')
            return redirect(url_for('addPost'))
        return redirect(url_for('index'))

    return render_template('addPost.html', form=form, condition=condition)


@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(defs.Users).filter_by(username=form.username.data).first()
        if user is None:
            addUser(form.email.data, form.username.data, form.password.data)
            return redirect(url_for('login_page'))

        else:
            flash('Неверные данные')

    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(defs.Users).filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('index'))

        else:
            flash('Неверные данные')

    return render_template("login.html", form=form)


@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@manager.user_loader
def load_user(user_id):
    return db.session.query(defs.Users).get(user_id)


@app.route('/ajax/deletePost', methods=["POST", "GET"])
@login_required
def deletePost():
    if current_user.role == 'admin':

        if request.method == "POST":
            post_id = request.form['id']
            post = db.session.query(defs.Posts).get_or_404(post_id)
            delPostFromDB(post)
            return jsonify()

    return redirect(url_for('index'))


@app.route('/ajax/showPosts', methods=["POST", "GET"])
def showPosts():
    COUNT_POSTS = config['settings']['COUNT_POSTS']
    if request.method == "GET":
        count = int(request.args.get('count'))
        data = []
        rawPosts = db.session.query(defs.Posts).order_by(desc(defs.Posts.id)).limit(COUNT_POSTS * count)
        data.append(toJson_and_delExtras(rawPosts, count))
        data.append(toJsonRole(checkRole(current_user)))

        return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
