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


@app.route('/new_record', methods=['GET', 'POST'])
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
        trademark_list = [x[0] + ' ' + x[1] for x in data_from_db]

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
            return redirect(
                url_for('amount', phone_number=request.form.get('phone_number'), Trademark=trademark_and_model[0],
                        Model=trademark_and_model[1], About=request.form.get('About')))
    return render_template('record.html')


def connect_to_db():
    # подключение к базе данных
    path_to_db_file = os.path.abspath('.')
    path_to_db_file += '/app/database.db'
    connect_db = sqlite3.connect(path_to_db_file)
    return connect_db


def get_cost_plane_date(trademark, model, about):
    cursor = connect_to_db().cursor()

    # получить car_id по Trademark, Model
    # из таблицы car
    query = "SELECT car_id FROM car WHERE Trademark='{0}' AND Model='{1}'".format(trademark, model)
    car_id = cursor.execute(query).fetchone()[0]

    # получить service_id по About
    # из таблицы service
    query = "SELECT service_id FROM service WHERE About='{0}'".format(about)
    service_id = cursor.execute(query).fetchone()[0]

    # получить cost, PlaneTime по car_id и service_id
    # из таблицы service_car
    query = "SELECT cost, planetime, service_car_id FROM service_car WHERE service_id='{0}' AND car_id='{1}'".format(
        service_id, car_id)
    cost, plane_time, service_car_id = cursor.execute(query).fetchone()
    return cost, plane_time, service_car_id


@app.route('/amount', methods=['GET', 'POST'])
def amount():
    if request.method == 'GET':
        phone_number = request.args.get('phone_number')
        trademark = request.args.get('Trademark')
        model = request.args.get('Model')
        about = request.args.get('About')
        cost, plane_time, service_car_id = get_cost_plane_date(trademark, model, about)

        return render_template('amount.html', phone_number=phone_number, Trademark=trademark,
                               Model=model, About=about, cost=cost, time=plane_time)
    if request.method == 'POST':
        conn = connect_to_db()
        cursor = conn.cursor()

        cost = request.form.get('cost')
        plane_time = request.form.get('time')
        trademark = request.args.get('Trademark')
        model = request.args.get('Model')
        about = request.args.get('About')
        phone = request.args.get('phone_number')

        # получить id из таблицы Клиент
        query = "SELECT client_id FROM client WHERE phone='{0}'".format(phone)
        client_id = cursor.execute(query).fetchone()

        # если новый клиент
        if client_id is None:
            # сохранить в бд
            query = "INSERT INTO client(FIO, Phone, Login, Password) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
                "Фамилия Имя Отчество",
                phone,
                phone,
                "здесь должна быть рандомная строка"
            )
            cursor.execute(query)
            # получим id только что добавленного клиента
            query = "SELECT client_id FROM client WHERE phone='{0}'".format(phone)
            client_id = cursor.execute(query).fetchone()[0]

        # получить id из таблицы Статус
        status_id = 3  # значение по-умолчанию (Отмена)
        if request.form.get('button') == 'order':
            status_id = cursor.execute("SELECT status_id FROM status WHERE name='Принято'").fetchone()[0]
        elif request.form.get('button') == 'order_manager':
            status_id = \
                cursor.execute("SELECT status_id FROM status WHERE name='Отредактировано менеджером'").fetchone()[0]
        elif request.form.get('button') == 'cancel':
            status_id = cursor.execute("SELECT status_id FROM status WHERE name='Отменено'").fetchone()[0]

        # добавить запись в таблицу обращение и получить id этого обращения
        query = "INSERT INTO purchase(client_id, status_id, planedate, comment) VALUES('{0}', '{1}', '{2}', '{3}')"\
            .format(client_id, status_id, plane_time, 'no comment')
        cursor.execute(query)

        purchase_id = cursor.execute("SELECT purchase_id FROM purchase ORDER BY purchase_id DESC LIMIT 1").fetchone()[0]

        # получить id из таблицы Услуга-авто
        service_car_id = get_cost_plane_date(trademark, model, about)[2]

        # внести запись в таблицу Элементы обращения
        query = "INSERT INTO purchase_elem(purchase_id, service_car_id, quantity, planedate, planecost) " \
                "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')"\
            .format(purchase_id, service_car_id, cost, plane_time, cost)
        cursor.execute(query)

        # save state
        conn.commit()

        if request.form.get('button') == 'cancel':
            # переход на домашнюю страницу
            return redirect(url_for('home'))
        return redirect(url_for('check', number=phone))
    return render_template('record.html')


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


@app.route('/check/<number>', methods=['GET', 'POST'])
def check(number):
    print(number)
    if request.method == 'POST':
        if request.form.get('code') == str(sms_code):
            update_sms_code()
            # здесь будет перенаправление в личный кабинет
            print('Redirect to client lk')
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
        cursor = connect_to_db().cursor()

        # получение пароля для текущего логина из формы
        query = "SELECT Password FROM client WHERE Login='{0}'".format(payload['username'])
        cursor.execute(query)
        data_from_db = cursor.fetchone()

        connect_to_db().close()
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
            # логин успешен - перенаправление на админ лк
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
        cursor = connect_to_db().cursor()

        # получение пароля для текущего логина из формы
        query = "UPDATE client SET Password='{0}' WHERE Login='{1}'".format(form_passwd, username)
        cursor.execute(query)
        connect_to_db().commit()

        connect_to_db().close()
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
