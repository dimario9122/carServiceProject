from flask import render_template, url_for, redirect, request, jsonify
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
        payload = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        return jsonify(payload)