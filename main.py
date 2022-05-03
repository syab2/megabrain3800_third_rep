import os
import shutil
from distutils.dir_util import copy_tree
from flask import Flask, render_template, redirect, request, url_for, abort, make_response, jsonify
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

import random

from data.api import blueprint
from data import db_session
from data.users import User
from data.games import Game
from data.edit import EditProfile

from forms.search import SearchForm
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.game import GameForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile')
def profile():
    search = SearchForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    games_qty = db_sess.query(Game).filter(Game.user_id == current_user.id).all()
    return render_template('profile.html', title='Профиль', search=search, user=user, games_qty=len(games_qty))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    db_sess = db_session.create_session()
    games = db_sess.query(Game).all()
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    try:
        user = db_sess.query(User).filter(User.id == current_user.id)
        return render_template('index.html', user=user, current_user=current_user, games=games, search=search, title='Главная')
    except Exception:
        return render_template('index.html', current_user=current_user, games=games, search=search, title='Главная')
        


@app.route('/register', methods=['GET', 'POST'])
def register():
    search = SearchForm()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, search=search,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) | (User.nickname == form.nickname.data)).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, search=search,
                                   message="Такой пользователь уже есть")
        user = User()
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.icon = '/static/img/user-icon.png'
        user.about = form.about.data
        user.birthday = form.birthday.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('register.html', title='Регистрация', search=search, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    search = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль", search=search,
                               form=form)
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('login.html', title='Авторизация', search=search, form=form)


@app.route('/add_game', methods=["GET", "POST"])
@login_required
def add_game():
    form = GameForm()
    search = SearchForm()
    count = 3
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = Game()   

        if len(str(form.title.data).strip()) <= 40:
            game.title = str(form.title.data).strip()
        else:
            game.title = str(form.title.data).strip()[:40]

        if len(str(form.description.data).strip()) <= 80:
            game.description = str(form.description.data).strip()
        else:
            game.description = str(form.description.data).strip()[:80]

        os.mkdir(f'static/games/{game.title}')
        os.mkdir(f'static/games/{game.title}/images')

        filename = str(''.join([str(random.randint(1, 9)) for x in range(5)])) + '_' + str(secure_filename(form.icon.data.filename))
        form.icon.data.save(f'static/games/{game.title}/images/{filename}')
        game.icon = url_for('static', filename=f'games/{game.title}/images/{filename}')

        filename1 = str(''.join([str(random.randint(1, 9)) for x in range(5)])) + '_' + str(secure_filename(form.archive.data.filename))
        form.archive.data.save(f'static/games/{game.title}/{filename1}')
        game.archive = url_for('static', filename=f'games/{game.title}/{filename1}')
        try:
            form.slide1.data.save(f'static/games/{game.title}/images/slide1.jpg')
        except Exception:
            count -= 1

        try:
            form.slide2.data.save(f'static/games/{game.title}/images/slide2.jpg')
        except Exception:
            count -= 1

        try:
            form.slide3.data.save(f'static/games/{game.title}/images/slide3.jpg')
        except Exception:
            count -= 1

        game.slides = ';'.join([url_for('static', filename=f'games/{game.title}/images/slide{x + 1}.jpg') for x in range(count)])

        current_user.games.append(game)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    if search.validate_on_submit() and not form.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('game_add.html', form=form, search=search, title='Добавление игры')


@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    search = SearchForm()
    form = EditProfile()
    if request.method == 'GET':     
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        form.nickname.data = user.nickname
        form.about.data = user.about
        form.birthday.data = user.birthday
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.nickname = form.nickname.data
        user.about = form.about.data
        user.birthday = form.birthday.data
        filename = str(''.join([str(random.randint(1, 10)) for x in range(5)])) + '_' + str(secure_filename(form.icon.data.filename))
        form.icon.data.save(f'static/img/{filename}')
        user.icon = url_for('static', filename=f'img/{filename}')
        db_sess.commit()
        return redirect('/profile')
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('edit_profile.html', form=form, search=search, title='Редактирование профиля', user=user)


@app.route('/game/<int:id>', methods=['GET', 'POST'])
def game_page(id):
    search = SearchForm()
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == id).first()
    author = db_sess.query(User).filter(User.id == game.user_id).first()
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('game_page.html', search=search, game=game, username=author)


@app.route('/edit-game/<int:id>', methods=['GET', "POST"])
@login_required
def edit_game(id):
    form = GameForm()
    search = SearchForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id).first()
        form.icon.data = game.icon
        form.title.data = game.title
        form.description.data = game.description
        form.archive.data = game.archive
    if form.is_submitted():
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id).first()

        try:
            dirr = '_'.join(form.title.data.split())
            os.mkdir(f'static/games/{dirr}')
            os.mkdir(f'static/games/{dirr}/images')
            copy_tree(f'static/games/{game.title}/images', f'static/games/{dirr}/images')
            shutil.rmtree(f'static/games/{game.title}')
        except Exception:
            pass

        game.title = '_'.join(str(form.title.data).strip().split())
        game.description = str(form.description.data).strip()

        filename = str(''.join([str(random.randint(1, 9)) for x in range(5)])) + '_' + str(secure_filename(form.icon.data.filename))
        form.icon.data.save(f'static/games/{game.title}/images/{filename}')
        game.icon = url_for('static', filename=f'games/{game.title}/images/{filename}')

        filename1 = str(''.join([str(random.randint(1, 9)) for x in range(5)])) + '_' + str(secure_filename(form.archive.data.filename))
        form.archive.data.save(f'static/games/{game.title}/{filename1}')
        game.archive = url_for('static', filename=f'games/{game.title}/{filename1}')

        db_sess.commit()
        
        return redirect('/')
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    return render_template('edit_game.html', form=form, search=search)


@app.route('/delete-game/<int:id>')
@login_required
def gelete_game(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == id).first()

    if game:
        db_sess.delete(game)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/search/<title>', methods=['GET', "POST"])
def search(title):
    search = SearchForm()
    db_sess = db_session.create_session()
    game_id = db_sess.query(Game).filter(Game.title.like(f'%{title}%')).all()
    if search.validate_on_submit():
        return redirect(f'/search/{search.text.data}')
    if game_id:
        return render_template('index.html', search=search, games=game_id)
    else:
        return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init('db/mega.db')
    app.register_blueprint(blueprint)
    app.run()


if __name__ == '__main__':
    main()
