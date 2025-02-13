from flask import Blueprint, render_template, request, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vika_smirnova_base',
            user='vika_smirnova_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
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

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        return {"error": "Film not found"}, 404
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    film = request.get_json()

    # Проверки для полей
    errors = {}

    # Проверка русского названия
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название не может быть пустым'

    # Проверка оригинального названия
    if not film.get('title') and not film.get('title_ru'):
        errors['title'] = 'Название на оригинальном языке не может быть пустым, если русское название тоже пустое'

    # Проверка года
    if not film.get('year'):
        errors['year'] = 'Год выпуска не может быть пустым'
    else:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'

    # Проверка описания
    if not film.get('description'):
        errors['description'] = 'Описание не может быть пустым'
    elif len(film['description']) > 2000:
        errors['description'] = 'Описание не может быть длиннее 2000 символов'

    # Если есть ошибки, возвращаем их
    if errors:
        return jsonify(errors), 400

    # Если оригинальное название пустое, используем русское название
    if not film.get('title'):
        film['title'] = film['title_ru']

    try:
        cur.execute("UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;",
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
        db_close(conn, cur)
        return jsonify(film), 200
    except Exception as e:
        db_close(conn, cur)
        return {'error': f'Ошибка при обновлении фильма: {str(e)}'}, 500

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    film = request.get_json()

    # Проверки для полей
    errors = {}

    # Проверка русского названия
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название не может быть пустым'

    # Проверка оригинального названия
    if not film.get('title') and not film.get('title_ru'):
        errors['title'] = 'Название на оригинальном языке не может быть пустым, если русское название тоже пустое'

    # Проверка года
    if not film.get('year'):
        errors['year'] = 'Год выпуска не может быть пустым'
    else:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'

    # Проверка описания
    if not film.get('description'):
        errors['description'] = 'Описание не может быть пустым'
    elif len(film['description']) > 2000:
        errors['description'] = 'Описание не может быть длиннее 2000 символов'

    # Если есть ошибки, возвращаем их
    if errors:
        return jsonify(errors), 400

    # Если оригинальное название пустое, используем русское название
    if not film.get('title'):
        film['title'] = film['title_ru']

    try:
        cur.execute("INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (film['title'], film['title_ru'], film['year'], film['description']))
        film_id = cur.fetchone()['id']
        db_close(conn, cur)
        return jsonify({'id': film_id}), 201
    except Exception as e:
        db_close(conn, cur)
        return {'error': f'Ошибка при добавлении фильма: {str(e)}'}, 500
    