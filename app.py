from flask import Flask, url_for, redirect, render_template, abort, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7


app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)


resource_created = False

@app.route("/")
def start():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="{css_path}">
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <ul>
            <li><a href="/lab1>Первая лабораторная</a></li>
            <li><a href="/lab2>Вторая лабораторная</a></li>
            <li><a href="/lab3/">Третья лабораторная</a></li>
            <li><a href="/lab4/">Четвёртная лабораторная</a></li>
            <li><a href="/lab5/">Пятая лабораторная</a><li>
            <li><a href="/lab6/">Шестая лабораторная</a><li>
            <li><a href="/lab7/">Седьмая лабораторная</a><li>
        </ul>
        <footer>
            <p>ФИО: Смирнова Виктория Александровна</p>
            <p>Группа: ФБИ-21</p>
            <p>Курс: 3</p>
            <p>Год: 2024</p>
        </footer>
    </body>
</html>
'''

@app.errorhandler(404)
def err40(err):
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="404_image.jpg")
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Ошибка 404</title>
        <link rel="stylesheet" href="{css_path}">
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
    </head>
    <body>
        <div class="error-container">
            <h1>Ошибка 404</h1>
            <p>Похоже, вы заблудились. Страница, которую вы ищете, не существует.</p>
            <img src="{img_path}" alt="404 Картинка">
            <p><a href="/">Вернуться на главную</a></p>
        </div>
    </body>
</html>
''', 404

@app.errorhandler(500)
def internal_error(error):
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка на сервере</title>
        <link rel="stylesheet" href="{css_path}">
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
    </head>
    <body>
        <h1>Ошибка 500 — Внутренняя ошибка сервера</h1>
        <p>Что-то пошло не так. Пожалуйста, попробуйте вернуться позже или свяжитесь с администратором.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500
