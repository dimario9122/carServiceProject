from flask import Flask

# создание экземпляра приложения
app = Flask(__name__)

# import views
from app import views
