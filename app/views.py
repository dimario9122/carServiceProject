from flask import render_template, url_for, redirect, request, jsonify
import sqlite3
import os
import random
from app import app


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('button') == 'do record':
            return redirect(url_for('record'))
    return render_template('home.html')


@app.route('/amount', methods=['GET', 'POST'])
def amount():
    '''
    Получение марки, модели авто
    и услуги выбранной пользователем

    Расчет сроков и стоимости
    Вывод пользователю на экран

    Кнопки Заказ. заказ через менеджера. Отмена

    Если заказ -
    дальше идем на страницу с вводом номера телефона, код, лк
    '''
    pass


@app.route('/new_record', methods=['GET'])
def new_record():
    '''
    Всю логику оформления полей из record
    поле марка авто
    поле модель авто
    поле тип услуги

    кнопка продолжить - amount
    '''
    return render_template('record.html')


@app.route('/record/<number>', methods=['GET', 'POST'])
def record(number):
    if request.method == 'GET':
        '''
            запрос данных из базы данных
            '''
        # получение абсолютного пути к файлу базы данных
        path_to_db_file = os.path.abspath('.')
        path_to_db_file += '/app/database.db'
        connect_db = sqlite3.connect(path_to_db_file)
        cursor = connect_db.cursor()
        # запрос всех марок авто
        query = "SELECT Trademark FROM car GROUP BY Trademark"
        cursor.execute(query)
        data_from_db = cursor.fetchall()
        trademark_list = [x[0] for x in data_from_db]
        # есть ли смысл в этом месте???
        payload = {
            'trademark_name': trademark_list[0]
        }
        # запрос моделей определенной марки
        query = "SELECT Model FROM car WHERE Trademark='{0}'".format(payload['trademark_name'])

        cursor.execute(query)
        data_from_db = cursor.fetchall()
        model_list = [x[0] for x in data_from_db]
        # запрос списка услуг
        query = "SELECT About FROM service"
        cursor.execute(query)
        data_from_db = cursor.fetchall()
        about_list = [x[0] for x in data_from_db]

        connect_db.close()
        '''
        запрос пароля из базы данных выполнен
        '''
        return render_template('record.html', message=request.args.get('Trademark'),
                               trademark_list=trademark_list, model_list=model_list, about_list=about_list)
    if request.method == 'POST':
        if request.form.get('button') == 'go to check':
            return redirect(url_for('check'))
    return render_template('record.html')


@app.route('/check/<number>', methods=['GET', 'POST'])
def check(number):
    print(number)
    if request.method == 'POST':
        if request.form.get('code') == str(sms_code):
            update_sms_code()
            # здесь будет перенаправление в личный кабинет
            return render_template('check.html', message=sms_code, error='OK!')
        else:
            return render_template('check.html', message=sms_code, error='Неверный код!')
    elif request.method == 'GET':
        update_sms_code()
        return render_template('check.html', message=sms_code)


sms_code = 0
def update_sms_code():
    global sms_code
    sms_code = random.randint(1000, 9999)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_manager.html')
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
        query = "SELECT Password FROM client WHERE Login='{0}'".format(payload['username'])
        cursor.execute(query)
        data_from_db = cursor.fetchone()

        connect_db.close()
        '''
        запрос пароля из базы данных выполнен
        '''

        # если пользователя с такми логином нет в бд
        if data_from_db is None:
            message = 'Неверный логин или пароль'
            return render_template('login_manager.html', message=message)

        # проверка на необходимость смены стандартного пароля
        if data_from_db[0] == payload['password'] == 'admin' and payload['username'] == 'admin':
            return redirect(url_for('change_password', username=payload['username']))

        # проверка пользовательского пароля и пароля из бд
        if data_from_db[0] == payload['password']:
            return redirect(url_for('home'))
        else:
            message = 'Неверный логин или пароль'
            return render_template('login_manager.html', message=message)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = ''
    status = 'Требуется изменение стандартного пароля!'
    if request.method == 'GET':
        username = request.args.get('username')
    if request.method == 'POST':
        status = 'Пароль успешно изменен!'
        username = request.form.get('username')
        form_passwd = request.form.get('password')
        '''
        запись нового пароля в бд
        '''
        # получение абсолютного пути к файлу базы данных
        path_to_db_file = os.path.abspath('.')
        path_to_db_file += '/app/database.db'
        connect_db = sqlite3.connect(path_to_db_file)
        cursor = connect_db.cursor()

        # получение пароля для текущего логина из формы
        query = "UPDATE client SET Password='{0}' WHERE Login='{1}'".format(form_passwd, username)
        cursor.execute(query)
        connect_db.commit()

        connect_db.close()
        '''
        конец записи нового пароля в бд
        '''
    return render_template('change_password.html', username=username, status=status)


'''
    На Home - жимаем вход - клиент -вводим номер телефона
    нажимаем продолжить и попадаем в /login_client маршрут
'''


@app.route('/login_client', methods=['POST'])
def login_client():
    if request.method == 'POST':
        number = request.form.get('phone_number')
        return redirect(url_for('check', number=number))
    return render_template('home.html')
