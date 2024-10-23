from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

resource_created = False

@app.route("/")
@app.route("/index")
def index():
    lab1_link = url_for("lab1")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="{css_path}">
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
    web_link = url_for("web")
    author_link = url_for("author")
    oak_link = url_for("oak")
    counter_link = url_for("counter")
    custom_link = url_for("custom")
    trigger_error_link = url_for("trigger_error")
    resource_link = url_for("resource")
    css_path = url_for("static", filename="lab1.css")
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="{root_link}">На главную</a>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="{root_link}">Главная страница</a></li>
            <li><a href="{web_link}">Страница web-сервера</a></li>
            <li><a href="{author_link}">Страница автора</a></li>
            <li><a href="{oak_link}">Страница с дубом</a></li>
            <li><a href="{counter_link}">Счётчик посещений</a></li>
            <li><a href="{custom_link}">Кастомная страница</a></li>
            <li><a href="{trigger_error_link}">Вызвать ошибку 500</a></li>
            <li><a href="{resource_link}">Управление ресурсом</a></li>
        </ul>
    </body>
</html>
'''

@app.route("/error/400")
def error_400():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 400</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не понял запрос.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400

@app.route("/error/401")
def error_401():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 401</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401

@app.route("/error/402")
def error_402():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 402</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402

@app.route("/error/403")
def error_403():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 403</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ запрещён.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403

@app.route("/error/405")
def error_405():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 405</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод не разрешён.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405

@app.route("/error/418")
def error_418():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>418 I'm a Teapot</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>418 I'm a Teapot</h1>
        <p>Я — чайник.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

@app.route("/lab1/web")
def web():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>web-сервер на flask</h1>
    </body>
</html>
''', 200, {
        'X-server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@app.route("/lab1/author")
def author():
    css_path = url_for("static", filename="lab1.css")
    name = "Смирнова Виктория Александровна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Информация об авторе</h1>
        <p>Студент: {name}</p>
        <p>Группа: {group}</p>
        <p>Факультет: {faculty}</p>
        <a href="/web">web</a>
    </body>
</html>
'''

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
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Счётчик посещений</h1>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <a href="{reset_link}">Очистить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    counter_link = url_for('counter')
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Счётчик очищен</h1>
        <a href="{counter_link}">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def create_resource():
    global resource_created
    css_path = url_for("static", filename="lab1.css")
    if not resource_created:
        resource_created = True
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Успешно: ресурс создан</h1>
        <a href="/lab1/resource">Назад к ресурсу</a>
    </body>
</html>
''', 201
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Отказано: ресурс уже создан</h1>
        <a href="/lab1/resource">Назад к ресурсу</a>
    </body>
</html>
''', 400

#обработчик для удаления ресурса
@app.route("/lab1/delete")
def delete_resource():
    global resource_created
    css_path = url_for("static", filename="lab1.css")
    if resource_created:
        resource_created = False
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Успешно: ресурс удалён</h1>
        <a href="/lab1/resource">Назад к ресурсу</a>
    </body>
</html>
''', 200
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Отказано: ресурс отсутствует</h1>
        <a href="/lab1/resource">Назад к ресурсу</a>
    </body>
</html>
''', 400

#родительская страница, показывающая статус ресурса и предоставляющая ссылки 
#на создание/удаление
@app.route("/lab1/resource")
def resource():
    css_path = url_for("static", filename="lab1.css")
    if resource_created:
        status = "Ресурс создан"
    else:
        status = "Ресурс ещё не создан"

    create_link = url_for("create_resource")
    delete_link = url_for("delete_resource")

    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>{status}</h1>
        <a href="{create_link}">Создать ресурс</a> |
        <a href="{delete_link}">Удалить ресурс</a>
    </body>
</html>
'''

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="404_image.jpg")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <link rel="stylesheet" href="{css_path}">
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
    return 1 / 0  

@app.errorhandler(500)
def internal_error(error):
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка на сервере</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Ошибка 500 — Внутренняя ошибка сервера</h1>
        <p>Что-то пошло не так. Пожалуйста, попробуйте вернуться позже или свяжитесь с администратором.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500

@app.route("/lab1/custom")
def custom():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="custom_image.jpg")  
    return f'''
<!doctype html>
<html>
    <head>
        <title>Кастомная страница</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Добро пожаловать на кастомную страницу</h1>
        <p>Это пример страницы, на которой можно разместить различный текст. Flask предоставляет гибкие возможности для создания веб-приложений с различными функциональными и визуальными элементами. Вы можете легко управлять маршрутами, работать с шаблонами и даже подключать базы данных.</p>
        <p>Flask позволяет использовать любые внешние библиотеки для разработки пользовательских интерфейсов, а также взаимодействовать с фронтендом через API. Это один из самых популярных фреймворков для небольших и средних проектов на Python.</p>
        <p>Этот текст и изображение, которое вы видите ниже, выводятся при помощи нового маршрута. Вы также можете настраивать любые заголовки ответа для передачи дополнительной информации о странице.</p>
        <img src="{img_path}" alt="Пример изображения">
    </body>
</html>
''', 200, {
        'Content-Language': 'ru',  
        'X-Custom-Header-1': 'Custom-Value-1',  
        'X-Custom-Header-2': 'Custom-Value-2',  
        'Content-Type': 'text/html; charset=utf-8' 
    }





@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if not name:
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="/static/main.css">
            </head>
            <body>
                <h1>Ошибка 400</h1>
                <p>Вы не задали имя цветка.</p>
                <a href="/lab2/flowers">Посмотреть список всех цветов</a>
            </body>
        </html>
        ''', 400
    
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/main.css">
    </head>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {', '.join(flower_list)}</p>
        <a href="/lab2/flowers">Посмотреть список всех цветов</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def missing_flower_name():
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="/static/main.css">
        </head>
        <body>
            <h1>Ошибка 400</h1>
            <p>Вы не задали имя цветка.</p>
            <a href="/lab2/flowers">Посмотреть список всех цветов</a>
        </body>
    </html>
    ''', 400

@app.route('/lab2/flowers')
def show_flowers():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/main.css">
    </head>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list)}
        </ul>
        <a href="/lab2/add_flower/">Добавить новый цветок</a>
        <a href="/lab2/clear_flowers" style="display:block; margin-top: 10px;">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="/static/main.css">
            </head>
            <body>
                <h1>Ошибка 404</h1>
                <p>Цветок с таким ID не найден.</p>
                <a href="/lab2/flowers">Посмотреть список всех цветов</a>
            </body>
        </html>
        ''', 404

    flower_name = flower_list[flower_id]
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/main.css">
    </head>
    <body>
        <h1>Информация о цветке</h1>
        <p>Цветок: {flower_name}</p>
        <p>ID цветка: {flower_id}</p>
        <a href="/lab2/flowers">Посмотреть список всех цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/main.css">
    </head>
    <body>
        <h1>Список очищен</h1>
        <p>Все цветы были удалены</p>
        <a href="/lab2/flowers">Посмотреть список всех цветов</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Виктория Смирнова'
    lab_number = '2'
    group = 'ФБИ-21'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html', name=name, lab_number=lab_number, 
                           group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

