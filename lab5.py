from flask import Blueprint, request, render_template, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    username = session.get('login', 'Anonymous') 
    return render_template('lab5/lab5.html', username=username)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
        host='127.0.0.1',
        database='vika_smirnova_base',
        user='vika_smirnova_base',
        password='2507'
    )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    password_hash = generate_password_hash(password)
    cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    cur.execute ("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (login, )) 
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Заполните все поля")

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", (login_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()['id']

    cur.execute("""
        SELECT id, title, article_text, is_favorite
        FROM articles
        WHERE user_id=%s
        ORDER BY is_favorite DESC, id ASC;
    """, (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article, error="Заполните все поля")

        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
        db_close(conn, cur)
        return redirect('/lab5/list')

    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    db_close(conn, cur)

    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()

    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    cur.execute("""
        SELECT id, title, article_text, user_id
        FROM articles
        WHERE is_public=TRUE
        ORDER BY id ASC;
    """)
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

@lab5.route('/lab5/toggle_favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("SELECT is_favorite FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    new_favorite_value = not article['is_favorite']

    cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_favorite_value, article_id))
    db_close(conn, cur)

    return redirect('/lab5/list')
