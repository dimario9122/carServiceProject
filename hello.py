from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/hello')
def say_hi_natali():
    return 'Hello Natali!'

@app.route('/hi')
def say_hi_dime():
    return 'Hello Dima'


if __name__ == "__main__":
    app.run()