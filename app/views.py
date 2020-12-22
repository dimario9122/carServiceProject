from flask import render_template, url_for, redirect, request, jsonify
import sqlite3
import os
import random
from app import app
from flask_cors import CORS

CORS(app) ##Установка CORS политики

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('button') == 'do record':
            return redirect(url_for('record'))
    return render_template('home.html')



@app.route('/new_record', methods=['GET','POST'])
def new_record():
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
        query = "SELECT Trademark, Model FROM car"
        cursor.execute(query)
        data_from_db = cursor.fetchall()
        trademark_list = [x[0]+' '+x[1] for x in data_from_db]

        # запрос списка услуг
        query = "SELECT About FROM service"
        cursor.execute(query)
        data_from_db = cursor.fetchall()
        about_list = [x[0] for x in data_from_db]

        connect_db.close()
        '''
        запрос данных из базы данных выполнен
        '''
        return jsonify(trademark_list=trademark_list, about_list=about_list)
    if request.method == 'POST':
        if request.form.get('button') == 'go to amount':
            trademark_and_model = request.form.get('Trademark')
            trademark_and_model = trademark_and_model.split()
            return redirect(url_for('amount', phone_number=request.form.get('phone_number'),Trademark=trademark_and_model[0],
                                    Model = trademark_and_model[1], About = request.form.get('About')))
    return render_template('record.html')


    '''
    Всю логику оформления полей из record
    поле марка авто
    поле модель авто
    поле тип услуги

    кнопка продолжить - amount
    '''


def calculate_cost(Trademark, Model, About):
    # функция расчета стоимости услуг автосервиса
    path_to_db_file = os.path.abspath('.')
    path_to_db_file += '/app/database.db'
    connect_db = sqlite3.connect(path_to_db_file)
    cursor = connect_db.cursor()

    # проверка марки
    if Trademark == 'Mercedes':
        cost = 3000
    elif Trademark == 'BMW':
        cost = 2500
    elif Trademark == 'AUDI':
        cost = 2300
    elif Trademark == 'Toyota':
        cost = 1700
    elif Trademark == 'Volvo':
        cost = 1500
    elif Trademark == 'Nissan':
        cost = 1250
    elif Trademark == 'Chevrolet':
        cost = 900
    else:
        cost=1000
    #проверка модели авто
    payload = {
        'trademark_name': Trademark,
    }

    query = "SELECT Model FROM car WHERE Trademark='{0}'".format(payload['trademark_name'])
    cursor.execute(query)
    data_from_db = cursor.fetchall()
    ModelFromDB = [x[0] for x in data_from_db]
    for i in range(len(ModelFromDB)):
        if Model == ModelFromDB[i]:
            Model = i+1
    if Model == 1:
        cost = cost * 12
    elif Model == 2:
        cost = cost * 11
    elif Model == 3:
        cost = cost * 10
    elif Model == 4:
        cost = cost * 9
    elif Model == 5:
        cost = cost * 8
    elif Model == 6:
        cost = cost * 7
    elif Model == 7:
        cost = cost * 6.5
    elif Model == 8:
        cost = cost * 6
    elif Model == 9:
        cost = cost * 5.5
    elif Model == 10:
        cost = cost * 5
    else:
        cost = cost * 4
    #проверка работ
    payload = {
        'About': About
    }

    query = "SELECT Service_id FROM service WHERE About='{0}'".format(payload['About'])
    cursor.execute(query)
    data_from_db = cursor.fetchone()
    service_id = data_from_db[0]

    if service_id == 1:
        cost = cost * 5
    elif service_id == 2:
        cost = cost * 4
    elif service_id == 3:
        cost = cost * 3
    elif service_id == 4:
        cost = cost * 2

    connect_db.close()

    return cost

def calculate_time(cost):
    # функция расчета времени
    if cost < 25000:
        time = '1 неделя'
    elif cost >= 25000 and cost < 50000:
        time = '2 недели'
    elif cost >= 50000 and cost < 75000:
        time = '3 недели'
    elif cost >= 75000 and cost < 100000:
        time = '4 недели'
    elif cost >= 100000 and cost < 125000:
        time = '5 недель'
    else:
        time = '6 недель'
    return time

@app.route('/amount', methods=['GET', 'POST'])
def amount():
    if request.method == 'GET':
        phone_number = request.args.get('phone_number')
        Trademark = request.args.get('Trademark')
        Model = request.args.get('Model')
        About = request.args.get('About')
        cost = calculate_cost(Trademark, Model, About)
        PlaneTime = calculate_time(cost)

        return render_template('amount.html',phone_number=phone_number, Trademark = Trademark,
                                    Model = Model, About = About, cost = cost,time = PlaneTime)
    if request.method == 'POST':
        if request.form.get('button') == 'go to check':
            # переход на страницу проверки номера
            cost = request.form.get('cost')
            PlaneTime = request.form.get('time')
            Trademark = request.args.get('Trademark')
            Model = request.args.get('Model')
            About = request.args.get('About')

            # подключение к базе данных
            path_to_db_file = os.path.abspath('.')
            path_to_db_file += '/app/database.db'
            connect_db = sqlite3.connect(path_to_db_file)
            cursor = connect_db.cursor()

            # блок вставки данных в таблицу service_car

            payload = {
                'trademark_name': Trademark,
                'model': Model
            }

            query = "SELECT Car_id FROM car WHERE Trademark='{0}' AND Model='{1}'".format(payload['trademark_name'],
                                                                                          payload['model'])
            cursor.execute(query)
            data_from_db = cursor.fetchone()
            car_id = data_from_db[0]

            payload = {
                'About': About
            }

            query = "SELECT Service_id FROM service WHERE About='{0}'".format(payload['About'])
            cursor.execute(query)
            data_from_db = cursor.fetchone()
            service_id = data_from_db[0]

            payload = {
                'Service_id': service_id,
                'Car_id': car_id,
                'Cost': cost,
                'PlaneTime': PlaneTime
            }

            query = "INSERT INTO service_car (Service_car_id, Service_id, Car_id, Cost, PlaneTime) " \
                    "VALUES (NULL,'{0}','{1}','{2}','{3}')".format(
                payload['Service_id'], payload['Car_id'], payload['Cost'], payload['PlaneTime'])
            cursor.execute(query)
            connect_db.commit()
            connect_db.close()
            # конец блока вставки данных в таблицу service_car

            number = request.args.get('phone_number')
            return redirect(url_for('check', number=number))
        if request.form.get('button') == 'go to home':
            # переход на домашнюю страницу
            return redirect(url_for('home'))
    return render_template('record.html')
    '''
    Получение марки, модели авто
    и услуги выбранной пользователем

    Расчет сроков и стоимости
    Вывод пользователю на экран

    Кнопки Заказ. заказ через менеджера. Отмена

    Если заказ -
    дальше идем на страницу с вводом номера телефона, код, лк
    '''


# функция не используется
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


@app.route('/check/<number>/', methods=['GET', 'POST'])
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
