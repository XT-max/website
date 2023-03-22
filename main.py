
import datetime
import os
import sqlite3

from flask import Flask, render_template, flash, request, abort, g

from config import Config
from fdatabase import FDataBase

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Соединение с БД, если оно еще не установленно"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/post', methods=['POST', 'GET'])
def post():
    db = get_db()
    database = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['post']) > 10:
            res = database.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('post.html', title='Добавить статью', menu=database.getMenu())


@app.route('/allposts')
def allposts():  # put application's code here
    db = get_db()
    database = FDataBase(db)
    return render_template('allposts.html', title='Cписок постов', menu=database.getMenu(),
                           posts=database.getPostAnnoce())


@app.route('/posts/<int:id_post>')
def showPost(id_post):  # put application's code here
    db = get_db()
    database = FDataBase(db)
    title, aticle = database.getPost(id_post)
    if not title:
        abort(404)
    return render_template('aticle.html', title='title', menu=database.getMenu(), post=aticle)


@app.route('/')
def index1():  # put application's code here
    db = get_db()
    database = FDataBase(db)
    return render_template('main.html', title='1', menu=database.getMenu())


@app.route('/history')
def index2():
    db = get_db()
    database = FDataBase(db)
    return render_template('history.html', menu=database.getMenu())


if __name__ == '__main__':
    app.run(debug=True)
