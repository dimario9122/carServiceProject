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

        #
        # запрос пароля из базы данных
        #

        # получение абсолютного пути к файлу базы данных
        path_to_db_file = os.path.abspath('.')
        path_to_db_file += '/app/database.db'
        connect_db = sqlite3.connect(path_to_db_file)
        cursor = connect_db.cursor()

        # запрос на получение пароля для логина из формы
        query = "SELECT Password FROM client WHERE Login='%s'" % payload['username']
        cursor.execute(query)
        data_from_db = cursor.fetchall()

        return jsonify({
            'form_data': payload,
            'database_data': data_from_db
        })