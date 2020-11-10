from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@app.route('/newlogin', methods=['get'])
def create_admin_login():
    message='Create new login and new password,please'
    if request.args.get("username") and request.args.get("password"):
        with open('database1.txt','w',encoding='utf8') as f:
            f.write((request.args.get("username")+':'+request.args.get("password")))
            f.close()
    else:
        return render_template('login.html',message=message)
    return redirect('/login')


@app.route('/login', methods=['get'])
def do_admin_login():
    with open('database1.txt','r',encoding='utf8') as f:
        num=f.read().splitlines()
        num_log_pass=num[0].split(':')

        if request.args.get("username")==num_log_pass[0]=='admin' and request.args.get("password")==num_log_pass[1]=='admin':
            f.close()
            message='Create new login and new password,please'
            render_template('login.html',message=message)
            return redirect('/newlogin')
        elif request.args.get("username")==num_log_pass[0] and request.args.get("password")==num_log_pass[1]:
            session['logged_in'] = True
            f.close()
            return home()
        else:
            #flash('wrong password!')
            return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)