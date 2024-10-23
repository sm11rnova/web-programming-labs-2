from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    lab1_link = url_for("lab1")
    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <ul>
            <li><a href="{lab1_link}">Первая лабораторная</a></li>
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

@app.route("/lab1")
def lab1():
    root_link = url_for("index")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="{root_link}">На главную</a>
    </body>
</html>
'''

@app.route("/error/400")
def error_400():
    return "400 Bad Request: Сервер не понял запрос.", 400

@app.route("/error/401")
def error_401():
    return "401 Unauthorized: Требуется аутентификация.", 401

@app.route("/error/402")
def error_402():
    return "402 Payment Required: Требуется оплата.", 402

@app.route("/error/403")
def error_403():
    return "403 Forbidden: Доступ запрещён.", 403

@app.route("/error/405")
def error_405():
    return "405 Method Not Allowed: Метод не разрешён.", 405

@app.route("/error/418")
def error_418():
    return "418 I'm a teapot: Я — чайник. RFC 2324.", 418

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
            </body>
        </html>""", 200, {
            'X-server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Смирнова Виктория Александровна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="oak.jpeg")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{img_path}">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('reset_counter')
    return f'''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: {count}
        <br>
        <a href="{reset_link}">Очистить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    counter_link = url_for('counter')
    return f'''
<!doctype html>
<html>
    <body>
        Счётчик очищен.
        <br>
        <a href="{counter_link}">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i><div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    img_path = url_for("static", filename="404_image.jpg")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                font-size: 50px;
                color: #333;
            }}
            p {{
                font-size: 20px;
                color: #666;
            }}
            a {{
                text-decoration: none;
                color: #007BFF;
                font-size: 18px;
            }}
            a:hover {{
                color: #0056b3;
            }}
            img {{
                max-width: 300px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Упс! Страница не найдена.</h1>
        <p>Кажется, вы попали не туда. Но не волнуйтесь, мы вас вернём на главную.</p>
        <a href="/">Вернуться на главную</a>
        <br><br>
        <img src="{img_path}" alt="404 Not Found">
    </body>
</html>
''', 404

@app.route("/error/trigger")
def trigger_error():
    return 1 / 0  # Это вызовет ошибку деления на ноль

# Перехватчик ошибки 500 (Internal Server Error)
@app.errorhandler(500)
def internal_error(error):
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка на сервере</title>
    </head>
    <body>
        <h1>Ошибка 500 — Внутренняя ошибка сервера</h1>
        <p>Что-то пошло не так. Пожалуйста, попробуйте вернуться позже или свяжитесь с администратором.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500