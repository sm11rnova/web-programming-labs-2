from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import psycopg2
from db import db 
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
     return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/')


@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = 'remember_me' in request.form  #запомнить меня

    if not login_form:
        return render_template('lab8/login.html', error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)
            return redirect('/lab8/')

    return render_template('/lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/logout/')
# @login_required
def logout():
    # session.pop('login', None)
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/public_articles/')
def public_articles():
    # Получаем все публичные статьи
    public_articles = articles.query.filter_by(is_public=True).all()

    # Отображаем их в шаблоне
    return render_template('lab8/public_articles.html', public_articles=public_articles)


@lab8.route('/lab8/search/', methods=['GET', 'POST'])
def search_articles():
    query = request.form.get('query')  # Получаем поисковый запрос из формы

    # Если запрос не пустой, ищем статьи
    if query:
        # Если пользователь авторизован
        if current_user.is_authenticated:
            # Ищем статьи, которые являются либо публичными, либо принадлежат текущему пользователю
            search_results = articles.query.filter(
                ((articles.title.ilike(f'%{query}%')) |  # Ищем в заголовке
                 (articles.article_text.ilike(f'%{query}%'))) &  # Ищем в тексте статьи
                ((articles.is_public == True) | (articles.login_id == current_user.id))  # Либо публичные, либо свои статьи
            ).all()
        else:
            # Если пользователь не авторизован, ищем только публичные статьи
            search_results = articles.query.filter(
                (articles.title.ilike(f'%{query}%')) |  # Ищем в заголовке
                (articles.article_text.ilike(f'%{query}%'))  # Ищем в тексте статьи
                & (articles.is_public == True)  # Ищем только публичные статьи
            ).all()

        return render_template('lab8/search_results.html', search_results=search_results, query=query)

    # Если запрос пустой, просто возвращаем пустую страницу поиска
    return render_template('lab8/search_results.html', search_results=None, query=None)


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = 'is_favorite' in request.form  
        is_public = 'is_public' in request.form 

        # Проверка на пустые поля
        if not title:
            return render_template('lab8/create_article.html', error='Заголовок не должен быть пустым')

        if not article_text:
            return render_template('lab8/create_article.html', error='Текст статьи не должен быть пустым')

        # Создание нового объекта статьи
        new_article = articles(
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public,
            likes=0,
            login_id=current_user.id  # связываем статью с текущим пользователем
        )
        # Сохранение в базу данных
        db.session.add(new_article)
        db.session.commit()

        # Перенаправление на страницу со списком статей
        return redirect('/lab8/articles/')

    # Если запрос GET, просто показываем форму
    return render_template('lab8/create_article.html')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    articly = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/article_list.html', articly=articly)

@lab8.route('/lab8/articles/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является владельцем статьи
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = 'is_favorite' in request.form
        is_public = 'is_public' in request.form

        # Проверка на пустые поля
        if not title:
            return render_template('lab8/edit_article.html', article=article, error='Заголовок не должен быть пустым')

        if not article_text:
            return render_template('lab8/edit_article.html', article=article, error='Текст статьи не должен быть пустым')

        # Обновление статьи
        article.title = title
        article.article_text = article_text
        article.is_favorite = is_favorite
        article.is_public = is_public

        db.session.commit()

        # Перенаправление на страницу со списком статей
        return redirect('/lab8/articles/')

    return render_template('lab8/edit_article.html', article=article)

@lab8.route('/lab8/articles/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является владельцем статьи
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    # Удаление статьи
    db.session.delete(article)
    db.session.commit()

    # Перенаправление на страницу со списком статей
    return redirect('/lab8/articles/')