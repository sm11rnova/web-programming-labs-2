from flask import Blueprint, url_for, redirect, render_template, abort, request


lab2 = Blueprint('lab2', __name__)


resource_created = False


@lab2.route('/lab2/a')
def a():
    return 'без слеша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'

flower_list = [
    {'name': 'роза', 'price': 100},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 30}
]


@lab2.route('/lab2/flowers', methods=['GET', 'POST'])
def show_flowers():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price.isdigit():
            flower_list.lab2end({'name': name, 'price': int(price)})
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    if not name or price <= 0:
        return render_template("error.html", error="Некорректное имя или цена цветка", code=400), 400
    flower_list.lab2end({'name': name, 'price': price})
    return redirect(url_for('show_flowers'))


@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
        return redirect(url_for('show_flowers'))
    else:
        return abort(404, "Цветок с таким ID не найден")


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('show_flowers'))


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculate(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else 'Деление на ноль невозможно'
    power = a ** b

    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/main.css">
        <title>Математические операции</title>
    </head>
    <body>
        <header>
        WEB-программирование, часть 2. Лабораторная работа 2
        </header>
        <h1>Результаты операций с числами {a} и {b}</h1>
        <p>Сумма: {addition}</p>
        <p>Разность: {subtraction}</p>
        <p>Произведение: {multiplication}</p>
        <p>Деление: {division}</p>
        <p>{a}<sup>{b}</sup> = {power}</p>
        <a href="/lab2/calc/1/1">Вернуться к значениям по умолчанию (1, 1)</a>
        <footer>
        &copy; Виктория Смирнова, ФБИ-21, 3 курс, 2024
        </footer>
    </body>
</html>
'''


#обработчик, перенаправляющий с адреса /lab2/calc/ на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def default_calc():
    return redirect(url_for('calculate', a=1, b=1))

#обработчик, перенаправляющий с адреса /lab2/calc/<int:a> на /lab2/calc/a/1
@lab2.route('/lab2/calc/<int:a>')
def redirect_to_calc(a):
    return redirect(url_for('calculate', a=a, b=1))

#список книг на стороне сервера
books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Ф. С. Фицджеральд", "title": "Великий Гэтсби", "genre": "Роман", "pages": 180},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Исторический роман", "pages": 1225},
    {"author": "Дж. Р. Р. Толкин", "title": "Властелин колец", "genre": "Фэнтези", "pages": 1178},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 417},
    {"author": "Артур Конан Дойл", "title": "Приключения Шерлока Холмса", "genre": "Детектив", "pages": 307},
    {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Роман", "pages": 296},
    {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 223},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 496}
]


#обработчик для вывода списка книг
@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


#cписок ягод с названиями, описанием и изображениями
berries = [
    {"name": "Клубника", "description": "Сладкая и сочная ягода с красным цветом.", "image": "strawberry.jpg"},
    {"name": "Голубика", "description": "Маленькие синие ягоды, известные своим вкусом и пользой.", "image": "blueberry.jpg"},
    {"name": "Малина", "description": "Ароматные и вкусные ягоды с ярко-красным цветом.", "image": "raspberry.jpg"},
    {"name": "Ежевика", "description": "Темные, сочные ягоды с кисло-сладким вкусом.", "image": "blackberry.jpg"},
    {"name": "Черника", "description": "Известна своим глубоким синим цветом и антиоксидантами.", "image": "bilberry.jpg"}
]


#обработчик для показа списка ягод с изображениями
@lab2.route('/lab2/berries')
def show_berries():
    return render_template('berries.html', berries=berries)