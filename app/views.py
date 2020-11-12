from flask import render_template, url_for, redirect, request, jsonify
import sqlite3
import os
from app import app


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        # получение данных из запроса
        payload = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        '''
        запрос пароля из базы данных
        '''
        # получение абсолютного пути к файлу базы данных
        path_to_db_file = os.path.abspath('.')
        path_to_db_file += '/app/database.db'
        connect_db = sqlite3.connect(path_to_db_file)
        cursor = connect_db.cursor()

        # получение пароля для текущего логина из формы
        query = "SELECT Password FROM client WHERE Login='%s'" % payload['username']
        cursor.execute(query)
        data_from_db = cursor.fetchone()

        connect_db.close()
        '''
        запрос пароля из базы данных выполнен
        '''

        # если пользователя с такми логином нет в бд
        if data_from_db is None:
            message = 'Неверный логин или пароль'
            return render_template('login.html', message=message)

        # проверка на необходимость смены стандартного пароля
        if data_from_db[0] == payload['password'] == 'admin' and payload['username'] == 'admin':
            return 'Redirect to page change passwd'

        # проверка пользовательского пароля и пароля из бд
        if data_from_db[0] == payload['password']:
            return 'Redirect to home page. Welcome user'
        else:
            message = 'Неверный логин или пароль'
            return render_template('login.html', message=message)